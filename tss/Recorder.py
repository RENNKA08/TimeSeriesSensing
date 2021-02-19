import cv2
import json
import tkinter as tk

from pathlib import Path
from PIL import Image, ImageTk
from tkinter import filedialog
from tss import SensorObserver
from tss import TSSFileManager
from typing import Optional, Tuple

class Recorder(tk.Frame):
    """
    レコーダー
    """
    FOURCC = cv2.VideoWriter_fourcc(*'mp4v')

    def __init__(self,
                 sensor_observer: SensorObserver,
                 camera_id: int = 0,
                 frame_width: int = 1920,
                 frame_height: int = 1080,
                 fps: int = 20) -> None:
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

        self.__fps = fps

        # センサオブザーバー
        self.__sensor_observer = sensor_observer
        self.__sensor_observer.add_observe_method(self.__observe)
        self.__sensor_observer.start_observe()

        # ビデオキャプチャ
        self.__video_capture: cv2.VideoCapture = cv2.VideoCapture(camera_id)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.__video_capture.set(cv2.CAP_PROP_FPS, fps)

        # ビデオライター
        self.__video_writer: Optional[cv2.VideoWriter] = None
        
        # ウィジェットの作成・配置
        self.__create_widgets()

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
        # プレビュー画面
        self.__preview_canvas: tk.Canvas = tk.Canvas(self, width=960, height=540)
        self.__preview_canvas.grid(row=0, column=0)

        # コントロールパネル
        controll_panel: tk.Frame = tk.Frame(self, width=240, height=540, background='#2b2c32')
        controll_panel.grid(row=0, column=1)

        ## 録画・録画停止ボタン
        self.__recording_button_label: tk.StringVar = tk.StringVar()
        self.__recording_button_label.set(u'録画開始')
        recording_button: tk.Button = tk.Button(controll_panel,
                                                textvariable=self.__recording_button_label,
                                                command=self.__on_recording_button_clicked)
        recording_button.pack()

        # ログ画面
        log_frame: tk.Frame = tk.Frame(self, width=1200, height=270, background='red')
        log_frame.grid(row=1, column=0)


    def __update(self) -> None:
        """
        画面の更新及び録画を行う
        """
        _, frame = self.__video_capture.read()

        if self.__is_recording:
            self.__video_writer.write(frame)
            self.__current_frame += 1

        self.__buffer = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((960, 540)))

        self.__preview_canvas.create_image(0, 0,
                                           image=self.__buffer,
                                           anchor=tk.NW)

        self.master.after(1, self.__update)


    def __on_recording_button_clicked(self) -> None:
        """
        録画・録画停止ボタンが押された場合の処理
        """
        if self.__is_recording:
            self.__recording_button_label.set(u'録画開始')
            self.__finish_recording()
        else:
            self.__recording_button_label.set(u'録画停止')
            self.__start_recording()


    def __observe(self, data: Tuple) -> None:
        """
        データが観測された際のメソッド
        """
        print(data)

        if self.__is_recording:
            self.__record['data'].append({
                'frame': self.__current_frame,
                'data': list(data)
            })


    def __start_recording(self) -> None:
        """
        録画を開始する
        """
        # ビデオライターの準備
        self.__video_writer = cv2.VideoWriter('~temp.mp4',
                                              Recorder.FOURCC,
                                              self.__fps,
                                              (int(self.__video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                               int(self.__video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        self.__record = {
            'labels': self.__sensor_observer.labels,
            'data': [
            ]
        }

        self.__current_frame = -1
        self.__is_recording = True


    def __finish_recording(self) -> None:
        """
        録画を終了する
        """
        self.__is_recording = False
        self.__video_writer = None

        # センサから取得したデータの記録をjson形式で保存する
        with Path('~temp.json').open(mode='w') as f:
            json.dump(self.__record, f)

        # 記録したデータをtss形式で保存する
        tss_file_manager = TSSFileManager(filedialog.asksaveasfilename(filetypes=[('tss file', '*.tss')], initialfile=u'output.tss'))
        tss_file_manager.save(Path('~temp.mp4'), Path('~temp.json'))


    def __exit(self) -> None:
        """
        終了処理
        """
        if self.__is_recording:
            self.__finish_recording()

        self.__video_capture.release()
        self.__sensor_observer.stop_observe()