import threading

from abc import ABCMeta, abstractmethod
from typing import Callable, List, Optional, Tuple


class SensorObserver(metaclass=ABCMeta):
    """
    センサとの通信を監視するためのクラス
    """

    def __init__(self, labels: Tuple[str, ...]) -> None:
        self.__labels = labels
        self.__observe_methods: List[Callable[[Tuple], None]] = []

        self.__is_observing = False

        self.__observing_thread: Optional[threading.Thread] = None

    @property
    def labels(self) -> Tuple[str, ...]:
        """
        Returns
        ----------
        labels : Tuple[str, ...]

            取得されるデータのラベル。
        """
        return self.__labels

    @property
    def is_observing(self) -> bool:
        """
        Returns
        ----------
        is_observing : bool

            監視中であるかどうか
        """
        return self.__is_observing

    def __observe(self) -> None:
        """
        センサとの通信を監視し、入力があった際に通知する。
        """
        while self.__is_observing:
            data = self.read_data()

            self.__notity(data)

    def __notity(self, data: Tuple) -> None:
        """
        Parameters
        ----------
        data : Tuple

            センサからの入力。

            labelsに対応したデータが格納されている必要がある。
        """
        for observe_method in self.__observe_methods:
            observe_method(data)

    def add_observe_method(self, observe_method: Callable[[Tuple], None]) -> None:
        """
        センサからの入力があった際に呼び出されるメソッドを追加する

        Parameters
        ----------
        observe_method : Callable[[Tuple], None]

            センサからの入力が合った際に呼び出されるメソッド
        """
        self.__observe_methods.append(observe_method)

    def start_observe(self) -> None:
        """
        センサとの通信の監視を開始する
        """
        self.__observing_thread = threading.Thread(target=self.__observe)

        self.__is_observing = True
        self.__observing_thread.start()

    def stop_observe(self) -> None:
        """
        センサとの通信の監視を終了する
        """
        self.__is_observing = False
        self.__observing_thread.join()

    @abstractmethod
    def read_data(self) -> Tuple:
        """
        データを読み取るためのメソッド。

        Returns
        ----------
        data : Tuple

            入力されたデータ。

            labelsに対応している必要がある。
        """
        pass
