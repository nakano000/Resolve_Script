import time
from pathlib import Path

import dataclasses
import sys

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
    get_currentframe, COLOR_LIST,
)
from rs_resolve.tool.subtitle2text_plus.subtitle2text_plus_ui import Ui_MainWindow

APP_NAME = 'Subtitle2TextPlus'


@dataclasses.dataclass
class ConfigData(config.Data):
    wait_time: float = 0.01
    color: str = 'Blue'


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


def get_video_item(timeline, index):
    frame = get_currentframe(timeline)
    for item in timeline.GetItemListInTrack('video', index):
        if item.GetStart() <= frame < item.GetEnd():
            return item
    return None


def get_resolve_window(pj_name):
    import pygetwindow
    for t in pygetwindow.getAllTitles():
        if t.startswith('DaVinci Resolve') and t.endswith(pj_name):
            return pygetwindow.getWindowsWithTitle(t)[0]
    return None


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
        self.resize(150, 150)
        self.fusion = fusion

        # combobox
        for w in [self.ui.videoComboBox, self.ui.subtitleComboBox]:
            m = QStringListModel()
            w.setModel(m)
        m = QStringListModel(COLOR_LIST)
        self.ui.colorComboBox.setModel(m)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()


        # style sheet
        self.ui.updateButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.convertButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.updateButton.clicked.connect(self.update_track)
        self.ui.convertButton.clicked.connect(self.convert)
        self.ui.closeButton.clicked.connect(self.close)

        #
        self.update_track()
        self.ui.closeButton.setFocus()

    def convert(self) -> None:
        import pyautogui

        data = self.get_data()

        resolve = self.fusion.GetResolve()
        page = resolve.GetCurrentPage()
        if page not in ['edit', 'cut']:
            return
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            print('Projectが見付かりません。')
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            print('Timelineが見付かりません。')
            return

        v_index = track_name2index(timeline, 'video', self.ui.videoComboBox.currentText())
        s_index = track_name2index(timeline, 'subtitle', self.ui.subtitleComboBox.currentText())

        if v_index == 0 or s_index == 0:
            print('選択したトラックが見付かりません。')
            return

        v_item = get_video_item(timeline, v_index)
        if v_item is None:
            print('ビデオクリップが見付かりません。')
            return
        v_sf = v_item.GetStart()
        v_ef = v_item.GetEnd()

        subtitle_items = []
        for item in timeline.GetItemListInTrack('subtitle', s_index):
            if item.GetStart() < v_ef and v_sf < item.GetEnd():
                subtitle_items.append(item)

        w = get_resolve_window(project.GetName())
        if w is None:
            print('DaVinci ResolveのWindowが見付かりません。')
            return

        # main
        for item in subtitle_items:
            sf = max([item.GetStart(), v_sf])
            ef = min([item.GetEnd(), v_ef])
            cf = int((sf + ef) / 2)
            text = item.GetName()
            # split
            w.activate()
            pyautogui.hotkey('ctrl', 'shift', 'a')
            for n in [sf, ef]:
                timeline.SetCurrentTimecode(str(n))
                w.activate()
                pyautogui.hotkey('ctrl', 'b')
                time.sleep(data.wait_time)
            # setup
            timeline.SetCurrentTimecode(str(cf))
            time.sleep(data.wait_time / 2)
            for text_plus in timeline.GetItemListInTrack('video', v_index):
                if text_plus.GetStart() < cf < text_plus.GetEnd():
                    # set styled text
                    if text_plus.GetFusionCompCount() == 0:
                        print('FusionCompが見付かりません。')
                        break
                    comp = text_plus.GetFusionCompByIndex(1)
                    lst = comp.GetToolList(False, 'TextPlus')
                    if not lst[1]:
                        print('TextPlus Nodeが見付かりません。')
                        break
                    tool = lst[1]
                    tool.StyledText = text
                    text_plus.SetClipColor(data.color)
                    break

        # end
        print('Done!')

    def update_track(self) -> None:
        v_m: QStringListModel = self.ui.videoComboBox.model()
        s_m: QStringListModel = self.ui.subtitleComboBox.model()
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            print('Projectが見付かりません。')
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            print('Timelineが見付かりません。')
            return
        if timeline is None:
            v_m.setStringList([])
            s_m.setStringList([])
            return

        # video
        v_m.setStringList(get_track_names(timeline, 'video'))

        # subtitle
        s_m.setStringList(get_track_names(timeline, 'subtitle'))

    def set_data(self, c: ConfigData):
        self.ui.waitTimeSpinBox.setValue(c.wait_time)
        self.ui.colorComboBox.setCurrentText(c.color)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.wait_time = self.ui.waitTimeSpinBox.value()
        c.color = self.ui.colorComboBox.currentText()
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


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())
