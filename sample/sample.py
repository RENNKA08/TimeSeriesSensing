import serial
import tss

from typing import Tuple


class SerialComObserver(tss.SensorObserver):
    """
    シリアル通信でセンサとやり取りする場合のSensorObserver例
    """

    def __init__(self, port: str, baudrate: int) -> None:
        """
        Parameters
        ----------
        port : str

            シリアル通信で用いるポート

        baudrate : int

            ボーレート
        """
        super().__init__(('No', 'Area1', 'Area2', 'Area3', 'Area4',
                          'Temp', 'AccelX', 'AccelY', 'AccelZ',
                          'GyroX', 'GyroY', 'GyroZ', 'MagX', 'MagY', 'MagZ'))

        self.__data_format = {
            'No':       0x00000000ffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
            'Area1':    0x000000000000000000000000000000ffff0000000000000000000000000000000000000000000000000000000000000000000000000000000000,
            'Area2':    0x0000000000000000000000000000000000ffff000000000000000000000000000000000000000000000000000000000000000000000000000000,
            'Area3':    0x00000000000000000000000000000000000000ffff00000000000000000000000000000000000000000000000000000000000000000000000000,
            'Area4':    0x000000000000000000000000000000000000000000ffff0000000000000000000000000000000000000000000000000000000000000000000000,
            'Temp':     0x000000000000000000000000000000000000000000000000ffff0000000000000000000000000000000000000000000000000000000000000000,
            'AccelX':   0x0000000000000000000000000000000000000000000000000000000000ffff000000000000000000000000000000000000000000000000000000,
            'AccelY':   0x00000000000000000000000000000000000000000000000000000000000000ffff00000000000000000000000000000000000000000000000000,
            'AccelZ':   0x000000000000000000000000000000000000000000000000000000000000000000ffff0000000000000000000000000000000000000000000000,
            'GyroX':    0x0000000000000000000000000000000000000000000000000000000000000000000000ffff000000000000000000000000000000000000000000,
            'GyroY':    0x00000000000000000000000000000000000000000000000000000000000000000000000000ffff00000000000000000000000000000000000000,
            'GyroZ':    0x000000000000000000000000000000000000000000000000000000000000000000000000000000ffff0000000000000000000000000000000000,
            'MagX':     0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000ffff000000000000000000000000000000,
            'MagY':     0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffff00000000000000000000000000,
            'MagZ':     0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffff0000000000000000000000
        }

        self.__labels = tuple(self.__data_format.keys())

        self.__serial = serial.Serial(port, baudrate)

    def extract_data(self, data: int, position_indicator: int) -> int:
        """
        データから指定した部分の値を抜き出す

        Parameters
        ----------
        data : int

            抜き出す元のデータ

        position_indicator : int

            抜き出す部分のbitを1、それ以外のbitを0とした値

        Returns
        ----------
        extracted_data : int

            抜き出されたデータ
        """
        while position_indicator & 1 == 0:
            position_indicator >>= 1
            data >>= 1

        extracted_data = data & position_indicator

        most_significant_bit = extracted_data - \
            (extracted_data & (position_indicator >> 1))

        if most_significant_bit != 0:
            extracted_data -= most_significant_bit << 1

        return extracted_data

    def parse_data(self, raw_data: bytes) -> Tuple:
        """
        受信したデータをパースする

        raw_data : bytes

            受信できた生のデータ
        """
        data = int(raw_data.decode()[1:], 16)

        result_list = []

        for label in self.__data_format.keys():
            result_list.append(self.extract_data(
                data, self.__data_format[label]))

        temp_index = self.__labels.index('Temp')

        result_list[temp_index] *= (0.125 / 64)
        result_list[temp_index] += 26.75

        return tuple(result_list)

    def read_data(self) -> Tuple:
        """
        データを読み出す

        Returns
        ----------
        data : Tuple

            読みだしたデータ
        """
        raw_data = self.__serial.readline()

        return self.parse_data(raw_data)


if __name__ == '__main__':
    sensor_observer = SerialComObserver('COM3', 115200)

    recorder = tss.Recorder(sensor_observer)
