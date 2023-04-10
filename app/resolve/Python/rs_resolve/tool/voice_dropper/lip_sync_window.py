import dataclasses
import sys

from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QStringListModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.core import (
    config,
    pipe as p,
)
from rs.gui import (
    appearance,
)

from rs_resolve.core import (
    track_name2index,
)
from rs_resolve.tool.voice_dropper.lip_sync_window_ui import Ui_MainWindow

APP_NAME = 'lipSyncWindow'


def get_track_names(timeline, track_type):
    r = []
    for i in range(1, timeline.GetTrackCount(track_type) + 1):
        r.append(timeline.GetTrackName(track_type, i))
    return r


def get_resolve_window(pj_name):
    import pygetwindow
    for t in pygetwindow.getAllTitles():
        if t.startswith('DaVinci Resolve') and t.endswith(pj_name):
            return pygetwindow.getWindowsWithTitle(t)[0]
    return None


def get_index(timeline, track_type, v):
    m: QStringListModel = v.model()
    names = p.pipe(
        v.selectionModel().selectedIndexes(),
        p.map(m.data),
        p.map(str),
        list,
    )
    if len(names) == 0:
        return 0

    return track_name2index(timeline, track_type, names[0])


@dataclasses.dataclass
class ConfigData(config.Data):
    wait: float = 2.0


class MainWindow(QMainWindow):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('%s' % APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(300, 300)
        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)

        # list
        for w in [self.ui.videoListView, self.ui.audioListView]:
            m = QStringListModel()
            w.setModel(m)

        # style sheet
        self.ui.applyButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.updateTrackButton.clicked.connect(self.update_track)

        #
        self.ui.closeButton.setFocus()
        self.update_track()

    def update_track(self) -> None:
        v_m: QStringListModel = self.ui.videoListView.model()
        a_m: QStringListModel = self.ui.audioListView.model()
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            v_m.setStringList([])
            a_m.setStringList([])
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            v_m.setStringList([])
            a_m.setStringList([])
            return
        v_m.setStringList(get_track_names(timeline, 'video'))
        a_m.setStringList(get_track_names(timeline, 'audio'))

    def set_data(self, c: ConfigData):
        self.ui.tatieWaitSpinBox.setValue(c.wait)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.wait = self.ui.tatieWaitSpinBox.value()
        return c

    def get_video_track_index(self, timeline):
        return get_index(timeline, 'video', self.ui.videoListView)

    def get_audio_track_index(self, timeline):
        return get_index(timeline, 'audio', self.ui.audioListView)

    def load_config(self) -> None:
        c = ConfigData()
        if self.config_file.is_file():
            c.load(self.config_file)
        self.set_data(c)

    def save_config(self) -> None:
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        c = self.get_data()
        c.save(self.config_file)

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)

    def show(self) -> None:
        self.load_config()
        super().show()


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())
