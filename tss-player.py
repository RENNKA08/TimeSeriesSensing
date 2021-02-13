import tss

def launch_player() -> None:
    """
    プレイヤーを起動する

    TODO: ファイルを引数から指定して開く機能を追加する
    """
    player = tss.Player()
    player.mainloop()


if __name__ == '__main__':
    launch_player()