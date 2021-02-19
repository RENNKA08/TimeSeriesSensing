from __future__ import annotations
import zipfile

from pathlib import Path
from typing import Optional

class TSSFileManager:
    """
    .tss形式のファイルを管理するためのクラス
    """
    def __init__(self, file_path: Path) -> None:
        """
        Parameters
        ----------
        file_path : Path

            tss形式のファイルへのパス
        """
        self.__file_path = file_path

    
    def save(self,
             movie_file_path: Path,
             record_file_path: Path,
             delete_original_files: bool = True) -> None:
        """
        .tss形式のファイルを保存する

        Parameters
        ----------
        movie_file_path : Path

            mp4形式の動画ファイルへのパス

        record_file_path : Path

            センサから取得したデータの記録ファイルへのパス

        delete_original_files: bool

            元の動画ファイルとセンサ情報記録ファイルを削除するか
        """
        with zipfile.ZipFile(self.__file_path, 'w', compression=zipfile.ZIP_DEFLATED) as f:
            f.write(movie_file_path, arcname='movie.mp4')
            f.write(record_file_path, arcname='data.json')

        if delete_original_files:
            movie_file_path.unlink()
            record_file_path.unlink()


    def exportAsCSV(self,
                    start_frame: Optional[int] = None,
                    end_frame: Optional[int] = None) -> None:
        """
        計測データをCSV形式で出力する

        Parameters
        ----------
        file_path : Path

            出力先のファイルへのパス

        start_frame : Optional[int]

            出力する範囲の開始フレーム番号

        end_frame : Optional[int]

            出力する範囲の終了フレーム番号
        """
        pass