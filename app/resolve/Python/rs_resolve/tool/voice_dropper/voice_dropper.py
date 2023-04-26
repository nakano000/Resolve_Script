import os
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
    util,
    chara_data,
    txt,
)
from rs.core.chara_data import CharaData
from rs.gui.chara.chara import MainWindow as CharaWindow

from rs.gui import (
    appearance,
    log,
)

from rs_fusion.core import ordered_dict_to_dict
from rs_resolve.core import (
    get_currentframe,
    set_currentframe,
    get_fps,
    track_name2index,
    get_item,
)

from rs_resolve.tool.voice_dropper.voice_dropper_ui import Ui_MainWindow
from rs_resolve.tool.voice_dropper.lip_sync_window import MainWindow as LipSyncWindow

APP_NAME = 'Voice Dropper'

SCRIPT_DIR: Path = config.ROOT_PATH.joinpath('data', 'app', 'VoiceDropper')


def get_resolve_window(pj_name):
    for t in pygetwindow.getAllTitles():
        if t.startswith('DaVinci Resolve') and t.endswith(pj_name):
            return pygetwindow.getWindowsWithTitle(t)[0]
    return None


@dataclasses.dataclass
class ConfigData(config.Data):
    voice_dir: str = ''

    wait_time: float = 0.015
    time_out: int = 15
    offset: int = 15
    extend: int = 0
    video_index: int = 1
    audio_index: int = 1
    make_text: bool = False
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
            self.created_lst.append(src_path)

    def on_modified(self, event):
        src_path = Path(event.src_path)
        # print('modified', src_path)
        if src_path.is_dir():
            if len(self.created_lst) > 0:
                self.modified.emit(self.created_lst.copy())
                self.created_lst.clear()


