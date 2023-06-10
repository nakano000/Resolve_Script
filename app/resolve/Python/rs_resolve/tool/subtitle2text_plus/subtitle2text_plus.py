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
    lang,
)
from rs.gui import (
    appearance,
)

from rs_resolve.core import (
    get_currentframe,
    LockOtherTrack,
    shortcut,
)
from rs_resolve.gui.shortcut.shortcut_window import MainWindow as ShortcutWindow
from rs_resolve.tool.subtitle2text_plus.subtitle2text_plus_ui import Ui_MainWindow

APP_NAME = 'Subtitle2TextPlus'


@dataclasses.dataclass
class ConfigData(config.Data):
    wait_time: float = 0.01
    color: str = 'Blue'
    use_auto_lock: bool = True


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

        # translate
        self.lang_code: lang.Code = lang.load()
        self.translate()

        # combobox
        for w in [self.ui.videoComboBox, self.ui.subtitleComboBox]:
            m = QStringListModel()
            w.setModel(m)
        m = QStringListModel(config.COLOR_LIST)
        self.ui.colorComboBox.setModel(m)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # window
        self.shortcut_window = ShortcutWindow(self, self.fusion)

        # style sheet
        self.ui.shortcutButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.updateButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.convertButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.shortcutButton.clicked.connect(self.shortcut_window.show)
        self.ui.updateButton.clicked.connect(self.update_track)
        self.ui.convertButton.clicked.connect(self.convert)
        self.ui.closeButton.clicked.connect(self.close)

        #
        self.update_track()
        self.ui.closeButton.setFocus()

    def translate(self) -> None:
        if self.lang_code == lang.Code.en:
            self.ui.settingGroupBox.setTitle('Setting')
            self.ui.trackGroupBox.setTitle('Track')
            self.ui.clipCplorLabel.setText('Clip Color')
            self.ui.waitLabel.setText('Wait Time')

    def get_text_plus(self, item):
        if item.GetFusionCompCount() == 0:
            print(
                'FusionComp not found.'
                if self.lang_code == lang.Code.en else
                'FusionCompが見付かりません。'
            )
            return
        comp = item.GetFusionCompByIndex(1)
        lst = comp.GetToolList(False, 'TextPlus')
        if not lst[1]:
            print(
                'TextPlus Node not found.'
                if self.lang_code == lang.Code.en else
                'TextPlus Nodeが見付かりません。'
            )
            return
        return lst[1]

    def convert(self) -> None:
        data = self.get_data()

        resolve = self.fusion.GetResolve()
        page = resolve.GetCurrentPage()
        if page not in ['edit', 'cut']:
            return
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            print(
                'Project not found.'
                if self.lang_code == lang.Code.en else
                'Projectが見付かりません。'
            )
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            print(
                'Timeline not found.'
                if self.lang_code == lang.Code.en else
                'Timelineが見付かりません。'
            )
            return

        v_index = track_name2index(timeline, 'video', self.ui.videoComboBox.currentText())
        s_index = track_name2index(timeline, 'subtitle', self.ui.subtitleComboBox.currentText())

        if v_index == 0 or s_index == 0:
            print(
                'Track not found.'
                if self.lang_code == lang.Code.en else
                '選択したトラックが見付かりません。'
            )
            return

        v_item = get_video_item(timeline, v_index)
        if v_item is None:
            print(
                'Video clip not found.'
                if self.lang_code == lang.Code.en else
                'ビデオクリップが見付かりません。'
            )
            return
        v_sf = v_item.GetStart()
        v_ef = v_item.GetEnd()

        subtitle_items = []
        for item in timeline.GetItemListInTrack('subtitle', s_index):
            if item.GetStart() < v_ef and v_sf < item.GetEnd():
                subtitle_items.append(item)

        w = get_resolve_window(project.GetName())
        if w is None:
            print(
                'DaVinci Resolve window not found.'
                if self.lang_code == lang.Code.en else
                'DaVinci ResolveのWindowが見付かりません。'
            )
            return

        # clear text+
        _node = self.get_text_plus(v_item)
        if _node is None:
            return
        _node.StyledText = ''

        with LockOtherTrack(timeline, v_index, track_type='video', enable=data.use_auto_lock):
            sc = shortcut.Data()
            if shortcut.CONFIG_FILE.is_file():
                sc.load(shortcut.CONFIG_FILE)

            # main
            for item in subtitle_items:
                sf = max([item.GetStart(), v_sf])
                ef = min([item.GetEnd(), v_ef])
                cf = int((sf + ef) / 2)
                text = item.GetName()
                # split
                w.activate()
                sc.active_timeline_panel()
                sc.deselect_all()
                for n in [sf, ef]:
                    timeline.SetCurrentTimecode(str(n))
                    w.activate()
                    sc.razor()
                    time.sleep(data.wait_time)
                # setup
                timeline.SetCurrentTimecode(str(cf))
                time.sleep(data.wait_time / 2)
                for clip in timeline.GetItemListInTrack('video', v_index):
                    if clip.GetStart() < cf < clip.GetEnd():
                        # set styled text
                        tool = self.get_text_plus(clip)
                        if tool is None:
                            break
                        tool.StyledText = text
                        clip.SetClipColor(data.color)
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
            print(
                'Project not found.'
                if self.lang_code == lang.Code.en else
                'Projectが見付かりません。'
            )
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            print(
                'Timeline not found.'
                if self.lang_code == lang.Code.en else
                'Timelineが見付かりません。'
            )
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
        self.ui.autoLockCheckBox.setChecked(c.use_auto_lock)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.wait_time = self.ui.waitTimeSpinBox.value()
        c.color = self.ui.colorComboBox.currentText()
        c.use_auto_lock = self.ui.autoLockCheckBox.isChecked()
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
