import argparse

from pathlib import Path
from tss import Player, TSSFileManager
from typing import List


def player(args: List[str]) -> None:
    """
    機能としてplayerが選択されている時に呼び出される関数

    Parameters
    ----------
    args : List[str]

        function(player)以降に与えられた引数
    """
    len_args = len(args)

    file_path = None

    if len_args == 1:
        file_path = Path(args[0])

        if file_path.suffix != '.tss':
            print(u'引数には.tss形式のファイルを指定してください。')
            return
    elif len_args > 1:
        print(u'無効な引数:', ','.join(args[1:]))
        return

    Player(file_path)


def gencsv(args: List[str]) -> None:
    """
    機能としてgencsvが選択されている時に呼び出される関数

    Parameters
    ----------
    args : List[str]

        function(gencsv)以降に与えられた引数
    """
    parser = argparse.ArgumentParser(prog='tss gencsv', description=u'tssファイルからcsvファイルを生成する',
                                     epilog=u'その他詳しい情報はGitHubのリポジトリ(https://github.com/Hara-Yuma/TimeSeriesSensing)を確認してください。')

    parser.add_argument('tssfile', help=u'tss形式のファイルへのパス')
    parser.add_argument('output', help=u'生成するcsvファイルへのパス')
    
    parsed_args = parser.parse_args(args)

    target_file_path = Path(parsed_args.tssfile)
    output_file_path = Path(parsed_args.output)

    if not target_file_path.exists():
        print(str(target_file_path), u'は存在しません。')
        return
    elif target_file_path.suffix != '.tss':
        print(u'引数tssfileには，.tss形式のファイルを指定してください。')
        return

    file_manager = TSSFileManager(target_file_path)
    file_manager.exportAsCSV(output_file_path, exists_ok=True)


def genmd(args: List[str]) -> None:
    """
    機能としてgenmdが選択されている時に呼び出される関数

    Parameters
    ----------
    args : List[str]

        function(gencsv)以降に与えられた引数
    """
    parser = argparse.ArgumentParser(prog='tss genmd', description=u'tssファイルからmdファイルを生成する',
                                     epilog=u'その他詳しい情報はGitHubのリポジトリ(https://github.com/Hara-Yuma/TimeSeriesSensing)を確認してください。')

    parser.add_argument('tssfile', help=u'tss形式のファイルへのパス')
    parser.add_argument('output', help=u'mdファイルを生成するディレクトリへのパス')
    
    parsed_args = parser.parse_args(args)

    target_file_path = Path(parsed_args.tssfile)
    output_dir_path = Path(parsed_args.output)

    if not target_file_path.exists():
        print(str(target_file_path), u'は存在しません。')
        return
    elif target_file_path.suffix != '.tss':
        print(u'引数tssfileには，.tss形式のファイルを指定してください。')
        return

    file_manager = TSSFileManager(target_file_path)
    file_manager.exportAsMD(output_dir_path, exists_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(prog='tss', description='Time Series Sensing',
                                     epilog=u'その他詳しい情報はGitHubのリポジトリ(https://github.com/Hara-Yuma/TimeSeriesSensing)を確認してください。')

    parser.add_argument('function', choices=['player', 'gencsv', 'genmd'], help=u'機能を指定する。')
    parser.add_argument('args', nargs='*', help=u'機能毎の引数')

    parsed_args = parser.parse_args()

    func = parsed_args.function

    if func == 'player':
        player(parsed_args.args)
    elif func == 'gencsv':
        gencsv(parsed_args.args)
    elif func == 'genmd':
        genmd(parsed_args.args)


main()