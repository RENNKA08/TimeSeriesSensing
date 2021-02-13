import tss

def launch_recorder() -> None:
    """
    レコーダーを起動する
    """
    recorder = tss.Recorder()
    recorder.mainloop()


if __name__ == '__main__':
    launch_recorder()