import math
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
    pipe as p,
    lang,
    util,
)
from rs.gui import (
    appearance,
)

from rs_resolve.core import (
    get_fps,
    get_track_names,
    track_name2index,
)

from rs_resolve.tool.text_plus2srt.text_plus2srt_ui import Ui_MainWindow

APP_NAME = 'TextPlus2SRT'


def to_time(fps, frame) -> str:
    float_sec = frame / fps
    sec = math.floor(float_sec)
    ms = round((float_sec - sec) * 1000)
    minute, sec = divmod(sec, 60)
    hour, minute = divmod(minute, 60)
    return '%02d:%02d:%02d,%03d' % (hour, minute, sec, ms)


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
        self.resize(250, 50)
        self.fusion = fusion

        # combobox
        w = self.ui.videoComboBox
        m = QStringListModel()
        w.setModel(m)

        # style sheet
        self.ui.updateButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.saveButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.updateButton.clicked.connect(self.update_track)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.closeButton.clicked.connect(self.close)

        #
        self.update_track()
        self.ui.closeButton.setFocus()

    def save(self) -> None:
        type_name = 'srt'
        path, _ = QFileDialog.getSaveFileName(
            self,
            'save as',
            '',
            f'{type_name.upper()} File (*.{type_name.lower()})',
        )
        if path == '':
            return

        srt_file = Path(path)

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

        index = track_name2index(timeline, 'video', self.ui.videoComboBox.currentText())

        if index == 0:
            print(
                'Track not found.'
                if self.lang_code == lang.Code.en else
                '選択したトラックが見付かりません。'
            )
            return

        # start
        start_frame = timeline.GetStartFrame()
        fps = get_fps(timeline)
        data_list = []
        for i, item in enumerate(timeline.GetItemListInTrack('video', index)):
            if item.GetFusionCompCount() == 0:
                continue
            comp = item.GetFusionCompByIndex(1)
            lst = comp.GetToolList(False, 'TextPlus')
            if not lst[1]:
                continue
            s_text = to_time(fps, item.GetStart() - start_frame)
            e_text = to_time(fps, item.GetEnd() - start_frame)
            text = lst[1].GetInput('StyledText', 0)
            lst = [
                str(i + 1),
                s_text + ' --> ' + e_text,
                text,
            ]
            data_list.append('\n'.join(lst))
        srt = '\n\n'.join(data_list)

        util.write_text(srt_file, srt)

        # end
        print('Done!')

    def update_track(self) -> None:
        m: QStringListModel = self.ui.videoComboBox.model()
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
            m.setStringList([])
            return

        # video
        m.setStringList(get_track_names(timeline, 'video'))


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())
