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
    # Space, 変換/無変換

    keymap.defineModifier('Space', 'User0')
    keymap.defineModifier(29, 'LUser1') # 無変換
    keymap.defineModifier(28, 'RUser1') # 変換

    # ワンショット
    keymap_global['O-Space'] = 'Space'
    keymap_global['O-(29)'] = lambda: keymap.wnd.setImeStatus(0)
    keymap_global['O-(28)'] = lambda: keymap.wnd.setImeStatus(1)

    # キー変換
    for mod_key in ['', 'Alt-', 'Ctrl-', 'Shift-', 'Win-']:

        # 共通
        for user_mod_key in ['User0-', 'User1-']:
            # Space
            keymap_global[mod_key + user_mod_key + 'B'] = mod_key + 'Space'

            # 右手
            keymap_global[mod_key + user_mod_key + 'H'] = mod_key + 'Left'
            keymap_global[mod_key + user_mod_key + 'J'] = mod_key + 'Down'
            keymap_global[mod_key + user_mod_key + 'K'] = mod_key + 'Up'
            keymap_global[mod_key + user_mod_key + 'L'] = mod_key + 'Right'
            keymap_global[mod_key + user_mod_key + 'U'] = mod_key + 'Home'
            keymap_global[mod_key + user_mod_key + 'O'] = mod_key + 'End'
            keymap_global[mod_key + user_mod_key + 'P'] = mod_key + 'Enter'
            keymap_global[mod_key + user_mod_key + 'Y'] = mod_key + 'Esc'

            # 左手
            keymap_global[mod_key + user_mod_key + 'E'] = mod_key + 'Up'
            keymap_global[mod_key + user_mod_key + 'S'] = mod_key + 'Left'
            keymap_global[mod_key + user_mod_key + 'D'] = mod_key + 'Down'
            keymap_global[mod_key + user_mod_key + 'F'] = mod_key + 'Right'
            keymap_global[mod_key + user_mod_key + 'A'] = mod_key + 'Home'
            keymap_global[mod_key + user_mod_key + 'G'] = mod_key + 'End'
            keymap_global[mod_key + user_mod_key + 'W'] = mod_key + 'PageUp'
            keymap_global[mod_key + user_mod_key + 'R'] = mod_key + 'PageDown'
            keymap_global[mod_key + user_mod_key + 'T'] = mod_key + 'Enter'
            keymap_global[mod_key + user_mod_key + 'Q'] = mod_key + 'Esc'

            # 文字削除
            keymap_global[mod_key + user_mod_key + 'Tab'] = mod_key + 'Back'
            keymap_global[mod_key + user_mod_key + 'Atmark'] = mod_key + 'Delete'

            # ファンクションキー
            for i, key in enumerate([str(x) for x in range(1, 10)] + ['0', 'Minus', 'Caret'], start=1):
                keymap_global[mod_key + user_mod_key + key] = mod_key + 'F' + str(i)

        # 変換/無変換 一部上書き
        keymap_global[mod_key + 'User1-H'] = mod_key + 'Back'
        keymap_global[mod_key + 'User1-J'] = mod_key + 'PageDown'
        keymap_global[mod_key + 'User1-K'] = mod_key + 'PageUp'
        keymap_global[mod_key + 'User1-L'] = mod_key + 'Delete'

    # マクロ
    keymap_global['User1-U'] = 'Shift-Home', 'Delete'
    keymap_global['User1-O'] = 'Shift-End', 'Delete'



    # --------------------------------------------------------------------
    # CapsLock

    # ユーザモディファイアキーの定義：CapsLock(240) --> U3
    keymap.defineModifier("(240)", "U3")

    # 単体押しは一定時間後にモディファイアの状態をリセット
    # keymap_global["U1"] = auto_reset_modifier     # これだとキー表記エラー
    keymap_global["(240)"] = auto_reset_modifier

    for c in [chr(i) for i in range(65, 91)]:
        keymap_global[ "U3-" + c ] = reset_modifier(keymap.InputKeyCommand("RC-" + c))

    def set_key_for_capslock(key, command, keymaps=keymap_global):
        keymaps[ "U3-" + key] = reset_modifier(keymap.InputKeyCommand(command))
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
