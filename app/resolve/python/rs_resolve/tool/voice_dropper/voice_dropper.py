import json
import math
import os
from functools import partial

import dataclasses
import sys
import time

from pathlib import Path

from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)
from PySide6.QtGui import (
    QColor,
)

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

from rs.core import (
    config,
    pipe as p,
    util,
    chara_data,
    txt,
    lab,
)
from rs.core.chara_data import CharaData
from rs.gui.chara.chara import MainWindow as CharaWindow

from rs.gui import (
    appearance,
    log,
)

from rs_fusion.core import (
    ordered_dict_to_dict,
    pose,
)
from rs_resolve.core import (
    get_currentframe,
    set_currentframe,
    get_fps,
    track_name2index,
    get_item,
    get_track_item_count,
    LockOtherTrack,
    shortcut,
    Appender,
)
from rs_resolve.gui import (
    get_resolve_window,
    activate_window,
)
from rs_resolve.tool.voice_dropper.voice_dropper_ui import Ui_MainWindow

APP_NAME = 'Voice Dropper'

SCRIPT_DIR: Path = config.ROOT_PATH.joinpath('data', 'app', 'VoiceDropper')


@dataclasses.dataclass
class ConfigData(config.Data):
    voice_dir: str = ''

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
        self.resize(350, 650)
        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        data_dir: Path = config.DATA_PATH.joinpath('app', 'VoiceDropper')
        self.text_plus_dir_name: str = '__RS_TextPlus_FPS__'
        self.text_plus_drb: Path = data_dir.joinpath(self.text_plus_dir_name + '.drb')
        self.anim_setting: str = data_dir.joinpath('setting_base.txt').read_text(encoding='utf-8')
        self.anim_setting_mm: str = data_dir.joinpath('setting_aiueo_mm.txt').read_text(encoding='utf-8')

        # window
        self.chara_window = CharaWindow(self)
        self.lip_sync_window = None

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
        self.ui.lipSyncButton.clicked.connect(self.open_lip_sync_window)

        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.voiceDirLineEdit.textChanged.connect(self.start)
        self.ui.voiceDirToolButton.clicked.connect(self.voiceDirToolButton_clicked)
        #
        self.make_dropper_folder()
        self.ui.closeButton.setFocus()
        self.start()

    def open_lip_sync_window(self):
        if self.lip_sync_window is None:
            from rs_resolve.tool.voice_dropper.lip_sync_window import MainWindow as LipSyncWindow
            self.lip_sync_window = LipSyncWindow(self, self.fusion)
            self.lip_sync_window.ui.applyButton.clicked.connect(self.lip_sync)
        self.lip_sync_window.show()

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
            self.__observer.schedule(
                WatchdogEvent(self.modified), path=str(path), recursive=True
            )
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
        # store current folder
        current_folder = media_pool.GetCurrentFolder()
        # make folder
        dropper_folder = None
        for folder in root_folder.GetSubFolderList():
            if folder.GetName() == 'VoiceDropper':
                dropper_folder = folder
                break
        if dropper_folder is None:
            dropper_folder = media_pool.AddSubFolder(root_folder, 'VoiceDropper')
        # import text+
        for folder in dropper_folder.GetSubFolderList():
            if folder.GetName() == self.text_plus_dir_name:
                return

        media_pool.SetCurrentFolder(dropper_folder)
        media_pool.ImportFolderFromFile(str(self.text_plus_drb))
        # restore current folder
        media_pool.SetCurrentFolder(current_folder)

    def directory_changed(self, created_lst):
        use_watchdog = self.__observer.is_alive()
        if use_watchdog:
            self.stop()

        self.voice_drop(created_lst)

        if use_watchdog:
            self.start()

    @staticmethod
    def setup_track(timeline, video_index, audio_index):
        video_size = timeline.GetTrackCount('video')
        audio_size = timeline.GetTrackCount('audio')
        if video_index > video_size:
            for i in range(video_index - video_size):
                timeline.AddTrack('video')
        if audio_index > audio_size:
            for i in range(audio_index - audio_size):
                timeline.AddTrack('audio', 'stereo')

    def wave_check(self, f, start_time, step, time_out) -> bool:
        self.add2log('waveファイルチェック:  Start')
        while True:
            if time.time() - start_time > time_out:
                self.add2log('タイムアウト:ファイルが計算中ため、処理をスキップします。', log.ERROR_COLOR)
                return False
            try:
                os.rename(str(f), str(f))
                break
            except OSError:
                time.sleep(step)

        self.add2log('waveファイルチェック:  OK')
        return True

    def import_wave2mediapool(self, media_pool, f: Path, start_time, step, time_out):
        mi_list = media_pool.ImportMedia(str(f))
        while True:
            if time.time() - start_time > time_out:
                self.add2log('タイムアウト:音声ファイルのインポートに失敗しました。', log.ERROR_COLOR)
                return None
            if len(mi_list) > 0:
                break
            else:
                time.sleep(step)
                mi_list = media_pool.ImportMedia(str(f))

        return mi_list[0]

    def insert_audio_clip(
            self, media_pool, timeline,
            mi, f: Path, audio_index: int, record_frame: int,
            start_time, step, time_out
    ):
        self.add2log('Insert Audio Clip: Start')
        audio_info = {
            "mediaPoolItem": mi,
            "trackIndex": audio_index,
            "recordFrame": record_frame,
        }
        _cnt = get_track_item_count(timeline, 'audio', audio_index)
        clip = media_pool.AppendToTimeline([audio_info])[0]
        while True:
            if time.time() - start_time > time_out:
                self.add2log('タイムアウト:音声クリップの挿入に失敗しました。', log.ERROR_COLOR)
                return None
            time.sleep(step)
            if get_track_item_count(timeline, 'audio', audio_index) == _cnt:
                mi.ReplaceClip(str(f))
                clip = media_pool.AppendToTimeline([audio_info])[0]
            else:
                break

        self.add2log('Insert Audio Clip: Done')
        return clip

    def setup_text_plus(
            self, clip,
            ch_data: CharaData, txt_file: Path,
            width: int, height: int,
            make_text: bool
    ) -> bool:
        self.add2log('Text Setup: Start')
        # text+用のテキストを読み込み
        if not txt_file.is_file() and make_text:
            self.add2log('テキストファイルを作成します。')
            txt_file.write_text(QApplication.clipboard().text(), encoding='utf-8-sig')
        t = util.str2lines(
            txt.read(txt_file, ch_data.c_code),
            ch_data.str_width * 2,
        ) if txt_file.is_file() else ''

        # comp
        if clip.GetFusionCompCount() == 0:
            self.add2log('FusionCompが見付かりません。', log.ERROR_COLOR)
            return False
        comp = clip.GetFusionCompByIndex(1)

        # tool
        lst = list(comp.GetToolList(False, 'TextPlus').values())
        if len(lst) == 0:
            self.add2log('Text+が見付かりません。', log.ERROR_COLOR)
            return False
        tool = lst[0]

        # settings
        st = ordered_dict_to_dict(bmd.readfile(str(ch_data.setting_file)))
        if st is None:
            self.add2log(f'settingファイルの読み込みに失敗しました。:{str(ch_data.setting_file)}', log.ERROR_COLOR)
            return False

        # apply
        comp.StartUndo('RS Jimaku')
        comp.Lock()
        tool.LoadSettings(st)
        tool.StyledText = t
        tool.UseFrameFormatSettings = 0
        tool.Width = width
        tool.Height = height
        comp.Unlock()
        comp.EndUndo(True)
        self.add2log('Text Setup: Done')
        return True

    def voice_drop(self, created_lst):
        time_sta = time.time()
        self.ui.logTextEdit.clear()
        if len(created_lst) == 0:
            return
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Projectが見付かりません。', log.ERROR_COLOR)
        media_pool = project.GetMediaPool()
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timelineが見付かりません。', log.ERROR_COLOR)
            return
        fps = get_fps(timeline)

        root_folder = media_pool.GetRootFolder()
        dropper_folder = None
        text_plus_folder = None
        voice_folder = None
        for folder in root_folder.GetSubFolderList():
            if folder.GetName() == 'VoiceDropper':
                dropper_folder = folder
            if folder.GetName() == 'Voice':
                voice_folder = folder
        if dropper_folder is not None:
            for folder in dropper_folder.GetSubFolderList():
                if folder.GetName() == self.text_plus_dir_name:
                    text_plus_folder = folder
                    break
        if voice_folder is None:
            voice_folder = media_pool.AddSubFolder(root_folder, "Voice")
        media_pool.SetCurrentFolder(voice_folder)

        if dropper_folder is None or text_plus_folder is None:
            self.add2log(f'MediaPoolにVoiceDropper/{self.text_plus_dir_name}フォルダ見付かりません。', log.ERROR_COLOR)
            return

        text_template = None
        for clip in text_plus_folder.GetClipList():
            if clip.GetClipProperty('Clip Name') == f'TextPlus{fps}FPS':
                text_template = clip
                break

        if text_template is None:
            self.add2log(
                f'MediaPoolにVoiceDropper/{self.text_plus_dir_name}/TextPlus{fps}FPSが見付かりません。',
                log.ERROR_COLOR,
            )
            return
        self.add2log('Use %s' % text_template.GetClipProperty('Clip Name'))

        # get data
        data = self.get_data()

        # main
        resolve.OpenPage('edit')
        appender = Appender(resolve, media_pool)
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
            ch_data = chara_data.from_file(f)

            # トラック
            audio_index = track_name2index(timeline, 'audio', ch_data.track_name + '_a')
            if audio_index == 0 or not data.use_chara:
                audio_index = data.audio_index
            video_index = track_name2index(timeline, 'video', ch_data.track_name + '_t')
            if video_index == 0 or not data.use_chara:
                video_index = data.video_index

            self.setup_track(timeline, video_index, audio_index)
            if get_item(timeline, 'video', video_index, current_frame) is not None:
                self.add2log('Videoトラックに既にアイテムが存在します。', log.ERROR_COLOR)
                return
            if get_item(timeline, 'audio', audio_index, current_frame) is not None:
                self.add2log('Audioトラックに既にアイテムが存在します。', log.ERROR_COLOR)
                return

            # time out 設定
            step = 0.2
            start_time = time.time()

            # ロック確認 VOICEPEAK用に出力待ち
            if not self.wave_check(f, start_time, step, data.time_out):
                continue

            # import
            mi = self.import_wave2mediapool(media_pool, f, start_time, step, data.time_out)
            if mi is None:
                continue

            # 音声クリップの挿入
            clip = self.insert_audio_clip(
                media_pool, timeline,
                mi, f, audio_index, current_frame,
                start_time, step, data.time_out,
            )
            if clip is None:
                continue

            duration = math.ceil(clip.GetDuration(True))  # GetDuration(True)で少数対応なら少数が帰る

            # Text+の挿入
            self.add2log('Insert Text Clip: Start')

            text_plus = appender.append2timeline(
                item=text_template,
                duration=duration + 1 + data.extend,
                track_index=video_index,
                media_type=1,
                record_frame=current_frame,
            )
            if text_plus is None:
                self.add2log('Insert Text Clip: Failed', log.ERROR_COLOR)
                continue
            self.add2log('Insert Text Clip: Done')

            # Text+の設定
            if not self.setup_text_plus(
                    text_plus,
                    ch_data,
                    f.parent.joinpath(f.stem + '.txt'),
                    int(timeline.GetSetting('timelineResolutionWidth')),
                    int(timeline.GetSetting('timelineResolutionHeight')),
                    data.make_text,
            ):
                continue

            # カラー、リンク、プレイヘッド
            if ch_data.color in config.COLOR_LIST:
                text_plus.SetClipColor(ch_data.color)
                clip.SetClipColor(ch_data.color)
            timeline.SetClipsLinked([text_plus, clip], True)

            set_currentframe(timeline, current_frame + duration + data.offset + data.extend)

            # log
            self.add2log('Import: ' + str(f))
            self.add2log('')
        # end
        time_end = time.time()
        self.add2log('Done! %fs' % (time_end - time_sta))

    def cut_clip(self, w, timeline, index, sf, ef, wait, sc: shortcut.Data):
        self.add2log('Cut Clip: Start')
        activate_window(w)
        sc.active_timeline_panel()
        sc.deselect_all()

        # cut list
        clip = get_item(timeline, 'video', index, sf)
        cut_lst = []
        if clip.GetStart() != sf:
            cut_lst.append(sf)
        if clip.GetEnd() != ef:
            cut_lst.append(ef)

        # cut
        for n in cut_lst:
            set_currentframe(timeline, n)
            activate_window(w)
            _cnt = get_track_item_count(timeline, 'video', index)
            start_time = time.time()
            sc.razor()
            while True:
                if time.time() - start_time > wait:
                    break
                if get_track_item_count(timeline, 'video', index) > _cnt:
                    break
                time.sleep(0.1)
        self.add2log('Cut Clip: Done')

    def set_anim(self, comp, tool, ch_data, f, fps):
        # get anim
        self.add2log(f'Load Anim({ch_data.anim_type.strip().lower()}, {ch_data.anim_parameter}): Start')
        lab_file = f.with_suffix('.lab')
        anim = ''
        offset = comp.GetAttrs()['COMPN_GlobalStart']
        if ch_data.anim_type.strip().lower() == 'open':
            anim = lab.wav2anim(f, fps, offset)
        elif lab_file.is_file():
            anim = lab.lab2anim(lab_file, fps, ch_data.anim_type.strip().lower(), offset)
        else:
            self.add2log(f'labファイルが見付かりません。{str(lab_file)}', log.ERROR_COLOR)
            return

        st = ordered_dict_to_dict(bmd.readstring(self.anim_setting % (
            ch_data.anim_parameter,
            ch_data.anim_parameter,
            ch_data.anim_parameter,
            anim,
        )))
        if st is None:
            self.add2log('アニメーションの読み込みに失敗しました。', log.ERROR_COLOR)
            return
        self.add2log('Load Anim: Done')

        # get anim tool list
        _pram = ch_data.anim_parameter
        tool_list = []
        for v in tool.SaveSettings()['Tools'][tool.Name]['Inputs'].values():
            if isinstance(v, dict) and '__ctor' in v.keys():
                if v['__ctor'] == 'InstanceInput' and v['Source'] in [_pram]:
                    tool_list.append(comp.FindTool(v['SourceOp']))

        # set Lip Sync
        self.add2log('Apply Anim: Start')
        comp.StartUndo('RS Lip Sync')
        comp.Lock()
        for t in tool_list:
            if t.GetAttrs()['TOOLB_Visible']:
                comment = t.GetInput('Comments', comp.CurrentTime)
                t.LoadSettings(st)
                t.SetInput('Comments', comment, comp.CurrentTime)
            else:
                o_st = t.SaveSettings()
                o_st['Tools']['MouthAnimBezierSpline'] = st['Tools']['MouthAnimBezierSpline']
                o_st['Tools'][t.Name]['Inputs'][_pram] = st['Tools']['Ctrl']['Inputs'][_pram]
                t.LoadSettings(o_st)
        comp.Unlock()
        comp.EndUndo(True)
        self.add2log('Apply Anim: Done')

    def set_anim_ofx(self, comp, ch_data, f):
        self.add2log(f'Load Anim({ch_data.anim_type.strip().lower()}, {ch_data.anim_parameter}): Start')
        lab_file = f.with_suffix('.lab')
        ch_data.anim_type = ch_data.anim_type.strip().lower()
        offset = comp.GetAttrs()['COMPN_GlobalStart']
        if  not lab_file.is_file():
            self.add2log(f'labファイルが見付かりません。{str(lab_file)}', log.ERROR_COLOR)
            return
        tools = comp.GetToolList()
        tool = None
        for t in tools.values():
            if t.ID.startswith('ofx.net.tachie_ofx.'):
                tool = t
                break
        if tool is None:
            self.add2log('立ち絵プラグインが見付かりません。', log.ERROR_COLOR)
            return
        # set Lip Sync
        self.add2log('Apply Anim: Start')
        comp.StartUndo('RS Lip Sync')
        comp.Lock()
        st = tool.SaveSettings()
        st['Tools'][tool.Name]['Inputs']['@lipsync/use_lab']['Value'] = 1
        st['Tools'][tool.Name]['Inputs']['@lipsync/lab_path']['Value'] = str(lab_file).replace('\\', '/')
        st['Tools'][tool.Name]['Inputs']['@lipsync/offset_frames']['Value'] = offset
        tool.LoadSettings(st)
        comp.Unlock()
        comp.EndUndo(True)
        self.add2log('Apply Anim: Done')

    def set_anim_mm(self, comp, ch_data, f, fps):
        # get anim
        self.add2log(f'Load Anim({ch_data.anim_type.strip().lower()}, {ch_data.anim_parameter}): Start')
        lab_file = f.with_suffix('.lab')
        anim_list = []
        ch_data.anim_type = ch_data.anim_type.strip().lower()
        offset = comp.GetAttrs()['COMPN_GlobalStart']
        if lab_file.is_file():
            anim_list = lab.lab2anim_mm(lab_file, fps, ch_data.anim_type, offset)
        else:
            self.add2log(f'labファイルが見付かりません。{str(lab_file)}', log.ERROR_COLOR)
            return
        if len(anim_list) < 7:
            self.add2log('アニメーションの読み込みに失敗しました。', log.ERROR_COLOR)
            return

        st = ordered_dict_to_dict(bmd.readstring(self.anim_setting_mm % tuple(anim_list[:7])))
        if st is None:
            self.add2log('アニメーションの読み込みに失敗しました。', log.ERROR_COLOR)
            return

        # scale anim
        scale_st = None
        if ch_data.anim_type == 'aiueo3':
            scal_parm = 'Size'
            if len(anim_list) > 7:
                scale_st = ordered_dict_to_dict(bmd.readstring(self.anim_setting % (
                    scal_parm,
                    scal_parm,
                    scal_parm,
                    anim_list[7],
                )))
            if scale_st is None:
                self.add2log('アニメーションの読み込みに失敗しました。', log.ERROR_COLOR)
                return
        self.add2log('Load Anim: Done')

        # get anim tool list
        tool_name = 'MouthAnim'
        tool = comp.FindTool(tool_name)
        if tool is None:
            self.add2log('MultiMerge MouthAnimがありません。', log.ERROR_COLOR)
            return
        scale_tool = None
        if ch_data.anim_type == 'aiueo3':
            scale_tool_name = 'MouthScale'
            scale_tool = comp.FindTool(scale_tool_name)
            if scale_tool is None:
                self.add2log('MouthScaleがありません。', log.ERROR_COLOR)
                return

        # set Lip Sync
        self.add2log('Apply Anim(MultiMerge): Start')
        comp.StartUndo('RS Lip Sync')
        comp.Lock()
        parm_name_list = [
            'Comments',
            'LayerName1',
            'LayerName2',
            'LayerName3',
            'LayerName4',
            'LayerName5',
            'LayerName6',
            'LayerName7',
        ]
        parm_dct = {}
        for parm in parm_name_list:
            parm_dct[parm] = tool.GetInput(parm, comp.CurrentTime)
        tool.LoadSettings(st)
        for parm in parm_name_list:
            tool.SetInput(parm, parm_dct[parm], comp.CurrentTime)
        # scale
        if ch_data.anim_type == 'aiueo3':
            comment = scale_tool.GetInput('Comments', comp.CurrentTime)
            scale_tool.LoadSettings(scale_st)
            scale_tool.SetInput('Comments', comment, comp.CurrentTime)

        comp.Unlock()
        comp.EndUndo(True)
        self.add2log('Apply Anim: Done')

    def set_anim_mm_o(self, comp, f, fps):
        self.add2log('Load Anim(open, <MultiMerge>): Start')
        # get anim tool list
        tool_name = 'MouthOpenAnim'
        tool = comp.FindTool(tool_name)
        if tool is None:
            self.add2log('MultiMerge MouthOpenAnimがありません。', log.ERROR_COLOR)
            return
        layer_max = int(tool.GetInput('M_Open', comp.CurrentTime))

        # get anim
        offset = comp.GetAttrs()['COMPN_GlobalStart']

        st = ordered_dict_to_dict(bmd.readstring(
            lab.wav2setting_mm(comp, f, fps, offset)
        ))
        if st is None:
            self.add2log('アニメーションの読み込みに失敗しました。', log.ERROR_COLOR)
            return

        self.add2log('Load Anim: Done')

        # set Lip Sync
        self.add2log('Apply Anim(MultiMerge): Start')

        # store
        parm_name_list = p.pipe(
            range(1, layer_max + 1),
            p.map(lambda x: 'LayerName%d' % x),
            list,
        )
        parm_name_list.append('Comments')
        parm_dct = {}
        for parm in parm_name_list:
            parm_dct[parm] = tool.GetInput(parm, comp.CurrentTime)

        # apply
        comp.StartUndo('RS Lip Sync')
        comp.Lock()

        tool.LoadSettings(st)

        # restore
        for parm in parm_name_list:
            tool.SetInput(parm, parm_dct[parm], comp.CurrentTime)

        comp.Unlock()
        comp.EndUndo(True)
        self.add2log('Apply Anim: Done')

    def lip_sync(self):
        self.ui.logTextEdit.clear()

        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Projectが見付かりません。', log.ERROR_COLOR)
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timelineが見付かりません。', log.ERROR_COLOR)
            return

        fps = get_fps(timeline)
        v_index = self.lip_sync_window.get_video_track_index(timeline)
        a_index = self.lip_sync_window.get_audio_track_index(timeline)

        if v_index == 0 or a_index == 0:
            self.add2log('選択したトラックが見付かりません。', log.ERROR_COLOR)
            return

        v_item = get_item(timeline, 'video', v_index)
        if v_item is None:
            self.add2log('ビデオクリップが見付かりません。', log.ERROR_COLOR)
            return
        v_sf = v_item.GetStart()
        v_ef = v_item.GetEnd()

        audio_items = []
        for item in timeline.GetItemListInTrack('audio', a_index):
            if item.GetStart() < v_ef and v_sf < item.GetEnd():
                audio_items.append(item)

        w = get_resolve_window(project.GetName())
        if w is None and not util.IS_MAC:
            self.add2log('DaVinci ResolveのWindowが見付かりません。', log.ERROR_COLOR)
            return
        if util.IS_WIN:
            self.setWindowState(Qt.WindowMinimized)  # windowsの場合、最小化しないとウィンドウがactiveにならないので、
            self.setWindowState(Qt.WindowActive)  # 最小化してからactiveにする

        # main
        self.add2log('Start')
        # config

        data = self.lip_sync_window.get_data()

        with LockOtherTrack(timeline, v_index, track_type='video', enable=data.use_auto_lock):
            sc = shortcut.Data()
            if shortcut.CONFIG_FILE.is_file():
                sc.load(shortcut.CONFIG_FILE)
            # main loop
            for item in audio_items:
                sf = max([item.GetStart(), v_sf])
                ef = min([math.ceil(item.GetEnd(True)), v_ef])  # endが少数なら切り上げ
                f = Path(item.GetMediaPoolItem().GetClipProperty('File Path'))
                self.add2log('wav: ' + str(f))

                # キャラクター設定
                ch_data = chara_data.from_file(f)

                # split
                self.cut_clip(w, timeline, v_index, sf, ef, data.time_out, sc)

                # get Macro Tool
                tatie_clip = get_item(timeline, 'video', v_index, sf)
                if tatie_clip is None:
                    self.add2log('立ち絵ビデオクリップが見付かりません。', log.ERROR_COLOR)
                    continue
                if tatie_clip.GetFusionCompCount() == 0:
                    self.add2log('Fusion Compが見付かりません。', log.ERROR_COLOR)
                    continue
                comp = tatie_clip.GetFusionCompByIndex(1)
                tools = p.pipe(
                    comp.GetToolList(False).values(),
                    p.filter(lambda x: x.ID in ['MacroOperator', 'GroupOperator']),
                    p.filter(lambda x: x.ParentTool is None),
                    list,
                )
                if len(tools) == 0:
                    self.add2log('MacroまたはGroupが見付かりません。', log.ERROR_COLOR)
                    continue
                tool = tools[0]

                # set anim
                if ch_data.anim_parameter == '<MultiMerge>':
                    if ch_data.anim_type == 'open':
                        self.set_anim_mm_o(comp, f, fps)
                    else:
                        self.set_anim_mm(comp, ch_data, f, fps)
                elif ch_data.anim_parameter == '<TACHIE_OFX>':
                    self.set_anim_ofx(comp, ch_data, f)
                else:
                    self.set_anim(comp, tool, ch_data, f, fps)

                # set color
                tatie_clip.SetClipColor(ch_data.color)

                # set pose
                pf = Path(ch_data.pose_file)
                if pf.is_file():
                    self.add2log('Apply Pose: Start')
                    text = pf.read_text(encoding='utf-8')
                    try:
                        lst = json.loads(text)
                    except json.JSONDecodeError:
                        self.add2log('Invalid JSON')
                        continue
                    if isinstance(lst, list):
                        pose.apply(comp, lst)
                        self.add2log('Apply Pose: Done')

        # delete empty
        if data.use_delete:
            self.add2log('Delete: Start')
            del_list = []
            for clip in timeline.GetItemListInTrack('video', v_index):
                if clip.GetStart() < v_ef and v_sf < clip.GetEnd():
                    c_frame = clip.GetStart() + clip.GetDuration() // 2
                    _wav = get_item(timeline, 'audio', a_index, c_frame)
                    if _wav is None:
                        del_list.append(clip)
            timeline.DeleteClips(del_list, False)
            self.add2log('Delete: Done')

        # log
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
