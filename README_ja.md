# z9 PowerShell Log Analyzer
[English](./README-en.md)
![Z9 Logo](./img/logo.png)

## 概要
PowerShellロギングのイベントログのXMLファイルからマルウェアが実行された痕跡を検出するスクリプトです。

## 必要要件
Python 3+

## インストール
```
git clone https://github.com/Sh1n0g1/z9
cd z9
pip install -r requirements.txt
```

## オンラインデモ
[https://z9.shino.club/](https://z9.shino.club/)
* サンドボックスも動作中

## 使い方
```
python z9.py <XMLファイル>
python z9.py <XMLファイル> <出力用JSONファイル>
```
出力されたJSONファイルは`viewer.html`で可視化できます。

## XMLファイルの準備の仕方
### PowerShellログインを有効にする方法
1. [`util/enable_powershell_logging.reg`](./util/enable_powershell_logging.reg)を対象端末で右クリックし、「結合」を選択する
2. 再起動をする
3. 以降、PowerShellスクリプトを実行するとすべてイベントログに記録される

### イベントログからXMLファイルを取得する
1. [`util/collect_psevent.bat`](./util/collect_psevent.bat)を実行する
2. `util/log`下にログが生成される
3. いずれのXMLファイルも本ツールにて精査が可能である

### イベントログを削除する方法
PowerShellのイベントログはどんどん蓄積されるため、特定のスクリプトのみのログが見たい場合は、一旦過去のログを削除する必要がある。
* [`util/collect_psevent.bat`](./util/clear_psevent.bat)を管理者権限で実行する


## 開発者
[hanataro-miz](https://github.com/hanataro-miz)  
[si-tm](https://github.com/si-tm)  
[take32457](https://github.com/take32457)  
[Bigdrea6](https://github.com/Bigdrea6)  
[azaberrypi](https://github.com/azaberrypi)  
[Sh1n0g1](https://github.com/Sh1n0g1)  
