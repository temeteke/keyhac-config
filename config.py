import sys
import os
import datetime

import pyauto
from keyhac import *


def configure(keymap):

    # --------------------------------------------------------------------
    # keyhacでCapsLockをモディファイアキー定義して無理矢理使う
    # http://d.hatena.ne.jp/Koonies/20110906/keyhac_capslock_modifier

    ## 関数実行時にモディファイアの状態をリセットするデコレータ
    def reset_modifier(func):
        import functools

        @functools.wraps(func)
        def _reset_modifier(*args, **kw):
            # モディファイアの状態を無理矢理リセット
            keymap.modifier = 0
            # 関数実行
            return func(*args, **kw)
        return _reset_modifier

    ## JobQueue/JobItem でサブスレッド処理にするデコレータ
    def job_queue(func):
        import functools

        @functools.wraps(func)
        def _job_queue(*args, **kw):

            num_items = JobQueue.defaultQueue().numItems()
            if num_items:   # 処理待ちアイテムがある場合は、その数を表示
                print(u"JobQueue.defaultQueue().numItems() :", num_items)

            def __job_queue_1(job_item):
                return func(*args, **kw)

            def __job_queue_2(job_item):
                # print("job_queue : ", func.__name__, args, kw)
                pass

            job_item = JobItem(__job_queue_1, __job_queue_2)
            JobQueue.defaultQueue().enqueue(job_item)

        return _job_queue

    ## 一定時間経過後にモディファイアの状態をリセット
    @job_queue
    def auto_reset_modifier():
        import time
        WAIT_TIME = 0.5  # 秒
        time.sleep(WAIT_TIME)
        # モディファイアの状態を無理矢理リセット
        # if keymap.modifier: print keymap.modifier
        keymap.modifier = 0

    # --------------------------------------------------------------------
    # config.py編集用のテキストエディタの設定

    keymap.editor = "C:\\Program Files (x86)\\vim\\vim73\\gvim.exe"

    # --------------------------------------------------------------------
    # キーマップ

    keymap_global = keymap.defineWindowKeymap()

    # --------------------------------------------------------------------
    # Space

    # Spaceをモディファイアキーにする
    keymap.defineModifier( "Space", "User0" )

    # Spaceをワンショットモディファイアにする
    keymap_global[ "O-Space" ] = "Space"

    # Spaceを使ったキーマップ
    for modifier in ['', 'Alt-', 'Ctrl-', 'Shift-', 'Win-']:
        # 右手
        keymap_global[modifier + 'U0-H'] = modifier + 'Left'
        keymap_global[modifier + 'U0-J'] = modifier + 'Down'
        keymap_global[modifier + 'U0-K'] = modifier + 'Up'
        keymap_global[modifier + 'U0-L'] = modifier + 'Right'
        keymap_global[modifier + 'U0-U'] = modifier + 'Home'
        keymap_global[modifier + 'U0-O'] = modifier + 'End'
        keymap_global[modifier + 'U0-P'] = modifier + 'Enter'
        keymap_global[modifier + 'U0-Y'] = modifier + 'Esc'

        # 左手
        keymap_global[modifier + 'U0-E'] = modifier + 'Up'
        keymap_global[modifier + 'U0-S'] = modifier + 'Left'
        keymap_global[modifier + 'U0-D'] = modifier + 'Down'
        keymap_global[modifier + 'U0-F'] = modifier + 'Right'
        keymap_global[modifier + 'U0-A'] = modifier + 'Home'
        keymap_global[modifier + 'U0-G'] = modifier + 'End'
        keymap_global[modifier + 'U0-W'] = modifier + 'PageUp'
        keymap_global[modifier + 'U0-R'] = modifier + 'PageDown'
        keymap_global[modifier + 'U0-T'] = modifier + 'Enter'
        keymap_global[modifier + 'U0-Q'] = modifier + 'Esc'

        # 文字削除
        keymap_global[modifier + 'U0-Tab'] = modifier + 'Back'
        keymap_global[modifier + 'U0-Atmark'] = modifier + 'Delete'

        # Space
        keymap_global[modifier + 'U0-B'] = modifier + 'Space'

        # ファンクションキー
        for i, key in enumerate(list(range(1, 10)) + [0, 'Minus', 'Caret'], start=1):
            keymap_global[f"{modifier}U0-{key}"] = f"{modifier}F{i}"

    # --------------------------------------------------------------------
    # CapsLock

    # ユーザモディファイアキーの定義：CapsLock(240) --> U1
    keymap.defineModifier("(240)", "U1")

    # 単体押しは一定時間後にモディファイアの状態をリセット
    # keymap_global["U1"] = auto_reset_modifier     # これだとキー表記エラー
    keymap_global["(240)"] = auto_reset_modifier

    for c in [chr(i) for i in range(65, 91)]:
        keymap_global[ "U1-" + c ] = reset_modifier(keymap.InputKeyCommand("RC-" + c))

    def set_key_for_capslock(key, command, keymaps=keymap_global):
        keymaps[ "U1-" + key] = reset_modifier(keymap.InputKeyCommand(command))
        keymaps[ "RC-" + key] = command

    # CapsLockのキーマップ
    set_key_for_capslock("J", "PageDown")
    set_key_for_capslock("K", "PageUp")

    # --------------------------------------------------------------------
    # アプリケーション別の設定

    # Explorer
    keymap_explorer = keymap.defineWindowKeymap( exe_name="explorer.exe" )
    set_key_for_capslock("H", "Alt-Left", keymap_explorer)
    set_key_for_capslock("L", "Alt-Right", keymap_explorer)
    keymap_explorer[ "U0-I" ] = "F2"

    # Firefox
    keymap_firefox = keymap.defineWindowKeymap( exe_name="firefox.exe" )
    keymap_firefox[ "U0-Z" ] = "Ctrl-Shift-T"
    keymap_firefox[ "U0-X" ] = "Ctrl-W"
    keymap_firefox[ "U0-C" ] = "Ctrl-PageUp"
    keymap_firefox[ "U0-V" ] = "Ctrl-PageDown"
    keymap_firefox[ "U0-N" ] = "Ctrl-T"
    keymap_firefox[ "U0-I" ] = "Ctrl-L"

    # Console
    keymap_console = keymap.defineWindowKeymap( exe_name="Console.exe" )
    keymap_console[ "U0-V" ] = "Shift-Insert"

    # mintty
    keymap_mintty = keymap.defineWindowKeymap( exe_name="mintty.exe" )
    keymap_mintty[ "U0-V" ] = "Shift-Insert"

    # gvim
    keymap_gvim = keymap.defineWindowKeymap( exe_name="gvim.exe" )
    keymap_gvim[ "U0-V" ] = "Shift-Insert"

    # VLC
    keymap_vlc = keymap.defineWindowKeymap(exe_name='vlc.exe')
    keymap_vlc['U0-Z'] = 'Ctrl-J'
    keymap_vlc['U0-C'] = 'Ctrl-Left'
    keymap_vlc['U0-V'] = 'Ctrl-Right'
    keymap_vlc['U0-M'] = 'Alt-Ctrl-Left'
    keymap_vlc['U0-Comma'] = 'Alt-Ctrl-Right'
