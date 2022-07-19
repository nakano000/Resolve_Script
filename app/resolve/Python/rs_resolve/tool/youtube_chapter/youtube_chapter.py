import dataclasses
import sys
from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QStringListModel,
    QItemSelectionModel,
)
from PySide2.QtWidgets import (
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

from rs_resolve.tool.youtube_chapter.youtube_chapter_ui import Ui_MainWindow

APP_NAME = 'Youtubeチャプター'


@dataclasses.dataclass
class ConfigData(config.Data):
    title: str = '目次'
    delimiter: str = '-'
    color: str = 'Rose'


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
                QItemSelectionModel.SelectCurrent | QItemSelectionModel.Rows
            )


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
        self.resize(450, 450)
        self.fusion = fusion

        # list view
        m = QStringListModel()
        m.setStringList([
            'Blue',
            'Cyan',
            'Green',
            'Yellow',
            'Red',
            'Pink',
            'Purple',
            'Fuchsia',
            'Rose',
            'Lavender',
            'Sky',
            'Mint',
            'Lemon',
            'Sand',
            'Cocoa',
            'Cream',
        ])
        self.ui.markerListView.setModel(m)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # button
        self.ui.copyButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.makeButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.makeButton.clicked.connect(self.make)
        self.ui.copyButton.clicked.connect(self.copy)
        self.ui.closeButton.clicked.connect(self.close)

    def make(self):
        v = self.ui.chapterPlainTextEdit
        data = self.get_data()
        delim = (' %s ' % data.delimiter).replace('  ', ' ')

        resolve = self.fusion.GetResolve()
        projectManager = resolve.GetProjectManager()

        project = projectManager.GetCurrentProject()
        if project is None:
            v.setPlainText('Projectが見付かりません。')
            return

        timeline = project.GetCurrentTimeline()
        if timeline is None:
            v.setPlainText('Timelineが見付かりません。')
            return

        fps = timeline.GetSetting('timelineFrameRate')
        m: dict = timeline.GetMarkers()

        lst = [data.title]
        for key in m:
            if m[key]['color'] == data.color:
                sec = round(key / fps)
                minute, sec = divmod(sec, 60)
                hour, minute = divmod(minute, 60)
                tc = '%02d:%02d' % (minute, sec)
                if hour > 0:
                    tc = '%02d:%s' % (hour, tc)
                if len(lst) == 1 and tc != '00:00':  # タイトルが入っているので  == 1
                    lst.append('00:00' + delim)
                lst.append(tc + delim + m[key]['name'])

        v.setPlainText('\n'.join(lst))

    def copy(self):
        QApplication.clipboard().setText(self.ui.chapterPlainTextEdit.toPlainText())

    def set_data(self, c: ConfigData):
        self.ui.titleLineEdit.setText(c.title)
        self.ui.delimiterLineEdit.setText(c.delimiter)
        select(self.ui.markerListView, [c.color])

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.title = self.ui.titleLineEdit.text().strip()
        c.delimiter = self.ui.delimiterLineEdit.text().strip()

        # c.color
        v = self.ui.markerListView
        m: QStringListModel = v.model()
        lst = v.selectionModel().selectedIndexes()
        c.color = m.data(lst[0]) if len(lst) > 0 else ''

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


if __name__ == '__main__':
    pass
