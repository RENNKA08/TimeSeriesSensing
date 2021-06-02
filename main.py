import serial
import tss

from typing import Tuple

LABELS = ('ID', 'No', 'x', 'y', 'z')


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
        super().__init__(LABELS)
        
        self.__serial = serial.Serial(port, baudrate)

    
    def parse_data(self, raw_data) -> Tuple:
        data_str = raw_data.decode()[2:].replace('\r\n', '')
        params = data_str.split(':')

        if len(params) == 1:
            return None

        ret_list = [params[3][3:], params[2][3:]]

        for i in range(3):
            ret_list.append(params[8 + i][2:])
                         
        return tuple(ret_list)


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
    sensor_observer = SerialComObserver('COM4', 115200)

    recorder = tss.Recorder(sensor_observer)
