# z9 PowerShell Log Analyzer
[English](./README-en.md)
![Z9 Logo](./img/logo.png)

## 概要
PowerShellロギングのイベントログのXMLファイルからマルウェアが実行された痕跡を検出するスクリプトです。

## インストール
```
git clone https://github.com/Sh1n0g1/z9
```

## 使い方

```
usage: z9.py [-h] [--output OUTPUT] [-s] [--no-viewer] [--utf8] input

positional arguments:
  input                 Input file path

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output file path
  -s, --static          Enable Static Analysis mode
  --no-viewer           Disable opening the JSON viewer in a web browser
  --utf8                Read scriptfile in utf-8 (deprecated)
```


### イベントログファイルを解析する（推奨）
```
python z9.py <入力ファイル> -o <出力JSONファイル名>
python z9.py <入力ファイル> -o <出力JSONファイル名> --no-viewer
```
|パラメータ               |       意味                             |
|-------------------------|----------------------------------------|
|`入力ファイル`            |イベントログからエクスポートしたXMLファイル |
|`-o 出力JSONファイル名`   |z9の出力結果のファイル名                  |
|`--no-viewer `           |ビューワを起動しない                      |

例)
```
python z9.py util\log\mwpsop.xml -o sample1.json
```

### PowerShellスクリプトのファイルを静的に解析する
```
python z9.py <入力ファイル> -o <出力JSONファイル名> -s
python z9.py <入力ファイル> -o <出力JSONファイル名> -s --utf8
python z9.py <入力ファイル> -o <出力JSONファイル名> -s --no-viewer
```
|パラメータ               |       意味                             |
|-------------------------|----------------------------------------|
|`入力ファイル`            |PowerShellスクリプト(*.ps1）　　　　　　　 |
|`-o 出力JSONファイル名`   |z9の出力結果のファイル名                  |
|`-s`                     |静的解析を実行する                       |
|`--utf8`                 |入力ファイルが`UTF-8`の時に指定する       |
|`--no-viewer `           |ビューワを起動しない                      |

例)
```
python z9.py malware.ps1 -o sample1.json -s
```

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
