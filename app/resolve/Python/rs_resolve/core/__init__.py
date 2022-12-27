COLOR_LIST = [
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
]


def timecode2Frame(tc: str, fps):
    int_fps = {
        23: 24,
        29: 30,
        47: 48,
        59: 60,
        95: 96,
        119: 120,
    }
    if fps in int_fps.keys():
        fps = int_fps[fps]
    is_DF = False
    if ';' in tc:
        is_DF = True
        tc = tc.replace(';', ':')
    t = tc.split(':')
    h = int(t[0])
    m = int(t[1]) + (h * 60)
    s = int(t[2]) + (m * 60)
    f = int(t[3]) + (s * fps)
    drop_frames = 0
    if is_DF:
        _f = fps / 15
        drop_frames = _f * (m - (m // 10))
    return f - drop_frames


def get_currentframe(timeline):
    tc: str = timeline.GetCurrentTimecode()
    fps = int(timeline.GetSetting('timelineFrameRate'))
    return timecode2Frame(tc, fps)


def set_currentframe(timeline, frame):
    timeline.SetCurrentTimecode(str(frame))


def get_fps(timeline):
    fps = int(timeline.GetSetting('timelineFrameRate'))
    float_fps = {
        23: 23.976,
        29: 29.97,
        47: 47.952,
        59: 59.94,
        95: 95.904,
        119: 119.88,
    }
    if fps in float_fps.keys():
        fps = float_fps[fps]
    return fps


def track_name2index(timeline, track_type, name):
    for i in range(1, timeline.GetTrackCount(track_type) + 1):
        if timeline.GetTrackName(track_type, i) == name:
            return i
    return 0


if __name__ == '__main__':
    def test(tc: str, fps, frames):
        r = timecode2Frame(tc, fps)
        comment = '%s  %s %d==%d' % (tc, str(fps), frames, r)
        assert r == frames, comment


    test('01:00:00:00', 16, 57600)
    test('01:00:00:00', 18, 64800)
    test('01:00:00:00', 23, 86400)
    test('01:00:00:00', 24, 86400)
    test('01:00:00:00', 25, 90000)
    test('01:00:00:00', 29, 108000)
    test('01:00:00;00', 29, 107892)
    test('01:00:00:00', 30, 108000)
    test('01:00:00:00', 47, 172800)
    test('01:00:00:00', 48, 172800)
    test('01:00:00:00', 50, 180000)
    test('01:00:00:00', 59, 216000)
    test('01:00:00;00', 59, 215784)
    test('01:00:00:00', 60, 216000)
    test('01:00:00:00', 72, 259200)
    test('01:00:00:00', 95, 345600)
    test('01:00:00:00', 96, 345600)
    test('01:00:00:00', 100, 360000)
    test('01:00:00:00', 119, 432000)
    test('01:00:00;00', 119, 431568)
    test('01:00:00:00', 120, 432000)
    print('OK')
