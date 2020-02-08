import sys
import os
import datetime
import itertools

import pyauto
from keyhac import *


def configure(keymap):
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

    mod_keys = ['Alt-', 'Ctrl-', 'Shift-', 'Win-']
    mod_keys_combs = []
    for i in range(len(mod_keys)+1):
        mod_keys_combs += [''.join(x) for x in itertools.combinations(mod_keys, i)]

    # キー変換
    for mod_key in mod_keys_combs:

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
    # アプリケーション別の設定

    # Explorer
    keymap_explorer = keymap.defineWindowKeymap(exe_name='explorer.exe')
    keymap_explorer['U0-I'] = 'F2'

    # Firefox
    keymap_firefox = keymap.defineWindowKeymap(exe_name='firefox.exe')
    keymap_firefox['User0-Z'] = 'Ctrl-Shift-T'
    keymap_firefox['User0-X'] = 'Ctrl-W'
    keymap_firefox['User0-C'] = 'Ctrl-PageUp'
    keymap_firefox['User0-V'] = 'Ctrl-PageDown'
    keymap_firefox['User0-N'] = 'Ctrl-T'
    keymap_firefox['User0-I'] = 'Ctrl-L'

    # Console
    keymap_console = keymap.defineWindowKeymap(exe_name='Console.exe')
    keymap_console['User0-V'] = 'Shift-Insert'
    keymap_console['User1-V'] = 'Shift-Insert'

    # mintty
    keymap_mintty = keymap.defineWindowKeymap(exe_name='mintty.exe')
    keymap_mintty['User0-V'] = 'Shift-Insert'
    keymap_mintty['User1-V'] = 'Shift-Insert'

    # VLC
    keymap_vlc = keymap.defineWindowKeymap(exe_name='vlc.exe')
    keymap_vlc['User0-Z'] = 'Ctrl-J'
    keymap_vlc['User0-C'] = 'Ctrl-Left'
    keymap_vlc['User0-V'] = 'Ctrl-Right'
    keymap_vlc['User0-M'] = 'Alt-Ctrl-Left'
    keymap_vlc['User0-Comma'] = 'Alt-Ctrl-Right'
