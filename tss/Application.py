import tkinter as tk

class Application(tk.Frame):
    """
    アプリケーション
    """
    def __init__(self, master: tk.Misc):
        """
        Parameters
        ----------
        master : tk.Misc

            アプリケーションのメインウィンドウとなるトップレベルウィジェット
        """
        super().__init__(master)
        self.master = master
        self.pack()