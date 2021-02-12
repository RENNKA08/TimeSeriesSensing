import cv2
import numpy as np
import threading

from typing import Optional, Tuple

class CameraController:
    """
    カメラの操作を行うためのクラス
    """
    FOURCC = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    def __init__(self, camera_id: int = 0) -> None:
        """
        Parameters
        ----------
        camera_id : int
        
            使用するカメラのID．
        """
        self.__video_capture = cv2.VideoCapture(camera_id)
        self.__video_writer = None

        self.__fps = self.__video_capture.get(cv2.CAP_PROP_FPS)
        self.__frame_size = (int(self.__video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                             int(self.__video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        self.__is_capturing = False
        self.__is_recording = False

        self.__frame_buffer: Optional[np.ndarray] = None

        self.__capturing_thread: Optional[threading.Thread] = None


    def __del__(self) -> None:
        self.__video_capture.release()


    @property
    def fps(self) -> float:
        """
        Returns
        ----------
        fps : float

            カメラのFPS
        """
        return self.__fps


    @property
    def frame_size(self) -> Tuple[int, int]:
        """
        Returns
        ----------
        frame_size : Tuple[int, int]

            フレームサイズ(横幅, 縦幅)
        """
        return self.__frame_size


    @property
    def is_capturing(self) -> bool:
        """
        Returns
        ----------
        is_capturing : bool

            キャプチャしているかどうか
        """
        return self.__is_capturing


    @property
    def is_recording(self) -> bool:
        """
        Returns
        ----------
        is_recording : bool

            録画しているかどうか
        """
        return self.__is_recording


    @property
    def frame_buffer(self) -> Optional[np.ndarray]:
        """
        キャプチャした画像が一時的に格納されるバッファ
        """
        return self.__frame_buffer


    def __capture(self) -> None:
        """
        キャプチャする。

        フレームを取得し、バッファを書き換える。
        """
        while self.is_capturing:
            _, self.__frame_buffer = self.__video_capture.read()

            if self.is_recording:
                self.__video_writer.write(self.frame_buffer)


    def start_capture(self) -> None:
        """
        キャプチャを開始する
        """
        if self.is_capturing:
            return

        self.__capturing_thread = threading.Thread(target=self.__capture)

        self.__is_capturing = True
        self.__capturing_thread.start()


    def start_recording(self, output_path: str) -> None:
        """
        録画を開始する

        Parameters
        ----------
        output_path : str

            ビデオファイルの出力先へのパス
        """
        if not self.is_capturing or self.is_recording:
            return

        self.__video_writer = cv2.VideoWriter(output_path, CameraController.FOURCC, self.fps, self.frame_size)
        self.__is_recording = True


    def stop_capture(self) -> None:
        """
        キャプチャを終了する。

        録画が途中である場合は、中断される。
        """
        if not self.is_capturing:
            return

        if self.is_recording:
            self.stop_recording()

        self.__is_capturing = False
        self.__capturing_thread.join()

        self.__frame_buffer = None


    def stop_recording(self) -> None:
        """
        録画を停止する
        """
        self.__is_recording = False
        self.__video_writer = None