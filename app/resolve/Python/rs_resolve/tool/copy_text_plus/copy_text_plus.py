from pathlib import Path

import sys

from PySide2.QtCore import (
    Qt,
    QStringListModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow, QFileDialog,
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
    track_name2index,
    get_item,
)
from rs_resolve.tool.copy_text_plus.copy_text_plus_ui import Ui_MainWindow

APP_NAME = 'Copy TextPlus'


def get_track_names(timeline, track_type):
    r = []
    for i in range(1, timeline.GetTrackCount(track_type) + 1):
        r.append(timeline.GetTrackName(track_type, i))
    return r


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
        self.resize(250, 400)
        self.fusion = fusion

        # config
        self.config_dir: Path = config.CONFIG_DIR.joinpath('PasteTool')
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.default_file: Path = self.config_dir.joinpath('default_CopyTextplus.txt')
        if not self.default_file.exists():
            self.default_file.write_text('StyledText\nWidth\nHeight\nUseFrameFormatSettings', encoding='utf-8')
        self.ui.plainTextEdit.setPlainText(
            self.default_file.read_text(encoding='utf-8')
        )

        # combobox
        for w in [self.ui.sourceComboBox, self.ui.destinationComboBox]:
            m = QStringListModel()
            w.setModel(m)

        # style sheet
        self.ui.updateButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.copyButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.swapButton.clicked.connect(self.swap_track)
        self.ui.updateButton.clicked.connect(self.update_track)

        self.ui.loadButton.clicked.connect(self.load_txt)
        self.ui.saveButton.clicked.connect(self.save_txt)

        self.ui.copyButton.clicked.connect(self.copy)
        self.ui.closeButton.clicked.connect(self.close)

        #
        self.update_track()
        self.ui.closeButton.setFocus()

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

    def copy(self) -> None:
        resolve = self.fusion.GetResolve()
        page = resolve.GetCurrentPage()
        if page not in ['edit', 'cut']:
            return
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            print('Project not found.')
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            print('Timeline not found.')
            return

        src_index = track_name2index(timeline, 'video', self.ui.sourceComboBox.currentText())
        dst_index = track_name2index(timeline, 'video', self.ui.destinationComboBox.currentText())

        if src_index == 0 or dst_index == 0:
            print('Track not found.')
            return
        if src_index == dst_index:
            print('Source and destination tracks are the same.')
            return

        src_item = get_item(timeline, 'video', src_index)
        if src_item is None:
            print('Video clip not found on source track.')
            return
        if src_item.GetFusionCompCount() == 0:
            print('FusionComp not found on source track..')
            return
        src_comp = src_item.GetFusionCompByIndex(1)
        src_lst = src_comp.GetToolList(False, 'TextPlus')
        if not src_lst[1]:
            print('TextPlus Node not found on source track.')
            return
        src_tp = src_lst[1]
        src_sf = src_item.GetStart()
        src_ef = src_item.GetEnd()

        dst_items = []
        for item in timeline.GetItemListInTrack('video', dst_index):
            if item.GetStart() < src_ef and src_sf < item.GetEnd():
                dst_items.append(item)

        param_list = p.pipe(
            self.ui.plainTextEdit.toPlainText().splitlines(),
            p.map(p.call.strip()),
            p.filter(lambda x: x != ''),
            list,
        )

        # main
        for item in dst_items:
            if item.GetFusionCompCount() == 0:
                continue
            comp = item.GetFusionCompByIndex(1)
            lst = comp.GetToolList(False, 'TextPlus')
            if not lst[1]:
                continue
            tp = lst[1]
            comp.StartUndo('Copy TextPlus')
            comp.Lock()
            src_st = src_tp.SaveSettings()
            dst_st = tp.SaveSettings()
            for param in param_list:
                if param in dst_st['Tools'][tp.Name]['Inputs']:
                    src_st['Tools'][src_tp.Name]['Inputs'][param] = dst_st['Tools'][tp.Name]['Inputs'][param]
                else:
                    src_st['Tools'][src_tp.Name]['Inputs'].pop(param, None)
            tp.LoadSettings(src_st)
            comp.Unlock()
            comp.EndUndo(True)

        # end
        print('Done!')

    def swap_track(self) -> None:
        src_text = self.ui.sourceComboBox.currentText()
        dst_text = self.ui.destinationComboBox.currentText()
        self.ui.sourceComboBox.setCurrentText(dst_text)
        self.ui.destinationComboBox.setCurrentText(src_text)

    def update_track(self) -> None:
        src_m: QStringListModel = self.ui.sourceComboBox.model()
        dst_m: QStringListModel = self.ui.destinationComboBox.model()
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            print('Project not found.')
            return
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            print('Timeline not found.')
            return
        if timeline is None:
            src_m.setStringList([])
            dst_m.setStringList([])
            return

        # video
        lst = get_track_names(timeline, 'video')
        src_m.setStringList(lst)
        dst_m.setStringList(lst)

    def load_txt(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', str(self.config_dir), 'Text files (*.txt)')[0]
        if file_name == '':
            return
        self.ui.plainTextEdit.setPlainText(
            Path(file_name).read_text(encoding='utf-8')
        )

    def save_txt(self):
        file_name = QFileDialog.getSaveFileName(self, 'Save file', str(self.config_dir), 'Text files (*.txt)')[0]
        if file_name == '':
            return
        Path(file_name).write_text(
            self.ui.plainTextEdit.toPlainText(),
            encoding='utf-8',
        )

def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())
