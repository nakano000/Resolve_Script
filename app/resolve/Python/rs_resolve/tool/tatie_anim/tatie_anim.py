import sys
from functools import partial

from PySide6.QtCore import (
    Qt,
    QStringListModel,
    QItemSelectionModel,
)
from PySide6.QtWidgets import (
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
from rs_resolve.core import get_currentframe
from rs_resolve.tool.tatie_anim.tatie_anim_ui import Ui_MainWindow

APP_NAME = '立ち絵アニメ'


def select(v, names):
    m: QStringListModel = v.model()
    sm = v.selectionModel()
    sm.clear()
    ss = m.stringList()
    for name in names:
        if name in ss:
            i = m.match(m.index(0, 0), Qt.DisplayRole, name)[0]
            sm.setCurrentIndex(
                i,
                QItemSelectionModel.SelectionFlag.SelectCurrent | QItemSelectionModel.SelectionFlag.Rows
            )


class MainWindow(QMainWindow):

    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(250, 250)

        self.fusion = fusion

        self.copy_anim_script = config.DATA_PATH.joinpath('lua', 'copy_anim.lua').read_text(encoding='utf-8')

        # list view
        m = QStringListModel()
        m.setStringList(p.pipe(
            range(1, 21),
            p.map(str),
            list,
        ))
        self.ui.videoIndexListView.setModel(m)

        # button
        self.ui.refreshButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.copyButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.copyButton.setText('copy(β版)')

        # event
        self.ui.refreshButton.clicked.connect(self.refresh)
        self.ui.copyButton.clicked.connect(self.copy)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))

        #
        select(self.ui.videoIndexListView, ['1'])

    def refresh(self):
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
        index = self.get_index()
        if index is None:
            print('indexを選択してください。')
            return
        item = self.get_item(timeline, index)
        if item is None:
            print('VideoItemが見付かりません。')
            return
        if item.GetFusionCompCount() == 0:
            print('FusionCompが見付かりません。')
            return
        comp = item.GetFusionCompByIndex(1)
        comp.StartUndo('RS Refresh')
        tool_list = comp.GetToolList(False, 'Fuse.RS_GlobalStart')
        for _key in tool_list.keys():
            tool_list[_key].Refresh()
        comp.EndUndo(True)

    def copy(self):
        index = self.get_index()
        if index is None:
            print('indexを選択してください。')
            return
        self.fusion.Execute('\n'.join([
            self.copy_anim_script,
            'copyAnim(%d)' % index,
        ]))

    def get_timeline(self):
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            return None, 'Projectが見付かりません。'
        timeline = project.GetCurrentTimeline()
        if timeline is None:
            return None, 'Timelineが見付かりません。'
        return timeline, ''

    def get_index(self):
        v = self.ui.videoIndexListView
        m: QStringListModel = v.model()
        indexes = p.pipe(
            v.selectionModel().selectedIndexes(),
            p.map(m.data),
            p.map(str),
            p.map(int),
            list,
        )
        if len(indexes) == 0:
            return None

        return indexes[0]

    @staticmethod
    def get_item(timeline, index):
        frame = get_currentframe(timeline)
        for item in timeline.GetItemListInTrack('video', index):
            if item.GetStart() <= frame < item.GetEnd():
                return item
        return None

    @staticmethod
    def get_items(timeline, index, sf, ef):
        items = []
        all_items = timeline.GetItemListInTrack('video', index)
        if all_items is None:
            return items
        for item in timeline.GetItemListInTrack('video', index):
            if item.GetStart() < ef and sf < item.GetEnd():
                items.append(item)
        return items


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    pass
