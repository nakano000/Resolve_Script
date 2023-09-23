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


def get_track_names(timeline, track_type):
    r = []
    for i in range(1, timeline.GetTrackCount(track_type) + 1):
        r.append(timeline.GetTrackName(track_type, i))
    return r


def get_item(timeline, track_type, index, frame=None):
    if frame is None:
        frame = get_currentframe(timeline)
    lst = timeline.GetItemListInTrack(track_type, index)
    if lst is None:
        return None
    for item in lst:
        if item.GetStart() <= frame < item.GetEnd():
            return item
    return None


def get_track_item_count(timeline, track_type, index):
    lst = timeline.GetItemListInTrack(track_type, index)
    if lst is None:
        return 0
    return len(lst)


class LockOtherTrack:
    def __init__(self, timeline, index, track_type='video', enable=True):
        self.timeline = timeline
        self.index = index
        self.track_type = track_type
        self.enable = enable
        self.__lock_state = {}
        self.__TYPE_LIST = ['video', 'audio', 'subtitle']
        for _track_type in self.__TYPE_LIST:
            self.__lock_state[_track_type] = {}

    def __enter__(self):
        if self.enable:
            for _track_type in self.__TYPE_LIST:
                for i in range(1, self.timeline.GetTrackCount(_track_type) + 1):
                    self.__lock_state[_track_type][i] = self.timeline.GetIsTrackLocked(_track_type, i)
                    if i == self.index and _track_type == self.track_type:
                        self.timeline.SetTrackLock(_track_type, i, False)
                    else:
                        self.timeline.SetTrackLock(_track_type, i, True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.enable:
            for _track_type in self.__TYPE_LIST:
                for i in range(1, self.timeline.GetTrackCount(_track_type) + 1):
                    self.timeline.SetTrackLock(_track_type, i, self.__lock_state[_track_type][i])


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
