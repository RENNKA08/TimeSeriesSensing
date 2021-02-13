# Time Series Sensing
## 概要
このアプリケーションの目的は、時系列データをより分かりやすく記録する事です。

動画とセンサからの入力を記録し、どの情報がどのような状況で記録されたかを分かりやすくします。

センサからの入力情報は、その時点で撮影しているフレームに対応付けられるため、リアルタイムで与えられる必要があります。

## 使い方
### モジュールをインストールする
このプロジェクトをcloneしなくとも、pipコマンドを用いて以下のようにモジュールをインストールできます。

```
pip install git+https://github.com/Hara-Yuma/TimeSeriesSensing
```

### 使用するセンサに合ったSensorObserverを作成する
tssを用いれば、任意のセンサ情報を動画データに紐づけて保存することができます。

そのためにはまず、使用するセンサに合ったSensorObserverを作成する必要があります。

SensorObserverはtss.SensorObserverを継承することで簡単に作成できます。

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
準備中

### 再生する
準備中