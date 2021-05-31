# Time Series Sensing
## 概要
このアプリケーションの目的は、時系列データをより分かりやすく記録する事です。

動画とセンサからの入力を記録し、どの情報がどのような状況で記録されたかを分かりやすくします。

センサからの入力情報は、その時点で撮影しているフレームに対応付けられるため、リアルタイムで与えられる必要があります。

## 使い方
### モジュールをインストールする
このプロジェクトを`clone`しなくとも、`pip`コマンドを用いて以下のようにモジュールをインストールできます。

```
pip install git+https://github.com/Hara-Yuma/TimeSeriesSensing
```

### 使用するセンサに合ったSensorObserverを作成する
tssを用いれば、任意のセンサ情報を動画データに紐づけて保存することができます。

そのためにはまず、使用するセンサに合った`SensorObserver`を作成する必要があります。

`SensorObserver`は`tss.SensorObserver`を継承することで簡単に作成できます。

```
import tss
from typing import Tuple

class MySensorObserver(tss.SensorObserver):
    def __init__(self) -> None:
        super().__init__(('label1', 'label2'))

    def read_data(self) -> Tuple:
        """
        tss.SensorObserverを継承した場合、
        必ずこのメソッドを実装する必要があります。

        このメソッドはセンサから入力があるまで待機し、
        入力があった場合にデータをラベルに対応したタプル形式で返す
        ようなメソッドです。

        このメソッドが終了しない場合、アプリケーションが正常に終了しません。

        入力状態の待機は、self.is_observingがTrueである場合にのみ継続されるべきです。
        """
```

具体的な例はsample/sample.pyを確認してください。

### 録画する
録画を行うためには，`SensorObserver`を作成する必要があります。

計測を行いたいセンサに合った`SensorObserver`を実装し，`Recorder`クラスに与えることで，
簡単に録画を行うことができます。

詳しいコードの例は，`sample/sample.py`を確認してください。

### 再生する
準備中

### 計測データをCSVファイルとして出力する
計測したデータを，ヘッダー付きのCSVファイルとして出力することができます。

例えば，`data.tss`というファイルをもとに，`output.csv`を出力するには，以下のようなコマンドを実行します。

```
$ python -m tss gencsv data.tss output.csv
```

この時，`output.csv`が既に存在している場合は上書きされるため注意が必要です。

### 計測したデータをMarkDownファイルとして出力する
計測したデータと，それを受信したフレームの画像をまとめたMarkDownファイルを出力することができます。

MarkDownファイルと共に，`images`ディレクトリが自動生成されます。

例えば，`data.tss`というファイルをもとにして，`output/`以下にMarkDownファイルを生成するためには次のように実行します．

```
$ python -m tss genmd data.tss output/
```
