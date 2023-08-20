import subprocess
import time
from typing import List

from PySide6.QtCore import (
    QObject,
    Signal,
)


class Player(QObject):
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_canceled = False
        self.exe_path: str = ''
        self.data: List[dict] = []

    def play(self):
        for d in self.data:
            if self.is_canceled:
                break
            command: List[str] = [
                str(self.exe_path),
                '/T',
                d['text'].replace('\n', ' '),
                '/P',
                d['chara'],
            ]
            pro = subprocess.Popen(command)
            while not self.is_canceled and pro.poll() is None:
                time.sleep(0.01)
            if pro.poll() is None:
                pro.kill()
        self.finished.emit()

    def export(self):
        for d in self.data:
            command: List[str] = [
                str(self.exe_path),
                '/T',
                d['text'].replace('\n', ' '),
                '/P',
                d['chara'],
                '/W',
                str(d['wav_file']),
            ]
            subprocess.run(command)
            with d['txt_file'].open('w', encoding='utf-8-sig', newline='\n') as f:
                f.write(d['subtitle'])
        self.finished.emit()

    def stop(self):
        self.is_canceled = True


if __name__ == '__main__':
    a = Player()
    a.exe_path = 'D:/App/aquestalkplayer_20220822/aquestalkplayer/AquesTalkPlayer.exe'
    a.data = [
        {
            'chara': 'れいむ',
            'text': 'おはようございます。',
        },
        {
            'chara': 'まりさ',
            'text': 'こんばんは',
        },
    ]
    a.play()
