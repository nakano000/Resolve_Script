from pathlib import Path

import dataclasses
import sys

from PySide6.QtCore import (
    Qt,
    QStringListModel,
)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow, QFileDialog,
)

from rs.core import (
    config,
    pipe as p,
    lang,
    util,
)
from rs.gui import (
    appearance,
    log,
)
from rs_fusion.core import ordered_dict_to_dict

from rs_resolve.core import (
    get_track_names,
    track_name2index, get_fps,
)

from rs_resolve.tool.subtitle2textPlus_typeB.subtitle2textPlus_typeB_ui import Ui_MainWindow

APP_NAME = 'Subtitle2TextPlusTypeB'


@dataclasses.dataclass
class ConfigData(config.Data):
    path: str = ''


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

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        self.setting_folder_name: str = 'Subtitle2TextPlus'
        self.text_plus_dir_name: str = '__RS_TextPlus_FPS__'
        data_dir: Path = config.DATA_PATH.joinpath('app', 'VoiceDropper')
        self.text_plus_drb: Path = data_dir.joinpath(self.text_plus_dir_name + '.drb')

        # style sheet
        # self.ui.settingFileToolButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.updateButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.convertButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.settingFileToolButton.clicked.connect(self.settingFileButton_clicked)
        self.ui.updateButton.clicked.connect(self.update_track)
        self.ui.convertButton.clicked.connect(self.convert)
        self.ui.closeButton.clicked.connect(self.close)

        #
        self.make_setting_folder()
        self.update_track()
        self.ui.closeButton.setFocus()

    def get_text_plus(self, item, text, st=None):
        if item.GetFusionCompCount() == 0:
            self.add2log('FusionComp not found.', log.ERROR_COLOR)
            return
        comp = item.GetFusionCompByIndex(1)
        lst = comp.GetToolList(False, 'TextPlus')
        if not lst[1]:
            self.add2log('TextPlus Node not found.', log.ERROR_COLOR)
            return
        tool = lst[1]
        comp.StartUndo('RS Jimaku')
        comp.Lock()
        tool.Font = 'Open Sans'
        if st is not None:
            tool.LoadSettings(st)
        tool.StyledText = text
        tool.UseFrameFormatSettings = 1
        comp.Unlock()
        comp.EndUndo(True)
        return lst[1]

    def convert(self) -> None:
        self.ui.logTextEdit.clear()

        data = self.get_data()

        resolve = self.fusion.GetResolve()
        page = resolve.GetCurrentPage()
        if page not in ['edit', 'cut']:
            return
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Project not found.', log.ERROR_COLOR)
            return
        media_pool = project.GetMediaPool()
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timeline not found.', log.ERROR_COLOR)
            return

        # track
        v_index = track_name2index(timeline, 'video', self.ui.videoComboBox.currentText())
        s_index = track_name2index(timeline, 'subtitle', self.ui.subtitleComboBox.currentText())

        if v_index == 0 or s_index == 0:
            self.add2log('Track not found.', log.ERROR_COLOR)
            return

        # fps
        fps = get_fps(timeline)

        # media pool check
        root_folder = media_pool.GetRootFolder()
        setting_folder = None
        text_plus_folder = None
        for folder in root_folder.GetSubFolderList():
            if folder.GetName() == self.setting_folder_name:
                setting_folder = folder

        if setting_folder is not None:
            for folder in setting_folder.GetSubFolderList():
                if folder.GetName() == self.text_plus_dir_name:
                    text_plus_folder = folder
                    break

        if text_plus_folder is None:
            self.add2log(
                f'Not Found: MediaPool/{self.text_plus_dir_name}/{self.text_plus_dir_name}',
                log.ERROR_COLOR,
            )
            return
        text_template = None
        for clip in text_plus_folder.GetClipList():
            if clip.GetClipProperty('Clip Name') == f'TextPlus{fps}FPS':
                text_template = clip
                break

        if text_template is None:
            self.add2log(
                f'Not Found: MediaPool/{self.text_plus_dir_name}/{self.text_plus_dir_name}/TextPlus{fps}FPS',
                log.ERROR_COLOR,
            )
            return

        # setting file
        setting_file = None
        st = None
        if data.path != '':
            setting_file = Path(data.path)
            if not setting_file.is_file():
                self.add2log('Setting File not found. Skipped.', log.WARNING_COLOR)
            else:
                st = ordered_dict_to_dict(bmd.readfile(data.path))
                if st is None:
                    self.add2log(f'Failed to read setting file:{data.path}', log.ERROR_COLOR)
                    return

        # main
        self.add2log('Start: Convert')
        for item in timeline.GetItemListInTrack('subtitle', s_index):
            sf = item.GetStart()
            ef = item.GetEnd()
            text = item.GetName()
            text_plus = media_pool.AppendToTimeline([{
                'mediaPoolItem': text_template,
                'startFrame': 0,
                'endFrame': ef - sf - 1,
                'trackIndex': v_index,
                'mediaType': 1,
                'recordFrame': sf,
            }])[0]
            if text_plus is None:
                self.add2log('Insert Text Clip: Failed', log.ERROR_COLOR)
                continue
            tool = self.get_text_plus(text_plus, text, st)
            if tool is None:
                continue

        # end
        self.add2log('Done!')

    def update_track(self) -> None:
        v_m: QStringListModel = self.ui.videoComboBox.model()
        s_m: QStringListModel = self.ui.subtitleComboBox.model()
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            self.add2log('Project not found.', log.ERROR_COLOR)
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            self.add2log('Timeline not found.', log.ERROR_COLOR)
            return
        if timeline is None:
            v_m.setStringList([])
            s_m.setStringList([])
            return

        # video
        v_m.setStringList(get_track_names(timeline, 'video'))

        # subtitle
        s_m.setStringList(get_track_names(timeline, 'subtitle'))

    def settingFileButton_clicked(self) -> None:
        w = self.ui.settingFileLineEdit
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select Setting File',
            w.text(),
            'Setting File (*.setting)',
        )
        if path != '':
            w.setText(path)

    def make_setting_folder(self):
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
            if folder.GetName() == self.setting_folder_name:
                dropper_folder = folder
                break
        if dropper_folder is None:
            dropper_folder = media_pool.AddSubFolder(root_folder, self.setting_folder_name)
        # import text+
        for folder in dropper_folder.GetSubFolderList():
            if folder.GetName() == self.text_plus_dir_name:
                return

        media_pool.SetCurrentFolder(dropper_folder)
        media_pool.ImportFolderFromFile(str(self.text_plus_drb))
        # restore current folder
        media_pool.SetCurrentFolder(current_folder)

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)

    def set_data(self, c: ConfigData):
        self.ui.settingFileLineEdit.setText(c.path)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.path = self.ui.settingFileLineEdit.text().strip()
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
