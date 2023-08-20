import functools
import sys

from PySide6.QtCore import (
    Qt,
    QSize, QEvent,
)
from PySide6.QtGui import (
    QTextDocument,
    QAbstractTextDocumentLayout,
    QPalette,
    QKeySequence,
    QKeyEvent,
    QStandardItemModel,
    QStandardItem,
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyledItemDelegate,
    QTreeWidgetItem,
    QStyle,
)

from rs.core import (
    pipe as p,
)
from rs.gui import (
    appearance,
)
from rs_fusion.core import operator as op
from rs_fusion.tool.font_tool.favorites_font import MainWindow as FavoritesWindow
from rs_fusion.tool.font_tool.font_tool_ui import Ui_MainWindow

APP_NAME = 'FontTool'


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.doc = QTextDocument()
        self.doc.setDocumentMargin(2)
        f = QTreeWidgetItem().font(0)
        f.setPointSize(11)
        self.doc.setDefaultFont(f)
        self.sample_text = ''

    def paint(self, painter, option, index):
        if index.parent().isValid() and not index.parent().parent().isValid():
            self.initStyleOption(option, index)
            self.make_html(option.text)

            option.text = ''
            style = QApplication.style()
            style.drawControl(QStyle.ControlElement.CE_ItemViewItem, option, painter)

            painter.save()
            rect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, option)
            painter.translate(rect.topLeft())
            painter.setClipRect(rect.translated(-rect.topLeft()))
            context = QAbstractTextDocumentLayout.PaintContext()
            if option.state & QStyle.StateFlag.State_Selected:
                context.palette.setColor(
                    QPalette.Text, option.palette.color(QPalette.Active, QPalette.HighlightedText))
            self.doc.documentLayout().draw(painter, context)
            painter.restore()
        else:
            super().paint(painter, option, index)

    def sizeHint(self, option, index):
        if index.parent().isValid() and not index.parent().parent().isValid():
            self.initStyleOption(option, index)
            self.make_html(option.text)
            return QSize(self.doc.idealWidth(), self.doc.size().height())
        else:
            return super().sizeHint(option, index)

    def make_html(self, text):
        sample_text = self.sample_text
        if sample_text == '':
            sample_text = 'Sample Text'
        txt = '%s&nbsp;&nbsp;&nbsp;<font face="%s" size=4>%s</font>' % (text, text, sample_text)
        self.doc.setHtml(txt)


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
        self.resize(300, 700)

        self.fusion = fusion
        self.fonts = {}
        for k, v in self.fusion.FontManager.GetFontList().items():
            self.fonts[k] = list(v.keys())

        self.favorites_window = FavoritesWindow(self, fusion)
        self.favorites_window.open()
        self.favorites = self.favorites_window.favorites

        # tree view
        v = self.ui.treeView
        v.header().hide()
        d = ItemDelegate(v)
        d.sample_text = self.ui.sampleLineEdit.text()
        v.setItemDelegate(d)
        m = QStandardItemModel()
        v.setModel(m)
        sm = v.selectionModel()
        self.read_font()

        # shortcut
        up_action = QAction(self)
        up_action.setShortcut(QKeySequence(Qt.Key_Up))
        up_action.setShortcutContext(Qt.ApplicationShortcut)
        up_action.triggered.connect(self.select_up)
        self.addAction(up_action)

        down_action = QAction(self)
        down_action.setShortcut(QKeySequence(Qt.Key_Down))
        down_action.setShortcutContext(Qt.ApplicationShortcut)
        down_action.triggered.connect(self.select_down)
        self.addAction(down_action)

        apply_action = QAction(self)
        apply_action.setShortcut(QKeySequence(Qt.Key_Return))
        apply_action.setShortcutContext(Qt.ApplicationShortcut)
        apply_action.triggered.connect(self.apply_font)
        self.addAction(apply_action)

        # button
        self.ui.applyButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.readButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.favoritesButton.setStyleSheet(appearance.ex_stylesheet)

        # event
        self.favorites_window.ui.setButton.clicked.connect(self.read_font)
        self.ui.sampleLineEdit.textChanged.connect(self.on_sample_text_changed)

        self.ui.treeView.doubleClicked.connect(self.apply_font)
        sm.selectionChanged.connect(self.auto_apply)

        self.ui.readButton.clicked.connect(self.read_text)
        self.ui.applyButton.clicked.connect(self.apply_font)
        self.ui.favoritesButton.clicked.connect(self.favorites_window.show)
        self.ui.minimizeButton.clicked.connect(functools.partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

    def select_up(self):
        self.ui.treeView.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier))

    def select_down(self):
        self.ui.treeView.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Down, Qt.NoModifier))

    def on_sample_text_changed(self, text):
        d = self.ui.treeView.itemDelegate()
        d.sample_text = text
        self.ui.treeView.viewport().update()

    def read_font(self) -> None:
        self.favorites = self.favorites_window.favorites
        # setup
        v = self.ui.treeView
        m = v.model()
        m.clear()

        # tags
        tags = {'Favorites': [], 'All': []}
        for name in self.fonts.keys():
            if name in self.favorites:
                tags['Favorites'].append(name)
        tags['All'] = list(self.fonts.keys())

        # main
        for tag_name, names in tags.items():
            node = QStandardItem(tag_name)
            node.setSelectable(False)
            m.appendRow(node)

            # font names
            for name in names:
                font_item = QStandardItem(name)
                node.appendRow(font_item)
                weights = self.fonts[name]
                if len(weights) <= 1:
                    continue
                for weight in weights:
                    weight_item = QStandardItem(weight)
                    font_item.appendRow(weight_item)
        #
        v.collapseAll()
        cnt = m.rowCount()
        for i in range(cnt):
            v.expand(m.index(i, 0))

    def apply_font(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            return
        v = self.ui.treeView
        m = v.model()
        sm = v.selectionModel()
        indexes = sm.selectedIndexes()
        if len(indexes) == 0:
            return
        p_index = indexes[0].parent()
        if not p_index.isValid():
            return
        if p_index.parent().isValid():
            font_name = m.data(p_index, Qt.DisplayRole)
            font_style = m.data(indexes[0], Qt.DisplayRole)
        else:
            font_name = m.data(indexes[0], Qt.DisplayRole)
            font_style = self.fonts[font_name][0]
        op.apply_font(comp, font_name, font_style)

    def auto_apply(self):
        if self.ui.autoCheckBox.isChecked():
            self.apply_font()

    def read_text(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            return
        tools = list(comp.GetToolList(True).values())
        for tool in tools:
            if tool.ID in ['TextPlus', 'Text3D']:
                self.ui.sampleLineEdit.setText(
                    tool.GetInput('StyledText', comp.CurrentTime)
                )
                break

    def show(self) -> None:
        super().show()
        self.ui.sampleLineEdit.setFocus()


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run(None)
