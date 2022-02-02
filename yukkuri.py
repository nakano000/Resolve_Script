import os
import subprocess
import pprint
import wave
from pathlib import Path

import DaVinciResolveScript as dvr_script

work_dir = Path('D:/dev/youtube/jimaku')

_word = 'こんばんは'
_word_s = '03_' + (_word[:10] if len(_word) > 10 else _word)

wav_file = work_dir.joinpath(_word_s + '.wav')
# png_file = work_dir.joinpath('dummy2.png')
# mp4_file = work_dir.joinpath(_word_s + '.mp4')

softalk_command = [
    'D:/App/softalk/softalkw.exe',
    '/S:120',
    '/R:' + str(wav_file),
    '/W:' + _word,
]
subprocess.run(softalk_command, shell=True)

# wr = wave.open(str(wav_file), 'rb')
# d = float(wr.getnframes()) / wr.getframerate()
# wr.close()
#
# ffmpeg_command = [
#     'D:/App/ffmpeg-5.0-essentials_build/bin/ffmpeg.exe',
#     '-loop',
#     '1',
#     '-i',
#     str(png_file),
#     '-i',
#     str(wav_file),
#     # '-tune',
#     # 'stillimage',
#     # '-s',
#     # '1920x1080',
#     '-r',
#     '30',
#     '-t',
#     str(d),
#     '-y',
#     str(mp4_file),
#
# ]
# subprocess.run(ffmpeg_command, shell=True)
# popen = subprocess.Popen(_command, shell=True)
# popen.wait()
print('export')
resolve = dvr_script.scriptapp("Resolve")
print('re')
fusion = resolve.Fusion()
projectManager = resolve.GetProjectManager()
mediaStorage = resolve.GetMediaStorage()
pj = projectManager.GetCurrentProject()
mp = pj.GetMediaPool()
root_dir = mp.GetRootFolder()

page = resolve.GetCurrentPage()

clip_list = mediaStorage.AddItemListToMediaPool(str(wav_file).replace('\\', '/'))
clip_list[0].SetClipProperty('Comments', _word)
ctl = pj.GetCurrentTimeline()
tl = mp.CreateTimelineFromClips(_word_s, clip_list)
if ctl:
    pj.SetCurrentTimeline(ctl)

# tli = tl.InsertTitleIntoTimeline('Text+')
tli = tl.InsertFusionTitleIntoTimeline('Text+')
# timelineVideoTrackCount = tl.GetTrackCount("video")
# for i in range(int(timelineVideoTrackCount)):
#     clips = tl.GetItemListInTrack("video", i + 1)
#     for clip in clips:
#         if clip.GetFusionCompCount() < 1:
#             # clip.AddFusionComp()
#             print(clip.GetStart())
#             print(clip.GetEnd())
#             comp = clip.ImportFusionComp('D:/dev/youtube/jimaku/aaa.comp')
#             t = comp.FindTool('Text1')
#             t.SetInput('StyledText', _word)
resolve.OpenPage(page)
