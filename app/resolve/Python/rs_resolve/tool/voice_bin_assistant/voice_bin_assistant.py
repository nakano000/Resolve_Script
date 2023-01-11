from functools import partial

import dataclasses
import sys
import time

from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QStringListModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)
from PySide2.QtGui import (
    QColor,
)

from rs.core import (
    config,
    pipe as p,
    voice_bin_process,
)
from rs.gui import (
    appearance,
    log,
)

from rs_resolve.core import (
    get_currentframe,
    get_fps,
    track_name2index,
)
from rs_resolve.tool.voice_bin_assistant.voice_bin_assistant_ui import Ui_MainWindow

APP_NAME = 'VoiceBinアシスタント'


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


def get_video_item(timeline, index):
    frame = get_currentframe(timeline)
    for item in timeline.GetItemListInTrack('video', index):
        if item.GetStart() <= frame < item.GetEnd():
            return item
    return None


def get_text(item) -> str:
    if item.GetFusionCompCount() == 0:
        return ''
    comp = item.GetFusionCompByIndex(1)
    lst = comp.GetToolList(False, 'TextPlus')

    if len(lst) == 0:
        return ''
    return lst[1].GetInput('StyledText')


@dataclasses.dataclass
class ConfigData(config.Data):
    import_wait: float = 0.1
    wave_offset: int = 15
    refer_track: bool = False

    tatie_wait: float = 2.0
    rebuild_script: bool = True


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
        self.resize(380, 700)
        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # list
        for w in [self.ui.videoListView, self.ui.audioListView]:
            m = QStringListModel()
            w.setModel(m)

        # style sheet
        self.ui.importButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.textPlusButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.tatieButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.textPlusTatieButton.setStyleSheet(appearance.in_stylesheet)

        self.ui.copyTextButton.setStyleSheet(appearance.ex_stylesheet)

        # event
        self.ui.importButton.clicked.connect(self.import_wave)
        self.ui.textPlusButton.clicked.connect(partial(self.split_and_setup, True, False))
        self.ui.tatieButton.clicked.connect(partial(self.split_and_setup, False, True))
        self.ui.textPlusTatieButton.clicked.connect(partial(self.split_and_setup, True, True))
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.updateTrackButton.clicked.connect(self.update_track)
        self.ui.copyTextButton.clicked.connect(self.copy_text)

        #
        self.ui.closeButton.setFocus()
        self.update_track()

    def set_data(self, c: ConfigData):
        self.ui.importWaitSpinBox.setValue(c.import_wait)
        self.ui.offsetSpinBox.setValue(c.wave_offset)
        self.ui.referTrackCheckBox.setChecked(c.refer_track)

        self.ui.tatieWaitSpinBox.setValue(c.tatie_wait)
        self.ui.rebuildCheckBox.setChecked(c.rebuild_script)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.import_wait = self.ui.importWaitSpinBox.value()
        c.wave_offset = self.ui.offsetSpinBox.value()
        c.refer_track = self.ui.referTrackCheckBox.isChecked()

        c.tatie_wait = self.ui.tatieWaitSpinBox.value()
        c.rebuild_script = self.ui.rebuildCheckBox.isChecked()
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

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)

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

    def copy_text(self):
        self.ui.logTextEdit.clear()

        # get data
        resolve = self.fusion.GetResolve()
        page = resolve.GetCurrentPage()
        if page not in ['edit', 'cut']:
            return
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Projectが見付かりません。')
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timelineが見付かりません。')
            return

        index = get_index(timeline, 'video', self.ui.videoListView)

        if index == 0:
            self.add2log('選択したトラックが見付かりません。')
            return

        # text
        frame = get_currentframe(timeline)
        text = p.pipe(
            timeline.GetItemListInTrack('video', index),
            p.filter(lambda i: frame <= i.GetStart()),
            p.map(get_text),
            p.map(p.call.replace('\n', '')),
            list,
            '\n'.join,
        )

        # copy
        QApplication.clipboard().setText(text)
        self.add2log(text)

    def import_wave(self) -> None:
        import pyautogui
        from collections import deque
        filenames = QFileDialog.getOpenFileNames(
            self,
            'Open File',
            None,
            'Wave File (*.wav);;All File (*.*)'
        )[0]

        self.ui.logTextEdit.clear()

        # get data
        resolve = self.fusion.GetResolve()
        page = resolve.GetCurrentPage()
        if page not in ['edit', 'cut']:
            return
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Projectが見付かりません。')
            return
        mediapool = project.GetMediaPool()
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timelineが見付かりません。')
            return

        w = get_resolve_window(project.GetName())
        if w is None:
            self.add2log('DaVinci ResolveのWindowが見付かりません。')
            return

        data = self.get_data()

        # Queue
        que = deque()
        if data.refer_track:
            index = get_index(timeline, 'video', self.ui.videoListView)
            if index == 0:
                self.add2log('選択したトラックが見付かりません。')
                return
            frame = get_currentframe(timeline)
            p.pipe(
                timeline.GetItemListInTrack('video', index),
                p.filter(lambda i: frame <= i.GetStart()),
                p.iter(lambda i: que.append(i.GetStart())),
            )
            timeline.SetCurrentTimecode(str(que.popleft()))

        # main
        for f in filenames:

            # import
            pool_item = mediapool.ImportMedia([f])[0]
            if pool_item.GetClipProperty('Usage') == '0':
                mediapool.DeleteClips([pool_item])  # Media Poolで選択状態にするため、削除して読み直す。
                mediapool.ImportMedia([f])[0]
                w.activate()
                pyautogui.hotkey('f10')
                time.sleep(data.import_wait)
                if len(que) == 0:
                    frame = get_currentframe(timeline)
                    timeline.SetCurrentTimecode(str(frame + data.wave_offset))
                else:
                    timeline.SetCurrentTimecode(str(que.popleft()))
                self.add2log('Import: ' + str(f))
            else:
                self.add2log('すでに使われています。スキップします。: ' + str(f))

        # end
        self.add2log('Done!')

    def split_and_setup(self, use_text_plus: bool, use_tatie: bool) -> None:
        import pyautogui
        self.ui.logTextEdit.clear()

        # get data
        resolve = self.fusion.GetResolve()
        page = resolve.GetCurrentPage()
        if page not in ['edit', 'cut']:
            return
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Projectが見付かりません。')
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timelineが見付かりません。')
            return

        fps = get_fps(timeline)
        v_index = get_index(timeline, 'video', self.ui.videoListView)
        a_index = get_index(timeline, 'audio', self.ui.audioListView)

        if v_index == 0 or a_index == 0:
            self.add2log('選択したトラックが見付かりません。')
            return

        v_item = get_video_item(timeline, v_index)
        if v_item is None:
            self.add2log('ビデオクリップが見付かりません。')
            return
        v_sf = v_item.GetStart()
        v_ef = v_item.GetEnd()

        audio_items = []
        for item in timeline.GetItemListInTrack('audio', a_index):
            if item.GetStart() < v_ef and v_sf < item.GetEnd():
                audio_items.append(item)

        w = get_resolve_window(project.GetName())
        if w is None:
            self.add2log('DaVinci ResolveのWindowが見付かりません。')
            return

        data = self.get_data()

        # main
        cmd_dir: Path = config.CONFIG_DIR.joinpath('VoiceBin', 'Scripts')
        cmd_dir.mkdir(parents=True, exist_ok=True)
        for item in audio_items:
            sf = max([item.GetStart(), v_sf])
            ef = min([item.GetEnd(), v_ef])
            cf = int((sf + ef) / 2)
            f = Path(item.GetMediaPoolItem().GetClipProperty('File Path'))
            # make script
            if data.rebuild_script:
                voice_bin_process.del_script(f)
            voice_bin_process.run(f, fps)

            text_lua = f.parent.joinpath(f.stem + '.lua')
            tatie_lua = f.parent.joinpath(f.stem + '.tatie.lua')
            # split
            self.add2log(f.stem)
            w.activate()
            pyautogui.hotkey('ctrl', 'shift', 'a')
            for n in [sf, ef]:
                timeline.SetCurrentTimecode(str(n))
                w.activate()
                pyautogui.hotkey('ctrl', 'b')
                time.sleep(data.tatie_wait)
            # setup
            timeline.SetCurrentTimecode(str(cf))
            if use_text_plus and text_lua.is_file():
                self.fusion.Execute(text_lua.read_text(encoding='utf-8'))
            if use_tatie and tatie_lua.is_file():
                self.fusion.Execute(tatie_lua.read_text(encoding='utf-8'))
            time.sleep(data.tatie_wait / 2.0)

        # end
        self.add2log('Done!')


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())
