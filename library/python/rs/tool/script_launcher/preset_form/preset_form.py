import subprocess
import sys
from functools import partial
from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QItemSelectionModel,
    QStringListModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
)

from rs.core import (
    config,
    pipe as p,
)
from rs.gui import (
    appearance,
)
from rs.tool.script_launcher.preset_form.filter_ui import Ui_Form as Filter_Ui
from rs.tool.script_launcher.preset_form.preset_form_ui import Ui_Form


class FilterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Filter_Ui()
        self.ui.setupUi(self)
        self.setWindowFlags(
            Qt.Tool
            | Qt.WindowStaysOnTopHint
        )
        self.setWindowTitle('filter')
        self.path = None

        self.ui.saveButton.setStyleSheet(appearance.ex_stylesheet)
        # event
        self.ui.saveButton.clicked.connect(self.save_filter)
        self.ui.cancelButton.clicked.connect(self.close)

        #

    def load_filter(self):
        self.ui.textEdit.setPlainText(self.path.read_text(encoding='utf-8'))

    def save_filter(self):
        self.path.write_text(self.ui.textEdit.toPlainText(), encoding='utf-8')
        self.close()

    def set_path(self, path: Path):
        if path.is_file():
            self.path = path
            self.setWindowTitle(self.path.name + ' (' + str(self.path) + ')')

    def show(self):
        if self.path.is_file():
            self.load_filter()
            super().show()


