## 使い方
DaVinci Resolve で使える ゆっくり動画補助ツールです。  
[概要動画](https://www.youtube.com/watch?v=CJGFOHqtUkE)
1. 右のReleasesからzipファイルをダウンロードし解凍。
2. りぞりぷと.exeを立ち上げる。
3. 使いたい機能のボタンを押す。
### 目次
* [softalk2wave](#softalk2wave)
* [AssistantSeika2wave](#AssistantSeika2wave)
* [VoiceBin](#VoiceBin)
* [Chara2Resolve](#Chara2Resolve)
* [Macro2Group](#Macro2Group)
* [VTT2Anim](#VTT2Anim)

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
### VoiceBin
動画参照
https://youtu.be/BAn7sj5xbxg

[目次へ](#目次)
### Chara2Resolve
現在Resolve18で動かないようです。ご注意ください。
[nicotalk&キャラ素材配布所](http://www.nicotalk.com/charasozai.html)  
こちらの素材をDaVinci Resolveでそこそこ使えるように変換(自動コンポ)するツールです。  
DaVinci Resolve Studio 17.4.4  
ゆっくり霊夢改(ver1a)、新れいむ(ver5f) で確認しました。
ver4a のものは未確認です。4aと5fは内部がそこそこ違うようで多分あまりよい結果にはなりません。
1. nicotalk&キャラ素材配布所からキャラ素材をダウンロードし解凍。
2. 左上のディレクトリ設定、キャラ素材に解凍した場所を設定。
3. その下の出力先に保存したい場所を設定。 DaVinci Resolve は、ここを参照しますので、後にファイルを動かすとリンク切れになります。
4. DaVinci Resolve を立ち上げ使える状態にする。プログラムからDaVinci Resolve の機能を使うため必要になります。
5. Chara2Resolveにもどり下のexportボタンを押す。ここでcompとsettingファイルを書き出します。
6. (オプション)settingファイルを fusion で改造。
7. installボタンを押しインストール。
8. DaVinci Resolve を立ち上げ直す。installしたものを有効にするため。
9. Effects->Toolbox->Generators->FusionGeneratorsから使用。

DaVinci Resolveでのテンプレートのパラメータについて
- -1 にするとパーツは非表示になります。
- eye_anim, mouth_anim について
  - 0でアニメーションなし
  - 1でループアニメーション
  - 2で待機->アニメーション->待機->アニメーション以下繰り返し
    - 待機時間はアニメ設定で指定した値を以下のように使う。
    - オフセット -> アニメーション -> (休憩 - オフセット) 以下この3つを繰り返し

[目次へ](#目次)
### Macro2Group
動画参照
https://youtu.be/ul7grfLvJCM

[目次へ](#目次)
### VTT2Anim
動画参照
https://youtu.be/zWq4AQeHZ68

[目次へ](#目次)
