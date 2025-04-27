""" __main__.py 文件介绍

    __main__.py 文件在 Python 中用于定义一个包（在这里是 freegames ）的直接执行入口。
    当通过命令行运行一个包（如 python -m package_name）时，Python 解释器会自动执行该包目录下的 __main__.py 文件。
    通常命令为 python -m freegames
"""

"""Free Games CLI
"""

import argparse         #处理命令行参数的库
import os
import runpy


def game_file(name):
    """Return True if filename represents a game.
        检查文件名是否符合要求，返回值为布尔之。
    """
    return (
        name.endswith('.py')
        and not name.startswith('__')
        and name != 'utils.py'
    )


def main():
    
    directory = os.path.dirname(os.path.realpath(__file__))                      # 获取当前脚本的绝对路径。
    contents = os.listdir(directory)                                             # 生成目录下所有文件名的列表。
    games = sorted(name[:-3] for name in contents if game_file(name))            # 过滤非游戏文件，并去掉 .py 后缀（如 snake.py → snake），最后排序生成 games 列表。sorted 函数是对列表中的元素按字幕顺序排序。

    """命令行输入 → argparse解析 → 执行子命令 → 结果输出
    
      │—— 子命令 → 命令逻辑
      ├── list  → 打印游戏列表
      ├── play  → 运行游戏
      ├── show  → 显示源代码
      └── copy  → 复制代码（检查覆盖）

    """
    parser = argparse.ArgumentParser(
        prog='freegames',
        description='Free Python Games',
        epilog='Copyright 2023 Grant Jenks',
    )
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')
    subparsers.required = True

    subparsers.add_parser('list', help='list games')

    parser_play = subparsers.add_parser('play', help='play free Python games')
    parser_play.add_argument('game', choices=games, help='game name')

    parser_show = subparsers.add_parser('show', help='show game source code')
    parser_show.add_argument('game', choices=games, help='game name')

    parser_copy = subparsers.add_parser('copy', help='copy game source code')
    parser_copy.add_argument('game', choices=games, help='game name')
    parser_copy.add_argument(
        '--force',
        action='store_true',
        help='overwrite existing file',
    )

    args = parser.parse_args()

    if args.command == 'list':
        for game in games:
            print(game)
    elif args.command == 'play':
        runpy.run_module('freegames.' + args.game)
    elif args.command == 'show':
        with open(os.path.join(directory, args.game + '.py')) as reader:
            print(reader.read())
    else:
        assert args.command == 'copy'
        filename = args.game + '.py'

        with open(os.path.join(directory, filename)) as reader:
            text = reader.read()

        cwd = os.getcwd()
        path = os.path.join(cwd, filename)

        if args.force or not os.path.exists(path):
            with open(path, 'w') as writer:
                writer.write(text)
        else:
            print('ERROR: File already exists. Specify --force to overwrite.')


if __name__ == '__main__':
    main()  # pragma: no cover
