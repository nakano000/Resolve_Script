import sys

from PySide6.QtCore import (
    Qt,
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

from rs_resolve.core import (
    shortcut as sc,
)

from rs_resolve.gui.shortcut.shortcut_ui import Ui_MainWindow
from rs_resolve.gui import (
    get_resolve_window,
    activate_window,
)

APP_NAME = 'Shortcut'


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
        self.resize(500, 100)
        self.fusion = fusion

        # style sheet
        self.ui.razorTestButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.deselectAllTestButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.activeTimelinePanelTestButton.setStyleSheet(appearance.other_stylesheet)

        self.ui.setButton.setStyleSheet(appearance.ex_stylesheet)

        # event
        self.ui.razorTestButton.clicked.connect(self.razor_test)
        self.ui.deselectAllTestButton.clicked.connect(self.deselect_all_test)
        self.ui.activeTimelinePanelTestButton.clicked.connect(self.active_timeline_panel_test)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.setButton.clicked.connect(self.set_shortcut)

        #
        self.ui.setButton.setFocus()

    def get_resolve_window(self):
        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()
        project = projectManager.GetCurrentProject()
        if project is None:
            print('Project not found.')
            return None
        return get_resolve_window(project.GetName())

    def razor_test(self):
        c = self.get_data()
        w = self.get_resolve_window()
        activate_window(w)
        c.razor()

    def deselect_all_test(self):
        c = self.get_data()
        w = self.get_resolve_window()
        activate_window(w)
        c.deselect_all()

    def active_timeline_panel_test(self):
        c = self.get_data()
        w = self.get_resolve_window()
        activate_window(w)
        c.active_timeline_panel()

    def set_data(self, c: sc.Data):
        self.ui.razorLineEdit.setText(' '.join(c.key_razor))
        self.ui.deselectAllLineEdit.setText(' '.join(c.key_deselect_all))
        self.ui.activeTimelinePanelLineEdit.setText(' '.join(c.key_active_timeline_panel))

    def get_data(self) -> sc.Data:
        c = sc.Data()
        c.key_razor = p.pipe(
            self.ui.razorLineEdit.text().split(),
            p.map(p.call.lower()),
            tuple,
        )
        c.key_deselect_all = p.pipe(
            self.ui.deselectAllLineEdit.text().split(),
            p.map(p.call.lower()),
            tuple,
        )
        c.key_active_timeline_panel = p.pipe(
            self.ui.activeTimelinePanelLineEdit.text().split(),
            p.map(p.call.lower()),
            tuple,
        )
        return c

    def load_config(self) -> None:
        c = sc.Data()
        if sc.CONFIG_FILE.is_file():
            c.load(sc.CONFIG_FILE)
        self.set_data(c)

    def save_config(self) -> None:
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        c = self.get_data()
        c.save(sc.CONFIG_FILE)

    def set_shortcut(self):
        self.save_config()
        self.close()

    def show(self) -> None:
        self.load_config()
        super().show()


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