class Form(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Preset')
        self.setWindowFlags(
            Qt.Tool
            | Qt.WindowStaysOnTopHint
        )
        self.resize(350, 400)

        self.preset_path = config.ROOT_PATH.joinpath('Preset')

        # window
        self.filter_window = FilterWindow()

        # listView
        for v in [self.ui.dirListView, self.ui.fileListView, self.ui.filterListView]:
            m = QStringListModel()
            m.setStringList([])
            v.setModel(m)
        # button
        self.ui.applyButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.addFilterButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.renameButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.editFilterButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.dirListView.selectionModel().selectionChanged.connect(self.load_file_List)
        self.ui.dirListView.selectionModel().selectionChanged.connect(self.load_filter_List)
        self.ui.fileListView.selectionModel().selectionChanged.connect(self.update_setting_path)
        self.ui.filterListView.selectionModel().selectionChanged.connect(self.update_text)
        self.ui.filterListView.selectionModel().selectionChanged.connect(self.update_filter_path)
        self.ui.trackIndexSpinBox.valueChanged.connect(self.update_track_index)
        self.ui.addFilterButton.clicked.connect(self.add_filter)
        self.ui.renameButton.clicked.connect(self.rename_filter)
        self.ui.editFilterButton.clicked.connect(self.edit_filter)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.dirListView.doubleClicked.connect(partial(self.open_dir, self.preset_path))
        self.ui.fileListView.doubleClicked.connect(self.open_file_dir)
        self.ui.filterListView.doubleClicked.connect(self.open_filter_dir)

        #
        self.update_track_index()

    def update_text(self):
        name = ''
        path = self.get_filter_path()
        if not path is None:
            name = path.stem if path.name != 'None' else ''
        self.ui.filterNameLineEdit.setText(name)

    def update_filter_path(self):
        self.ui.applyButton.setFilterFile(self.get_filter_path())

    def update_setting_path(self):
        self.ui.applyButton.setSettingFile(self.get_file_path())

    def update_track_index(self):
        self.ui.applyButton.setTrackIndex(self.ui.trackIndexSpinBox.value())

    def add_filter(self):
        path = self.get_dir_path()
        if path is None:
            return
        name = self.ui.filterNameLineEdit.text().strip()
        ext = '.txt'
        if name.lower().endswith(ext):
            name = name[: -4]
        if name == '':
            return
        dir_path = path.joinpath('').joinpath('Filter')
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path.joinpath(name + '.txt')
        if not file_path.is_file():
            file_path.write_text(
                '',
                encoding='utf-8',
                newline='\n',
            )
        self.load_filter_List()
        self.select_by_name(self.ui.filterListView, name + ext)

    def rename_filter(self):
        org = self.get_filter_path()
        path = self.get_dir_path()
        if path is None or org is None:
            return
        name = self.ui.filterNameLineEdit.text().strip()
        ext = '.txt'
        if name.lower().endswith(ext):
            name = name[: -4]
        if name == '':
            return
        file_path = path.joinpath('Filter', name + '.txt')
        if not file_path.is_file() and org.is_file():
            org.rename(file_path)
        self.load_filter_List()
        self.select_by_name(self.ui.filterListView, name + ext)

    def edit_filter(self):
        path = self.get_filter_path()
        if path is None:
            return
        if not path.is_file():
            return
        self.filter_window.set_path(path)
        self.filter_window.show()

    @staticmethod
    def select_by_name(v, name):
        m: QStringListModel = v.model()
        sm = v.selectionModel()
        ss = m.stringList()
        if name in ss:
            i = m.match(m.index(0, 0), Qt.DisplayRole, name)[0]
            sm.setCurrentIndex(i, QItemSelectionModel.Clear
                               | QItemSelectionModel.SelectCurrent
                               | QItemSelectionModel.Rows)

    def setting(self):
        self.ui.filterNameLineEdit.setText('')
        self.load_dir_List()

    def load_dir_List(self):
        path: Path = self.preset_path
        v = self.ui.dirListView
        m: QStringListModel = v.model()
        sm = v.selectionModel()
        old_selection = sm.selection()

        wasBlocked = v.blockSignals(True)
        p.pipe(
            path.iterdir(),
            p.filter(p.call.is_dir()),
            p.map(p.get.name),
            list,
            sorted,
            m.setStringList,
        )
        ss = m.stringList()
        if len(ss) > 0:
            i = m.match(m.index(0, 0), Qt.DisplayRole, ss[0])[0]
            sm.setCurrentIndex(i, QItemSelectionModel.Clear
                               | QItemSelectionModel.SelectCurrent
                               | QItemSelectionModel.Rows)
        v.blockSignals(wasBlocked)
        new_selection = sm.selection()
        sm.emitSelectionChanged(new_selection, old_selection)

    def get_dir_path(self):
        v = self.ui.dirListView
        m: QStringListModel = v.model()
        i = v.selectionModel().currentIndex()
        s = m.data(i)
        if s is not None:
            return self.preset_path.joinpath(s)
        return None

    def load_file_List(self):
        path = self.get_dir_path()
        v = self.ui.fileListView
        m: QStringListModel = v.model()
        sm = v.selectionModel()
        if path is None:
            m.setStringList([])
            return
        p.pipe(
            path.iterdir(),
            p.filter(p.call.is_file()),
            p.filter(lambda x: x.suffix.lower() == '.setting'),
            p.map(p.get.name),
            list,
            sorted,
            m.setStringList,
        )
        ss = m.stringList()
        if len(ss) > 0:
            i = m.match(m.index(0, 0), Qt.DisplayRole, ss[0])[0]
            sm.setCurrentIndex(i, QItemSelectionModel.Clear
                               | QItemSelectionModel.SelectCurrent
                               | QItemSelectionModel.Rows)

    def load_filter_List(self):
        path = self.get_dir_path().joinpath('Filter')
        v = self.ui.filterListView
        m: QStringListModel = v.model()
        sm = v.selectionModel()
        if path is None or not path.is_dir():
            m.setStringList(['None'])
        else:
            p.pipe(
                path.iterdir(),
                p.filter(p.call.is_file()),
                p.filter(lambda x: x.suffix.lower() == '.txt'),
                p.map(p.get.name),
                list,
                sorted,
                lambda x: ['None'] + x,
                m.setStringList,
            )
        ss = m.stringList()
        if len(ss) > 0:
            i = m.match(m.index(0, 0), Qt.DisplayRole, ss[0])[0]
            sm.setCurrentIndex(i, QItemSelectionModel.Clear
                               | QItemSelectionModel.SelectCurrent
                               | QItemSelectionModel.Rows)

    def get_file_path(self):
        path = self.get_dir_path()
        if path is None:
            return None
        v = self.ui.fileListView
        m: QStringListModel = v.model()
        i = v.selectionModel().currentIndex()
        s = m.data(i)
        if s is not None:
            return path.joinpath(s)
        return None

    def get_filter_path(self):
        path = self.get_dir_path()
        if path is None:
            return None
        v = self.ui.filterListView
        m: QStringListModel = v.model()
        i = v.selectionModel().currentIndex()
        s = m.data(i)
        if s is not None:
            return path.joinpath('Filter', s)
        return None

    def open_file_dir(self):
        path = self.get_file_path()
        if path is not None:
            subprocess.Popen(['explorer', str(path.parent)])

    def open_filter_dir(self):
        path = self.get_filter_path()
        if path is not None:
            if path.parent.is_dir():
                subprocess.Popen(['explorer', str(path.parent)])
            else:
                subprocess.Popen(['explorer', str(path.parent.parent)])

    @staticmethod
    def open_dir(path, _):
        subprocess.Popen(['explorer', str(path)])

    def show(self):
        self.setting()
        super().show()


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = Form()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
