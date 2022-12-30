import math
import xml.etree.ElementTree as ET


class Timeline(object):
    def __init__(self, path):
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.seq = self.root.find('sequence')
        self.tics = self.seq.find('media').find('video').find('format').find('samplecharacteristics')

    def set_name(self, name: str):
        self.root.find('sequence').find('name').text = name

    def set_fps(self, fps: float):
        int_fps = math.floor(fps)
        is_ntsc = False
        ntsc_list = {
            23: 24,
            29: 30,
            47: 48,
            59: 60,
            95: 96,
            119: 120,
        }
        if int_fps in ntsc_list.keys():
            int_fps = ntsc_list[int_fps]
            is_ntsc = True
        tc = self.seq.find('timecode')
        for e in [self.seq, tc, self.tics]:
            e.find('rate').find('timebase').text = str(int_fps)
            e.find('rate').find('ntsc').text = str(is_ntsc).upper()

    def set_width(self, width: int):
        self.tics.find('width').text = str(width)

    def set_height(self, height: int):
        self.tics.find('height').text = str(height)

    def set_dropframe(self, is_dropframe: bool):
        df = self.seq.find('timecode').find('displayformat')
        if is_dropframe:
            df.text = 'DF'
        else:
            df.text = 'NDF'

    def __str__(self):
        return '\n'.join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE xmeml>',
            ET.tostring(self.root, encoding='unicode'),
        ])


if __name__ == '__main__':
    from rs.core import config

    fcp = Timeline(config.DATA_PATH.joinpath('app', 'VoiceDropper', 'Timeline.xml'))
    fcp.set_name('test')
    fcp.set_fps(23.976)
    fcp.set_width(640)
    fcp.set_height(480)
    fcp.set_dropframe(True)
    print(fcp)
