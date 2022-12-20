from functools import partial

import dataclasses
import sys

from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QStringListModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow, QComboBox,
)
from PySide2.QtGui import (
    QColor,
)

from rs.core import (
    config,
    pipe as p,
)
from rs.gui import (
    appearance,
    log,
)

from rs_resolve.core import (
    get_currentframe,
    get_fps,
)
from rs_resolve.tool.playhead.playhead_ui import Ui_MainWindow

APP_NAME = 'Playhead'


def set_playhead(timeline, frame):
    timeline.SetCurrentTimecode(str(
        max(frame, timeline.GetStartFrame())
    ))


def get_track_names(timeline, track_type):
    r = []
    for i in range(1, timeline.GetTrackCount(track_type) + 1):
        r.append(timeline.GetTrackName(track_type, i))
    return r


def track_name2index(timeline, track_type, name):
    for i in range(1, timeline.GetTrackCount(track_type) + 1):
        if timeline.GetTrackName(track_type, i) == name:
            return i
    return 0


@dataclasses.dataclass
class ConfigData(config.Data):
    num01: int = 5
    num02: int = 15


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
        self.resize(200, 200)
        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # combobox
        for w in [self.ui.videoComboBox, self.ui.audioComboBox, self.ui.subtitleComboBox]:
            m = QStringListModel()
            w.setModel(m)

        # style sheet
        self.ui.updateButton.setStyleSheet(appearance.other_stylesheet)
        for w in [
            self.ui.n01LeftButton,
            self.ui.n01RightButton,
            self.ui.n02LeftButton,
            self.ui.n02RightButton,
            self.ui.vidioLeftButton,
            self.ui.vidioRightButton,
            self.ui.audioLeftButton,
            self.ui.audioRightButton,
            self.ui.subtitleLeftButton,
            self.ui.subtitleRightButton,
            self.ui.timelineLeftButton,
            self.ui.timelineRightButton,
        ]:
            w.setStyleSheet(appearance.in_stylesheet)

        # event

        self.ui.updateButton.clicked.connect(self.update_track)
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))

        self.ui.n01LeftButton.clicked.connect(partial(self.move_playhead, -self.ui.num01SpinBox.value()))
        self.ui.n01RightButton.clicked.connect(partial(self.move_playhead, self.ui.num01SpinBox.value()))
        self.ui.n02LeftButton.clicked.connect(partial(self.move_playhead, -self.ui.num02SpinBox.value()))
        self.ui.n02RightButton.clicked.connect(partial(self.move_playhead, self.ui.num02SpinBox.value()))

        self.ui.vidioLeftButton.clicked.connect(partial(
            self.move_to_pre_item, 'video', self.ui.videoComboBox
        ))
        self.ui.vidioRightButton.clicked.connect(partial(
            self.move_to_next_item, 'video', self.ui.videoComboBox
        ))
        self.ui.audioLeftButton.clicked.connect(partial(
            self.move_to_pre_item, 'audio', self.ui.audioComboBox
        ))
        self.ui.audioRightButton.clicked.connect(partial(
            self.move_to_next_item, 'audio', self.ui.audioComboBox
        ))
        self.ui.subtitleLeftButton.clicked.connect(partial(
            self.move_to_pre_item, 'subtitle', self.ui.subtitleComboBox
        ))
        self.ui.subtitleRightButton.clicked.connect(partial(
            self.move_to_next_item, 'subtitle', self.ui.subtitleComboBox
        ))

        self.ui.timelineLeftButton.clicked.connect(self.set_start)
        self.ui.timelineRightButton.clicked.connect(self.set_end)

        #
        self.update_track()
        self.ui.closeButton.setFocus()

    def set_data(self, c: ConfigData):
        self.ui.num01SpinBox.setValue(c.num01)
        self.ui.num02SpinBox.setValue(c.num02)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.num01 = self.ui.num01SpinBox.value()
        c.num02 = self.ui.num02SpinBox.value()
        return c

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

    def get_timeline(self):
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        timeline = project.GetCurrentTimeline()
        return timeline

    def move_to_pre_item(self, track_type: str, w: QComboBox):
        timeline = self.get_timeline()
        if timeline is None:
            return

        index = track_name2index(timeline, track_type, w.currentText())
        frame = get_currentframe(timeline)
        r = frame

        for clip in timeline.GetItemListInTrack(track_type, index):
            if clip.GetStart() < frame:
                r = clip.GetStart()
            else:
                break
            if clip.GetEnd() < frame:
                r = clip.GetEnd()
            else:
                break
        set_playhead(timeline, r)

    def move_to_next_item(self, track_type: str, w: QComboBox):
        timeline = self.get_timeline()
        if timeline is None:
            return

        index = track_name2index(timeline, track_type, w.currentText())
        frame = get_currentframe(timeline)
        r = frame

        for clip in timeline.GetItemListInTrack(track_type, index):
            if clip.GetStart() > frame:
                r = clip.GetStart()
                break
            if clip.GetEnd() > frame:
                r = clip.GetEnd()
                break
        set_playhead(timeline, r)

    def move_playhead(self, n):
        timeline = self.get_timeline()
        if timeline is None:
            return

        set_playhead(timeline, get_currentframe(timeline) + n)

    def set_start(self):
        timeline = self.get_timeline()
        if timeline is None:
            return

        set_playhead(timeline, timeline.GetStartFrame())

    def set_end(self):
        timeline = self.get_timeline()
        if timeline is None:
            return

        set_playhead(timeline, timeline.GetEndFrame())

    def update_track(self) -> None:
        v_m: QStringListModel = self.ui.videoComboBox.model()
        a_m: QStringListModel = self.ui.audioComboBox.model()
        s_m: QStringListModel = self.ui.subtitleComboBox.model()
        timeline = self.get_timeline()
        if timeline is None:
            v_m.setStringList([])
            a_m.setStringList([])
            s_m.setStringList([])
            return

        # video
        v_m.setStringList(get_track_names(timeline, 'video'))
        if v_m.rowCount() == 0:
            self.ui.videoComboBox.setEnabled(False)
            self.ui.vidioLeftButton.setEnabled(False)
            self.ui.vidioRightButton.setEnabled(False)
        else:
            self.ui.videoComboBox.setEnabled(True)
            self.ui.vidioLeftButton.setEnabled(True)
            self.ui.vidioRightButton.setEnabled(True)

        # audio
        a_m.setStringList(get_track_names(timeline, 'audio'))
        if a_m.rowCount() == 0:
            self.ui.audioComboBox.setEnabled(False)
            self.ui.audioLeftButton.setEnabled(False)
            self.ui.audioRightButton.setEnabled(False)
        else:
            self.ui.audioComboBox.setEnabled(True)
            self.ui.audioLeftButton.setEnabled(True)
            self.ui.audioRightButton.setEnabled(True)

        # subtitle
        s_m.setStringList(get_track_names(timeline, 'subtitle'))
        if s_m.rowCount() == 0:
            self.ui.subtitleComboBox.setEnabled(False)
            self.ui.subtitleLeftButton.setEnabled(False)
            self.ui.subtitleRightButton.setEnabled(False)
        else:
            self.ui.subtitleComboBox.setEnabled(True)
            self.ui.subtitleLeftButton.setEnabled(True)
            self.ui.subtitleRightButton.setEnabled(True)


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
