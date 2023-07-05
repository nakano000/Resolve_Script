## 使い方

DaVinci Resolve で使える 動画制作補助ツールです。  
日本語のフォルダに入れると動きません。ご注意ください。

1. 右のReleasesからzipファイルをダウンロードし解凍。
2. (オプション)アップグレードの場合は旧ツールからconfigフォルダをコピー
3. りぞりぷと.exeを立ち上げる。
4. 使いたい機能のボタンを押す。

参考
立ち絵、口パクの作り方
https://youtu.be/WyKujodsLh0

### 目次

* [ResolveLauncher](#ResolveLauncher)
* [softalk2wave](#softalk2wave)
* [AssistantSeika2wave](#AssistantSeika2wave)
* [AquesTalkWrapper](#AquesTalkWrapper)
* [VoiceBin](#VoiceBin)
* [VoiceSync](#VoiceSync)
* [PsdSplitter](#PsdSplitter)
* [Macro2Group](#Macro2Group)
* [VTT2Anim](#VTT2Anim)
* [ScriptLauncher](#ScriptLauncher)
* [DiskCache](#DiskCache)
* [Characters](#Characters)
* [Linuxで使う](#Linuxで使う)

### ResolveLauncher

動画参照
https://youtu.be/MfRBx0_7ZB4

動画参照
https://youtu.be/hrrWekhWuYY

[目次へ](#目次)

### softalk2wave

音声と字幕ファイル(srt)を書き出します。  
簡単に書き出しからDaVinci ResolveのEdit pageへドラッグアンドドラップするのが目的のツールです。  
SofTalkが別途必要です。

1. 右上の softalkw.exe の場所の欄に softalkw.exe の場所を設定。 softalkw.exe はソフトークに同封されています。
2. その下の保存ディレクトリにwavとsrtファイルの保存先ディレクトリを設定。
3. 音声設定にしゃべらせたい文字を入力。
4. 下のexportボタンを押す。ここでwavとsrtファイルを書き出します。
5. 左のファイル一覧から wavとsrtファイルを DaVinci Resolve の Edit page へ、ドラッグアンドドラップする。

[目次へ](#目次)

### AssistantSeika2wave

音声と字幕ファイル(srt)を書き出します。  
簡単に書き出しからDaVinci ResolveのEdit pageへドラッグアンドドラップするのが目的のツールです。  
AssistantSeika、他音声読み上げソフトが必要です。

1. AssistantSeika を使えるよう設定し立ち上げ。
2. 右上の SeikaSay2.exe の場所の欄に SeikaSay2.exe の場所を設定。 SeikaSay2.exe は AssistantSeika に同封されています。
3. その下の保存ディレクトリにwavとsrtファイルの保存先ディレクトリを設定。
4. 音声設定にしゃべらせたい文字を入力。
5. 音声設定の右側を AssistantSeika の話者一覧を見ながら設定。 Template があればそれを使っても可。
6. 下のexportボタンを押す。ここでwavとsrtファイルを書き出します。
7. 左のファイル一覧から wavとsrtファイルを DaVinci Resolve の Edit page へ、ドラッグアンドドラップする。

[目次へ](#目次)

### AquesTalkWrapper

AquesTalkPlayerをラップして使いやすくします。

[目次へ](#目次)

### VoiceBin

動画参照
https://youtu.be/BAn7sj5xbxg

動画参照
https://youtu.be/afiJp1lodMo

動画参照
https://youtu.be/5Q6WNtMFhWI

[目次へ](#目次)

### VoiceSync

動画参照
https://youtu.be/Y5KpnlWsqmo

[目次へ](#目次)

### PsdSplitter

動画参照
https://youtu.be/LHM6jDKnLng

[目次へ](#目次)

### Macro2Group

動画参照
https://youtu.be/ul7grfLvJCM

[目次へ](#目次)

### VTT2Anim
2.0.0で一時無効化しました。<br>
Subtitle2TextPlusを使ってください。<br>
Workspase->Scripts->(Edit)->RS->Subtitle2TextPlus<br>

[目次へ](#目次)

### ScriptLauncher

動画参照
https://youtu.be/5h5jIBJ4Lmo

動画参照
https://youtu.be/ZwZyUCaTaTw

[目次へ](#目次)

### DiskCache

動画参照
https://youtu.be/kta_94REcEE

[目次へ](#目次)

### Characters

コピー用の文字を表示します。

[目次へ](#目次)

### Linuxで使う

検証不足です。ご注意ください。<br>
下記環境にて確認しています。
(りぞりぷと 2.0.0からpythonは3.10.11に変更しました。)

- りぞりぷと 1.x.x
- CentOS Linux release 7.9.2009 (Core)
- python 3.6.8
- DaVinci Resolve 18.02

#### python3.6をダビンチリゾルブに認識させる。

```
cd /lib64
sudo ln -s libpython3.6m.so.1.0 libpython3.6.so.1.0
sudo ldconfig
```

#### python3に必要なライブラリを入れる。

りぞりぷと を解凍したフォルダ内で

```
sudo pip3 install --upgrade pip
pin3 install -r requirements.txt
```

#### りぞりぷと を立ち上げる

```
python3 bin/launcher.py
```

[目次へ](#目次)