class MainWindow(QMainWindow):
    modified = Signal(list)

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

        tmp_dir = config.CONFIG_DIR.joinpath('tmp')
        tmp_dir.mkdir(parents=True, exist_ok=True)
        self.temp_file: Path = tmp_dir.joinpath('timeline.xml')

        self.xml = config.DATA_PATH.joinpath('app', 'VoiceDropper', 'Timeline.xml').read_text(encoding='utf-8')

        self.script_base: str = SCRIPT_DIR.joinpath('script_base.lua').read_text(encoding='utf-8')

        # window
        self.chara_window = CharaWindow(self)
        self.lip_sync_window = LipSyncWindow(self, self.fusion)

        # watcher
        self.modified.connect(self.directory_changed, Qt.QueuedConnection)
        self.__observer = PollingObserver()

        # style sheet
        self.ui.startButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.stopButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.importButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.lipSyncButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.charaButton.setStyleSheet(appearance.ex_stylesheet)

        # event
        self.ui.charaButton.clicked.connect(self.chara_window.show)

        self.ui.startButton.clicked.connect(self.start)
        self.ui.stopButton.clicked.connect(self.stop)

        self.ui.importButton.clicked.connect(self.import_wave)
        self.ui.lipSyncButton.clicked.connect(self.lip_sync_window.show)
        self.lip_sync_window.ui.applyButton.clicked.connect(self.lip_sync)

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
        self.directory_changed(
            p.pipe(
                filenames,
                p.map(Path),
                list
            )
        )

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

    def directory_changed(self, created_lst):
        use_watchdog = self.__observer.is_alive()
        if use_watchdog:
            self.stop()

        self.voice_drop(created_lst)

        if use_watchdog:
            self.start()

    def setup_track(self, timeline, video_index, audio_index):
        video_size = timeline.GetTrackCount('video')
        audio_size = timeline.GetTrackCount('audio')
        if video_index > video_size:
            for i in range(video_index - video_size):
                timeline.AddTrack('video')
        if audio_index > audio_size:
            for i in range(audio_index - audio_size):
                timeline.AddTrack('audio', 'stereo')

    def voice_drop(self, created_lst):
        time_sta = time.time()
        self.ui.logTextEdit.clear()
        if len(created_lst) == 0:
            return
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Projectが見付かりません。')
        media_pool = project.GetMediaPool()
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timelineが見付かりません。')
            return

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

        # main
        resolve.OpenPage('edit')
        for f in p.pipe(
                created_lst,
                p.filter(p.call.is_file()),
                dict.fromkeys,
                list,
                sorted,
        ):
            f: Path
            QApplication.processEvents()
            self.add2log('Start: %s' % f.name)
            current_frame = get_currentframe(timeline)

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
            self.setup_track(timeline, video_index, audio_index)
            if get_item(timeline, 'video', video_index, current_frame) is not None:
                self.add2log('Videoトラックに既にアイテムが存在します。')
                return
            if get_item(timeline, 'audio', audio_index, current_frame) is not None:
                self.add2log('Audioトラックに既にアイテムが存在します。')
                return

            # time out 設定
            step = 0.2
            start_time = time.time()
            is_time_out = False

            # ロック確認 VOICEPEAK用に出力待ち
            self.add2log('waveファイルチェック:  START')
            while True:
                if time.time() - start_time > data.time_out:
                    is_time_out = True
                    break
                try:
                    os.rename(str(f), str(f))
                    break
                except OSError:
                    time.sleep(step)

            if is_time_out:
                self.add2log('タイムアウト:ファイルが計算中ため、処理をスキップします。')
                continue
            self.add2log('waveファイルチェック:  OK')

            # import
            mi = None
            mi_list = media_pool.ImportMedia(str(f))
            while True:
                if time.time() - start_time > data.time_out:
                    is_time_out = True
                    break
                if len(mi_list) > 0:
                    mi = mi_list[0]
                    break
                else:
                    time.sleep(step)
                    mi_list = media_pool.ImportMedia(str(f))

            if is_time_out:
                self.add2log('タイムアウト:音声ファイルのインポートに失敗しました。')
                continue
            self.add2log('Insert Audio Clip: Start')

            # 音声クリップの挿入
            audio_info = {
                "mediaPoolItem": mi,
                "trackIndex": audio_index,
                "recordFrame": current_frame,
            }
            _audio_track_cnt = len(timeline.GetItemListInTrack('audio', audio_index))
            clip = media_pool.AppendToTimeline([audio_info])[0]
            time.sleep(data.wait_time)
            while True:
                if time.time() - start_time > data.time_out:
                    is_time_out = True
                    break
                time.sleep(step)
                if len(timeline.GetItemListInTrack('audio', audio_index)) == _audio_track_cnt:
                    mi.ReplaceClip(str(f))
                    clip = media_pool.AppendToTimeline([audio_info])[0]
                else:
                    break

            if is_time_out:
                self.add2log('タイムアウト:音声クリップの挿入に失敗しました。')
                continue
            duration = clip.GetDuration()
            self.add2log('Insert Audio Clip: Done')

            self.add2log('Insert Text Clip: Start')

            text_plus = media_pool.AppendToTimeline([{
                'mediaPoolItem': text_template,
                'startFrame': 0,
                'endFrame': duration - 1 + data.extend,  # 1フレーム短くする (start 0 end 0 で 尺は1フレーム)
                'trackIndex': video_index,
                'mediaType': 1,
                'recordFrame': current_frame,
            }])[0]
            if text_plus is None:
                self.add2log('Insert Text Clip: Failed')
                continue
            self.add2log('Insert Text Clip: Done')

            self.add2log('Text Setup : Start')
            # text+用のテキストを読み込み
            txt_file = f.parent.joinpath(f.stem + '.txt')
            if not txt_file.is_file() and data.make_text:
                self.add2log('テキストファイルを作成します。')
                txt_file.write_text(QApplication.clipboard().text(), encoding='utf-8-sig')
            t = util.str2lines(
                txt.read(txt_file, ch_data.c_code),
                ch_data.str_width * 2,
            ) if txt_file.is_file() else ''
            # comp
            if text_plus.GetFusionCompCount() == 0:
                self.add2log('FusionCompが見付かりません。')
                continue
            comp = text_plus.GetFusionCompByIndex(1)

            # tool
            lst = list(comp.GetToolList(False, 'TextPlus').values())
            if len(lst) == 0:
                self.add2log('Text+が見付かりません。')
                continue
            tool = lst[0]

            # settings
            st = ordered_dict_to_dict(bmd.readfile(str(ch_data.setting_file)))
            if st is None:
                self.add2log('settingファイルの読み込みに失敗しました。')
                continue

            # apply
            comp.StartUndo('RS Jimaku')
            comp.Lock()
            tool.LoadSettings(st)
            tool.StyledText = t
            tool.UseFrameFormatSettings = 0
            tool.Width = int(timeline.GetSetting('timelineResolutionWidth'))
            tool.Height = int(timeline.GetSetting('timelineResolutionHeight'))
            comp.Unlock()
            comp.EndUndo(True)

            if ch_data.color in config.COLOR_LIST:
                text_plus.SetClipColor(ch_data.color)
                clip.SetClipColor(ch_data.color)
            self.add2log('Text Setup: Done')
            # リンク
            timeline.SetClipsLinked([text_plus, clip], True)

            set_currentframe(timeline, current_frame + duration + data.offset + data.extend)

            self.add2log('Import: ' + str(f))

            #
            self.add2log('')
        # end
        time_end = time.time()
        self.add2log('Done! %fs' % (time_end - time_sta))

    def lip_sync(self):
        self.ui.logTextEdit.clear()

        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Projectが見付かりません。')
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timelineが見付かりません。')
            return

        fps = get_fps(timeline)
        v_index = self.lip_sync_window.get_video_track_index(timeline)
        a_index = self.lip_sync_window.get_audio_track_index(timeline)

        if v_index == 0 or a_index == 0:
            self.add2log('選択したトラックが見付かりません。')
            return

        v_item = get_item(timeline, 'video', v_index)
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
        if util.IS_WIN:
            self.setWindowState(Qt.WindowMinimized)  # windowsの場合、最小化しないとウィンドウがactiveにならないので、
            self.setWindowState(Qt.WindowActive)  # 最小化してからactiveにする

        # main
        self.add2log('Start')
        # config
        from rs.core import lab

        tatie_wait = self.lip_sync_window.get_data().wait

        setting_base: str = config.ROOT_PATH.joinpath(
            'data', 'app', 'VoiceDropper', 'setting_base.txt'
        ).read_text(encoding='utf-8')
        for item in audio_items:
            sf = max([item.GetStart(), v_sf])
            ef = min([item.GetEnd(), v_ef])
            cf = int((sf + ef) / 2)
            f = Path(item.GetMediaPoolItem().GetClipProperty('File Path'))
            lab_file = f.parent.joinpath(f.stem + '.lab')
            self.add2log('wav: ' + str(f))

            # キャラクター設定
            ch_data = CharaData()
            for cd in chara_data.get_chara_list():
                cd: CharaData
                m = re.fullmatch(cd.reg_exp, f.stem)
                if m is not None:
                    ch_data = cd
                    break

            # split
            self.add2log('Cut Clip: Start')
            w.activate()
            pyautogui.hotkey('ctrl', '4')
            pyautogui.hotkey('ctrl', 'shift', 'a')
            for n in [sf, ef]:
                timeline.SetCurrentTimecode(str(n))
                w.activate()
                pyautogui.hotkey('ctrl', 'b')
                time.sleep(tatie_wait)
            self.add2log('Cut Clip: Done')

            # get Macro Tool
            tatie_clip = get_item(timeline, 'video', v_index, cf)
            if tatie_clip is None:
                self.add2log('立ち絵ビデオクリップが見付かりません。')
                continue
            if tatie_clip.GetFusionCompCount() == 0:
                self.add2log('Fusion Compが見付かりません。')
                continue
            comp = tatie_clip.GetFusionCompByIndex(1)
            tools = p.pipe(
                comp.GetToolList(False).values(),
                p.filter(lambda x: x.ID in ['MacroOperator', 'GroupOperator']),
                p.filter(lambda x: x.ParentTool is None),
                list,
            )
            if len(tools) == 0:
                self.add2log('MacroまたはGroupが見付かりません。')
                continue
            tool = tools[0]

            # get anim
            self.add2log('Load Anim: Start')
            anim = ''
            offset = comp.GetAttrs()['COMPN_GlobalStart']
            if ch_data.anim_type.strip().lower() == 'open':
                anim = lab.wav2anim(f, fps, offset)
            elif lab_file.is_file():
                anim = lab.lab2anim(lab_file, fps, ch_data.anim_type.strip().lower(), offset)

            st = ordered_dict_to_dict(bmd.readstring(setting_base % (
                ch_data.anim_parameter,
                ch_data.anim_parameter,
                ch_data.anim_parameter,
                anim,
            )))
            if st is None:
                self.add2log('アニメーションの読み込みに失敗しました。')
                continue
            self.add2log('Load Anim: Done')

            # get anim tool list
            tool_list = [tool]
            for v in tool.SaveSettings()['Tools'][tool.Name]['Inputs'].values():
                if isinstance(v, dict) and '__ctor' in v.keys():
                    if v['__ctor'] == 'InstanceInput':
                        tool_list.append(comp.FindTool(v['SourceOp']))

            # set Lip Sync
            self.add2log('Apply Anim: Start')
            comp.StartUndo('RS Lip Sync')
            comp.Lock()
            for t in tool_list:
                comment = t.GetInput('Comments', comp.CurrentTime)
                t.LoadSettings(st)
                t.SetInput('Comments', comment, comp.CurrentTime)
            comp.Unlock()
            comp.EndUndo(True)
            self.add2log('Apply Anim: Done')

            # set color
            tatie_clip.SetClipColor(ch_data.color)
        self.add2log('')
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
        self.ui.timeOutSpinBox.setValue(c.time_out)
        self.ui.offsetSpinBox.setValue(c.offset)
        self.ui.extendSpinBox.setValue(c.extend)
        self.ui.videoIndexSpinBox.setValue(c.video_index)
        self.ui.audioIndexSpinBox.setValue(c.audio_index)
        self.ui.makeTextCheckBox.setChecked(c.make_text)
        self.ui.useCharaCheckBox.setChecked(c.use_chara)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.voice_dir = self.ui.voiceDirLineEdit.text().strip()

        c.wait_time = self.ui.waitTimeSpinBox.value()
        c.time_out = self.ui.timeOutSpinBox.value()
        c.offset = self.ui.offsetSpinBox.value()
        c.extend = self.ui.extendSpinBox.value()
        c.video_index = self.ui.videoIndexSpinBox.value()
        c.audio_index = self.ui.audioIndexSpinBox.value()
        c.make_text = self.ui.makeTextCheckBox.isChecked()
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
