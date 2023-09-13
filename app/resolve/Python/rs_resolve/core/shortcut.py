import dataclasses
from pathlib import Path

import pyautogui

from rs.core import config, util

CONFIG_FILE: Path = config.CONFIG_DIR.joinpath('Shortcut.json')


@dataclasses.dataclass
class Data(config.Data):
    key_razor: tuple = ('ctrl', 'b') if not util.IS_MAC else ('command', 'b')
    key_deselect_all: tuple = ('ctrl', 'shift', 'a') if not util.IS_MAC else ('command', 'shift', 'a')
    key_active_timeline_panel: tuple = ('ctrl', '4') if not util.IS_MAC else ('command', '4')

    def razor(self):
        pyautogui.hotkey(*self.key_razor)

    def deselect_all(self):
        pyautogui.hotkey(*self.key_deselect_all)

    def active_timeline_panel(self):
        pyautogui.hotkey(*self.key_active_timeline_panel)

    def load(self, path: Path) -> None:
        super().load(path)
        self.key_razor = tuple(self.key_razor)
        self.key_deselect_all = tuple(self.key_deselect_all)
        self.key_active_timeline_panel = tuple(self.key_active_timeline_panel)


if __name__ == '__main__':
    org_data = Data()
    if CONFIG_FILE.exists():
        org_data.load(CONFIG_FILE)
    config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # save
    data = Data()
    data.key_razor = ('ctrl', 'a')
    data.save(CONFIG_FILE)
    print('data:', data)

    # load
    data2 = Data()
    data2.load(CONFIG_FILE)
    print('data2:', data2)

    #
    org_data.save(CONFIG_FILE)
    print('org_data:', org_data)
