import cv2
import tkinter as tk

from PIL import Image, ImageTk
from tss import SensorObserver

class Recorder(tk.Frame):
    """
    レコーダー
    """
    FOURCC = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    def __init__(self,
                 sensor_observer: SensorObserver,
                 camera_id: int = 0,
                 frame_width: int = 1920,
                 frame_height: int = 1080,
                 fps: int = 30) -> None:
        """
        Parameters
        ----------
        sensor_observer : SensorObserver

            センサとの通信を監視するためのクラス

        camera_id : int

            使用するカメラID
        """
        super().__init__(tk.Tk('TSS Recorder'))
        self.pack()

        self.master.resizable(width=False, height=False) # type: ignore

        # ビデオキャプチャ
        self.__video_capture: cv2.VideoCapture = cv2.VideoCapture(camera_id)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.__video_capture.set(cv2.CAP_PROP_FPS, fps)

        self.__create_widgets()

        # バッファ
        self.__buffer = None

        # 現在録音中であるかのフラグ
        self.__is_recording: bool = False

        # update
        self.__update()

        # メインループに入る
        self.master.mainloop()

        # メインループを抜けたら終了処理
        self.__exit()


    def __create_widgets(self) -> None:
        """
        ウィジェットを配置する
        """
        # プレビュー画面 + コントロールパネル
        vbox: tk.Frame = tk.Frame(self)
        vbox.pack()

        # プレビュー画面
        self.__preview_canvas: tk.Canvas = tk.Canvas(vbox, width=960, height=540)
        self.__preview_canvas.pack(side='left')

        # コントロールパネル
        controll_panel: tk.Frame = tk.Frame(vbox, width=240, height=540, background='#2b2c32')
        controll_panel.pack(side='right')

        # ログ画面
        log_frame: tk.Frame = tk.Frame(self, width=1200, height=270, background='red')
        log_frame.pack()

    
    def __update(self) -> None:
        """
        画面の更新及び録画を行う
        """
        _, frame = self.__video_capture.read()

        self.__buffer = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((960, 540)))

        self.__preview_canvas.create_image(0, 0,
                                           image=self.__buffer,
                                           anchor=tk.NW)

        self.master.after(15, self.__update)


    def __start_recording(self) -> None:
        """
        録画を開始する
        """
        pass


    def __finish_recording(self) -> None:
        """
        録画を終了する
        """
        pass


    def __exit(self) -> None:
        """
        終了処理
        """
        self.__video_capture.release()