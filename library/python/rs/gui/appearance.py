
from PySide2.QtGui import (
    QPalette,
    QColor,
)
from PySide2.QtCore import (
    Qt,
)

stylesheet = '\n'.join(
    [
        '* {font: 14px "Consolas";}',
        'QMenu {font: 12px "Arial";}',
        'QMenu { background-color: #2b2b2b; }',
        'QMenu::item:disabled { color: #606060; }',
        'QMenu::item:selected { background-color: #0a64b4; }',
    ]
)

in_stylesheet = '\n'.join(
    [
        'background-color: #2f5d50;',
        'color: rgb(255, 255, 255);',
    ]
)
ex_stylesheet = '\n'.join(
    [
        'background-color: #74325c;',
        'color: rgb(255, 255, 255);',
    ]
)


def _get_palette():
    text_color: QColor = QColor(210, 210, 210)
    base_color: QColor = QColor(40, 40, 46)
    p = QPalette()
    p.setColor(QPalette.Window, base_color)
    p.setColor(QPalette.WindowText, text_color)
    p.setColor(QPalette.Base, QColor(23, 24, 26))
    p.setColor(QPalette.AlternateBase, base_color)
    p.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    p.setColor(QPalette.ToolTipText, text_color)
    p.setColor(QPalette.Text, text_color)
    p.setColor(QPalette.Button, base_color)
    p.setColor(QPalette.ButtonText, text_color)
    p.setColor(QPalette.BrightText, Qt.red)

    p.setColor(QPalette.Disabled, QPalette.Base, QColor(80, 80, 80))
    p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(140, 140, 140))
    p.setColor(QPalette.Disabled, QPalette.WindowText, QColor(140, 140, 140))
    p.setColor(QPalette.Disabled, QPalette.Text, QColor(190, 190, 190))

    p.setColor(QPalette.Highlight, QColor(10, 100, 180))
    p.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    return p


palette = _get_palette()
