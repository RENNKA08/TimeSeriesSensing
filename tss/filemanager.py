from __future__ import annotations

import json
import shutil
import zipfile

from pathlib import Path
from typing import Optional

class TSSFileManager:
    """
    .tss形式のファイルを管理するためのクラス
    """

    class FileAlreadyExistsError(BaseException):
        """
        ファイルが既に存在していたことを知らせる例外クラス
        """
        pass


    class AutoExtractFailedError(BaseException):
        """
        自動解凍に失敗したことを知らせる例外クラス
        """
        pass


    def __init__(self, file_path: Path) -> None:
        """
        Parameters
        ----------
        file_path : Path

            tss形式のファイルへのパス
        """
        self.__file_path: Path = file_path

        self.__extracted_file_path: Optional[Path] = None

    
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

        delete_original_files : bool

            元の動画ファイルとセンサ情報記録ファイルを削除するか
        """
        with zipfile.ZipFile(self.__file_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
            zip.write(movie_file_path, arcname='movie.mp4')
            zip.write(record_file_path, arcname='data.json')

        if delete_original_files:
            movie_file_path.unlink()
            record_file_path.unlink()


    def extract(self, dir_path: Path, exists_ok: bool = False) -> None:
        """
        .tss形式のファイルを解凍する

        Parameters
        ----------
        dir_path : Path

            解凍先のフォルダへのパス

        exists_ok : bool

            解凍先のフォルダが存在した場合に上書きするかどうか

        Raises
        ----------
        FileNotFoundError

            解凍元として指定されているtssファイルが存在しないことを知らせる例外

        FileAlreadyExistsError

            解凍先として指定されているディレクトリが既に存在していたことを知らせる例外
        """
        if not self.__file_path.exists():
            raise FileNotFoundError()

        if exists_ok:
            shutil.rmtree(dir_path)
        elif dir_path.exists():
            raise TSSFileManager.FileAlreadyExistsError()

        with zipfile.ZipFile(self.__file_path) as zip:
            zip.extractall(dir_path)

        self.__extracted_file_path = dir_path


    def exportAsCSV(self,
                    file_path: Path,
                    start_frame: Optional[int] = None,
                    end_frame: Optional[int] = None,
                    exists_ok: bool = False) -> None:
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

        exists_ok : bool

            指定されたファイルが存在している場合に上書きするかどうか

        Raises
        ----------
        FileNotFoundError

            指定されているtssファイルが存在しないことを知らせる例外

        AutoExtractFailedError

            ~tempディレクトリが既に存在しており，自動解凍に失敗したことを知らせる例外

        FileAlreadyExistsError

            出力先として指定されたファイルが既に存在していたことを知らせる例外     
        """
        if self.__extracted_file_path is None:
            try:
                self.extract(Path('~temp'))
            except FileNotFoundError as e:
                raise e
            except TSSFileManager.FileAlreadyExistsError as e:
                raise TSSFileManager.AutoExtractFailedError()
        
        with (self.__extracted_file_path / 'data.json').open(mode='r') as f:
            data = json.load(f)

        shutil.rmtree(Path('~temp'))

        csv = ','.join(data['labels']) + '\n'

        if start_frame is None:
            start_frame = -1
        
        if end_frame is None:
            end_frame = data['data'][-1]['frame']

        for record in data['data']:
            if start_frame <= record['frame'] <= end_frame:
                csv += ','.join(map(str, record['data'])) + '\n'

        if file_path.exists() and not exists_ok:
            raise TSSFileManager.FileAlreadyExistsError()

        with file_path.open(mode='w') as f:
            f.write(csv)