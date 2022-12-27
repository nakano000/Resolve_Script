import re
from functools import partial

import dataclasses
import sys
import time

from pathlib import Path

from PySide2.QtCore import (
    Qt,
    Signal,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)
from PySide2.QtGui import (
    QColor,
)

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

import pyautogui
import pygetwindow

from rs.core import (
    config,
    pipe as p,
    voice_bin_process,
    util,
    chara_data,
)
from rs.core.chara_data import CharaData

from rs.gui import (
    appearance,
    log,
)

from rs_resolve.core import (
    get_currentframe,
    get_fps,
    set_currentframe,
    track_name2index
)
from rs_resolve.tool.voice_dropper.voice_dropper_ui import Ui_MainWindow

APP_NAME = 'Voice Dropper'

SCRIPT_DIR: Path = config.ROOT_PATH.joinpath('data', 'app', 'VoiceDropper')


def get_resolve_window(pj_name):
    for t in pygetwindow.getAllTitles():
        if t.startswith('DaVinci Resolve') and t.endswith(pj_name):
            return pygetwindow.getWindowsWithTitle(t)[0]
    return None


def get_window(name):
    for t in pygetwindow.getAllTitles():
        if t == name:
            return pygetwindow.getWindowsWithTitle(t)[0]
    return None


def get_video_item(timeline, index):
    frame = get_currentframe(timeline)
    for item in timeline.GetItemListInTrack('video', index):
        if item.GetStart() <= frame < item.GetEnd():
            return item
    return None


@dataclasses.dataclass
class ConfigData(config.Data):
    voice_dir: str = ''

    wait_time: float = 0.001
    offset: int = 15
    video_index: int = 1
    audio_index: int = 1
    make_script: bool = True
    use_chara: bool = True


class WatchdogEvent(FileSystemEventHandler):
    def __init__(self, sig):
        super(WatchdogEvent, self).__init__()
        self.modified: Signal = sig
        self.created_lst = []

    def on_created(self, event):
        src_path = Path(event.src_path)
        # print('created', src_path)
        if src_path.suffix.lower() in ['.wav', ]:
            self.created_lst.append(str(src_path))

    def on_modified(self, event):
        src_path = Path(event.src_path)
        # print('modified', src_path)
        if src_path.is_dir():
            if len(self.created_lst) > 0:
                self.modified.emit(str(src_path), self.created_lst.copy())
                self.created_lst.clear()


