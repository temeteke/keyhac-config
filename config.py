import sys
import os
import datetime
import itertools

import pyauto
from keyhac import *

import string


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

    mod_keys = ['A-', 'C-', 'S-', 'W-']
    mod_keys_combs = []
    for i in range(len(mod_keys)+1):
        mod_keys_combs += [''.join(x) for x in itertools.combinations(mod_keys, i)]

    # キー変換
    for mod_key in mod_keys_combs:

        # 共通
        for user_mod_key in ['U0-', 'U1-']:
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
        keymap_global[mod_key + 'U1-H'] = mod_key + 'Back'
        keymap_global[mod_key + 'U1-J'] = mod_key + 'PageDown'
        keymap_global[mod_key + 'U1-K'] = mod_key + 'PageUp'
        keymap_global[mod_key + 'U1-L'] = mod_key + 'Delete'
        keymap_global[mod_key + 'U1-Tab'] = mod_key + 'Delete'
        keymap_global[mod_key + 'U1-Atmark'] = mod_key + 'Back'

    # ランチャー(PowerToys Run)
    keymap_global['O-U0-LCtrl'] = 'A-Space'

    # マクロ
    keymap_global['U1-U'] = 'S-Home', 'Delete'
    keymap_global['U1-O'] = 'S-End', 'Delete'

    # モニター間の移動
    keymap_global['U1-E'] = 'W-Up'
    keymap_global['U1-S'] = 'W-Left'
    keymap_global['U1-D'] = 'W-Down'
    keymap_global['U1-F'] = 'W-Right'
    keymap_global['U1-W'] = 'W-S-Left'
    keymap_global['U1-R'] = 'W-S-Right'

    def mouse_move_between_monitor_command(monitor):
        def run():
            mouse_x, mouse_y = pyauto.Input.getCursorPos()
            monitor_info = sorted(pyauto.Window.getMonitorInfo())
            next_monitor = monitor % len(monitor_info)

            for i, v in enumerate(monitor_info):
                if v[0][0] <= mouse_x < v[0][2]:
                    current_monitor = i
                    break

            if next_monitor != current_monitor:
                monitor_width = monitor_info[next_monitor][0][2] - monitor_info[next_monitor][0][0]
                monitor_height = monitor_info[next_monitor][0][3] - monitor_info[next_monitor][0][1]
                current_monitor_width = monitor_info[current_monitor][0][2] - monitor_info[current_monitor][0][0]
                current_monitor_height = monitor_info[current_monitor][0][3] - monitor_info[current_monitor][0][1]
                mouse_x = int(monitor_info[next_monitor][0][0] + (mouse_x - monitor_info[current_monitor][0][0]) * monitor_width / current_monitor_width)
                mouse_y = int(monitor_info[next_monitor][0][1] + (mouse_y - monitor_info[current_monitor][0][1]) * monitor_height / current_monitor_height)
                Input.send([pyauto.MouseMove(mouse_x, 0), pyauto.MouseMove(mouse_x, mouse_y)]) # yが現在の画面の高さ以上の座標に移動するとxがおかしくなるので2段階に分けて移動する

            keymap.InputKeyCommand('Ctrl')()

        return run

    for i in range(4):
        keymap_global[f'U1-{i+1}'] = mouse_move_between_monitor_command(i)

    # クリップボードの履歴
    keymap_global['U0-V'] = 'W-V'
    keymap_global['U1-V'] = 'W-V'

    # --------------------------------------------------------------------
    # フットスイッチ

    keymap.defineModifier(124, 'LUser2') # 左
    keymap.defineModifier(126, 'RUser2') # 右

    for x in string.ascii_uppercase + string.digits:
        keymap_global['U2-' + x] = 'S-' + x

    keymap_global['O-(124)'] = 'Esc'
    keymap_global['(125)'] = 'Space'
    keymap_global['O-(126)'] = 'Enter'
    keymap_global['U2-(125)'] = '(127)'

    # テンキーのNumLock
    keymap_global['U2-Num0'] = 'Insert'
    keymap_global['U2-Num1'] = 'End'
    keymap_global['U2-Num2'] = 'Down'
    keymap_global['U2-Num3'] = 'PageDown'
    keymap_global['U2-Num4'] = 'Left'
    keymap_global['U2-Num5'] = 'Space'
    keymap_global['U2-Num6'] = 'Right'
    keymap_global['U2-Num7'] = 'Home'
    keymap_global['U2-Num8'] = 'Up'
    keymap_global['U2-Num9'] = 'PageUp'


    # --------------------------------------------------------------------
    # アプリケーション別の設定

    # Explorer
    keymap_explorer = keymap.defineWindowKeymap(exe_name='explorer.exe')
    keymap_explorer['U0-Z'] = 'A-Up'
    keymap_explorer['U0-X'] = 'C-W'
    keymap_explorer['U0-M'] = 'A-Left'
    keymap_explorer['U0-Comma'] = 'A-Right'
    keymap_explorer['U0-Period'] = 'C-R'
    keymap_explorer['U0-I'] = 'F2'

    # ブラウザ
    def is_browser(window):
        if window.getProcessName() in ('firefox.exe', 'chrome.exe', 'msedge.exe'):
            return True
        else:
            return False

    keymap_browser = keymap.defineWindowKeymap(check_func=is_browser)
    keymap_browser['U0-Z'] = 'C-S-T'
    keymap_browser['U0-X'] = 'C-W'
    keymap_browser['U0-C'] = 'C-PageUp'
    keymap_browser['U0-V'] = 'C-PageDown'
    keymap_browser['U0-N'] = 'C-T'
    keymap_browser['U0-M'] = 'A-Left'
    keymap_browser['U0-Comma'] = 'A-Right'
    keymap_browser['U0-Period'] = 'C-R'
    keymap_browser['U0-I'] = 'C-L'

    # mintty
    keymap_mintty = keymap.defineWindowKeymap(exe_name='mintty.exe')
    keymap_mintty['U0-V'] = 'S-Insert'

    # VLC
    keymap_vlc = keymap.defineWindowKeymap(exe_name='vlc.exe')
    keymap_vlc['U0-Z'] = 'C-J'
    keymap_vlc['U0-C'] = 'C-Left'
    keymap_vlc['U0-V'] = 'C-Right'
    keymap_vlc['U0-M'] = 'OpenBracket'
    keymap_vlc['U0-Comma'] = 'CloseBracket'
    keymap_vlc['U0-Period'] = 'A-C-Left'
    keymap_vlc['U0-Slash'] = 'A-C-Right'
    keymap_vlc['O-(124)'] = lambda: None #ワンショットモディファイアを無効化する
    keymap_vlc['O-(126)'] = lambda: None #ワンショットモディファイアを無効化する
    keymap_vlc['D-(124)'] = 'Left'  #押された瞬間に入力する
    keymap_vlc['D-(126)'] = 'Right' #押された瞬間に入力する
    keymap_vlc['D-LU2-(124)'] = 'Left'  #押されている間ずっと入力する
    keymap_vlc['D-RU2-(126)'] = 'Right' #押されている間ずっと入力する
    keymap_vlc['D-(125)'] = lambda: None #長押しされても入力しない
    keymap_vlc['U-(125)'] = 'Space' #離されたときに入力する

    # Splashtop
    keymap_splashtop = keymap.defineWindowKeymap(exe_name='strwinclt.exe')
    keymap_splashtop['O-(29)'] = '(29)'
    keymap_splashtop['O-(28)'] = '(28)'

    # Minecraft
    #ワンショットモディファイアの無効化と押されているときにずっと入力する様にした方がいいかも?
    keymap_minecraft = keymap.defineWindowKeymap(exe_name='javaw.exe', window_text='Minecraft*')
    keymap_minecraft['D-Space'] = 'D-Space'
    keymap_minecraft['U-Space'] = 'U-Space'

    # Grand Theft Auto V
    keymap_gta5 = keymap.defineWindowKeymap(exe_name='GTA5.exe')
    keymap_gta5['D-Space'] = 'D-Space'
    keymap_gta5['U-Space'] = 'U-Space'

    # Fusion 360
    keymap_fusion360 = keymap.defineWindowKeymap(exe_name='Fusion360.exe')
    keymap_fusion360['O-(124)'] = lambda: None #ワンショットモディファイアを無効化する
    keymap_fusion360['D-(124)'] = 'D-S-MButton'
    keymap_fusion360['U-(124)'] = 'U-S-MButton'
    keymap_fusion360['O-(126)'] = lambda: None #ワンショットモディファイアを無効化する
    keymap_fusion360['D-(126)'] = 'D-MButton'
    keymap_fusion360['U-(126)'] = 'U-MButton'

    # Cura
    keymap_cura = keymap.defineWindowKeymap(exe_name='Cura.exe')
    keymap_cura['O-(124)'] = lambda: None #ワンショットモディファイアを無効化する
    keymap_cura['D-(124)'] = 'D-RButton'
    keymap_cura['U-(124)'] = 'U-RButton'
    keymap_cura['O-(126)'] = lambda: None #ワンショットモディファイアを無効化する
    keymap_cura['D-(126)'] = 'D-MButton'
    keymap_cura['U-(126)'] = 'U-MButton'