class MainWindow(QMainWindow):
    modified = Signal(str, list)

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
        self.resize(450, 650)
        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        self.script_base: str = SCRIPT_DIR.joinpath('script_base.lua').read_text(encoding='utf-8')

        # watcher
        self.modified.connect(self.directory_changed, Qt.QueuedConnection)
        self.__observer = PollingObserver()

        # style sheet
        self.ui.startButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.stopButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.importButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.startButton.clicked.connect(self.start)
        self.ui.stopButton.clicked.connect(self.stop)

        self.ui.importButton.clicked.connect(self.import_wave)
        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.voiceDirLineEdit.textChanged.connect(self.start)
        self.ui.voiceDirToolButton.clicked.connect(self.voiceDirToolButton_clicked)
        #
        self.make_dropper_folder()
        self.ui.closeButton.setFocus()
        self.start()

    def import_wave(self) -> None:
        data = self.get_data()
        filenames = QFileDialog.getOpenFileNames(
            self,
            'Open File',
            data.voice_dir,
            'Wave File (*.wav);;All File (*.*)'
        )[0]

        self.ui.logTextEdit.clear()
        self.directory_changed(data.voice_dir, filenames)

    def set_status_label(self):
        w = self.ui.statusLabel
        if self.__observer.is_alive():
            w.setText(' 監視中 ')
            w.setStyleSheet('color: white; background-color: green;')
        else:
            w.setText(' 停止中 ')
            w.setStyleSheet('')

    def start(self):
        data = self.get_data()
        if data.voice_dir == '':
            return
        path = Path(data.voice_dir)
        if path.is_dir():
            self.stop()
            self.__observer = PollingObserver()
            self.__observer.schedule(WatchdogEvent(self.modified), str(path), True)
            self.__observer.start()
        self.set_status_label()

    def stop(self):
        if self.__observer.is_alive():
            self.__observer.stop()
            self.__observer.join()
        self.set_status_label()

    def make_dropper_folder(self):
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            return
        media_pool = project.GetMediaPool()
        root_folder = media_pool.GetRootFolder()
        for folder in root_folder.GetSubFolderList():
            if folder.GetName() == 'VoiceDropper':
                return
        media_pool.AddSubFolder(root_folder, 'VoiceDropper')

    def directory_changed(self, s, created_lst):
        self.ui.logTextEdit.clear()
        if len(created_lst) == 0:
            return
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Projectが見付かりません。')
            return
        media_pool = project.GetMediaPool()
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timelineが見付かりません。')
            return

        w = get_resolve_window(project.GetName())
        if w is None:
            self.add2log('DaVinci ResolveのWindowが見付かりません。')
            return
        if util.IS_WIN:
            self.setWindowState(Qt.WindowMinimized)  # windowsの場合、最小化しないとウィンドウがactiveにならないので、
            self.setWindowState(Qt.WindowActive)  # 最小化してからactiveにする

        root_folder = media_pool.GetRootFolder()
        dropper_folder = None
        voice_folder = None
        for folder in root_folder.GetSubFolderList():
            if folder.GetName() == 'VoiceDropper':
                dropper_folder = folder
            if folder.GetName() == 'Voice':
                voice_folder = folder
        if voice_folder is None:
            voice_folder = media_pool.AddSubFolder(root_folder, "Voice")
        media_pool.SetCurrentFolder(voice_folder)

        if dropper_folder is None:
            self.add2log('MediaPool VoiceDropperフォルダにtext+が見付かりません。')
            return
        if len(dropper_folder.GetClipList()) == 0:
            self.add2log('MediaPool VoiceDropperフォルダにtext+が見付かりません。')
            return
        text_template = dropper_folder.GetClipList()[0]

        # get data
        data = self.get_data()
        fps = get_fps(timeline)

        # util
        def send_hotkey(key_list):
            w.activate()
            pyautogui.hotkey(*key_list)
            time.sleep(data.wait_time)

        def select_audio_track(index):
            if timeline.GetTrackCount('audio') == 1:
                send_hotkey(['ctrl', 'alt', str(index)])
            elif index == 1:
                send_hotkey(['ctrl', 'alt', '2'])
            else:
                send_hotkey(['ctrl', 'alt', '1'])
            send_hotkey(['ctrl', 'alt', str(index)])

        def select_video_track(index):
            if timeline.GetTrackCount('video') == 1:
                send_hotkey(['alt', str(index)])
            elif index == 1:
                send_hotkey(['alt', '2'])
            else:
                send_hotkey(['alt', '1'])
            send_hotkey(['alt', str(index)])

        # main
        for f in p.pipe(
                created_lst,
                p.map(lambda x: Path(x).parent.joinpath(Path(x).stem + '.wav')),
                p.filter(p.call.is_file()),
                dict.fromkeys,
                list,
                sorted,
        ):
            f: Path
            QApplication.processEvents()
            self.add2log('処理中: %s' % f.name)
            current_frame = get_currentframe(timeline)
            work_frame = timeline.GetEndFrame() + 30

            # キャラクター設定
            ch_data = CharaData()
            for cd in chara_data.get_chara_list():
                cd: CharaData
                m = re.fullmatch(cd.reg_exp, f.stem)
                if m is not None:
                    ch_data = cd
                    break

            audio_index = (
                track_name2index(timeline, 'audio', ch_data.track_name + '_a')
                if data.use_chara else
                data.audio_index
            )
            video_index = (
                track_name2index(timeline, 'video', ch_data.track_name + '_t')
                if data.use_chara else
                data.video_index
            )
            if audio_index < 1 or audio_index > 8:
                self.add2log(f'音声トラック名 {ch_data.track_name}_a が1〜8の範囲で見付かりません。')
                self.add2log(f'音声トラック {data.audio_index} を使います。')
                audio_index = data.audio_index
            if video_index < 1 or video_index > 8:
                self.add2log(f'ビデオトラック名 {ch_data.track_name}_t が1〜8の範囲で見付かりません。')
                self.add2log(f'ビデオトラック {data.video_index} を使います。')
                video_index = data.video_index

            txt_file = f.parent.joinpath(f.stem + '.txt')
            t = util.str2lines(
                voice_bin_process.read_text(txt_file, ch_data.c_code),
                ch_data.str_width * 2,
            ) if txt_file.is_file() else ''

            lua_script = '\n'.join([
                self.script_base,
                'setJimaku(',
                f'    [[{t}]],',
                f'    "{ch_data.color}",',
                f'    {video_index},',
                f'    {audio_index},',
                f'    {current_frame},',
                f'    [[{str(ch_data.setting_file)}]]',
                ')',
            ])

            # import
            mi = media_pool.ImportMedia(str(f))[0]

            # 音声クリップの仮挿入
            clip = media_pool.AppendToTimeline([{'mediaPoolItem': mi}])[0]
            duration = clip.GetDuration()
            send_hotkey(['ctrl', 'z'])
            set_currentframe(timeline, current_frame)
            # 音声トラックの選択
            select_audio_track(audio_index)
            # 音声クリップの挿入
            clip = media_pool.AppendToTimeline([{'mediaPoolItem': mi}])[0]
            set_currentframe(timeline, clip.GetStart())
            send_hotkey(['y'])
            # 音声クリップの移動 work
            send_hotkey(['ctrl', 'x'])
            # send_hotkey(['ctrl', 'z'])
            set_currentframe(timeline, work_frame)
            send_hotkey(['ctrl', 'v'])
            # 音声トラックの選択解除
            send_hotkey(['ctrl', 'alt', str(audio_index)])
            # text+クリップの仮挿入
            media_pool.AppendToTimeline([{'mediaPoolItem': text_template}])
            send_hotkey(['ctrl', 'z'])
            # videoトラックの選択
            select_video_track(video_index)
            # text+クリップの挿入
            text_plus = media_pool.AppendToTimeline([{
                'mediaPoolItem': text_template,
                'startFrame': 0,
                'endFrame': duration - 1,  # 1フレーム短くする (start 0 end 0 で 尺は1フレーム)
                'mediaType': 1,
            }])[0]
            set_currentframe(timeline, text_plus.GetStart())
            send_hotkey(['y'])
            # text+クリップの移動 work
            send_hotkey(['ctrl', 'x'])
            set_currentframe(timeline, work_frame)
            send_hotkey(['ctrl', 'v'])
            # クリップの移動 current
            set_currentframe(timeline, work_frame)
            send_hotkey(['alt', 'y'])
            send_hotkey(['ctrl', 'x'])
            set_currentframe(timeline, current_frame)
            send_hotkey(['ctrl', 'v'])
            # クリップのリンク
            send_hotkey(['ctrl', 'alt', 'l'])
            # 音声トラックの選択をリセットするために、適当な物を追加しUndo
            set_currentframe(timeline, work_frame + duration)
            timeline.InsertGeneratorIntoTimeline('Solid Color')
            send_hotkey(['ctrl', 'z'])
            # クリップにスクリプトを実行
            self.fusion.Execute(lua_script)
            # 再生ヘッドの移動
            set_currentframe(timeline, current_frame + duration + data.offset)
            #
            self.add2log('Import: ' + str(f))
            #
            if data.make_script:
                voice_bin_process.run(Path(f), fps)
                self.add2log('Make Script')
            #
            self.add2log('')
        # end
        self.add2log('Done!')

    def voiceDirToolButton_clicked(self) -> None:
        w = self.ui.voiceDirLineEdit
        path = QFileDialog.getExistingDirectory(
            self,
            'Select Directory',
            w.text(),
        )
        if path != '':
            w.setText(path)

    def set_data(self, c: ConfigData):
        self.ui.voiceDirLineEdit.setText(c.voice_dir)

        self.ui.waitTimeSpinBox.setValue(c.wait_time)
        self.ui.offsetSpinBox.setValue(c.offset)
        self.ui.videoIndexSpinBox.setValue(c.video_index)
        self.ui.audioIndexSpinBox.setValue(c.audio_index)
        self.ui.makeScriptCheckBox.setChecked(c.make_script)
        self.ui.useCharaCheckBox.setChecked(c.use_chara)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.voice_dir = self.ui.voiceDirLineEdit.text().strip()

        c.wait_time = self.ui.waitTimeSpinBox.value()
        c.offset = self.ui.offsetSpinBox.value()
        c.video_index = self.ui.videoIndexSpinBox.value()
        c.audio_index = self.ui.audioIndexSpinBox.value()
        c.make_script = self.ui.makeScriptCheckBox.isChecked()
        c.use_chara = self.ui.useCharaCheckBox.isChecked()
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


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())
