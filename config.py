import sys
import os
import datetime
import itertools
import string

import pyauto
from keyhac import *


def configure(keymap):
    # --------------------------------------------------------------------
    # 定数の定義

    # 標準のモディファイアキーの組み合わせ
    MOD_KEYS = ['A-', 'C-', 'S-', 'W-']
    MOD_KEYS_COMBS = []
    for i in range(len(MOD_KEYS)+1):
        MOD_KEYS_COMBS += [''.join(x) for x in itertools.combinations(MOD_KEYS, i)]

    # --------------------------------------------------------------------
    # キーマップ

    keymap_global = keymap.defineWindowKeymap()

    # --------------------------------------------------------------------
    # 標準のモディファイアキーのワンショット

    keymap_global['O-LCtrl'] = 'Esc'
    keymap_global['O-LShift'] = 'W-Tab'
    keymap_global['O-RShift'] = 'W-D'

    # --------------------------------------------------------------------
    # ユーザモディファイアキーの定義

    ## スペース
    keymap.defineModifier('Space', 'User0')
    ## 無変換/変換
    keymap.defineModifier(29, 'LUser1') # 無変換
    keymap.defineModifier(28, 'RUser1') # 変換
    ## フットスイッチ
    keymap.defineModifier(124, 'LUser2') # 左
    keymap.defineModifier(126, 'RUser2') # 右
    ## セミコロン
    keymap.defineModifier('Semicolon', 'RUser3') # 右

    # --------------------------------------------------------------------
    # スペース

    for mod_key in MOD_KEYS_COMBS:
        # ワンショット
        keymap_global['O-' + mod_key + 'Space'] = mod_key + 'Space'
        keymap_global['O-' + mod_key + 'U1-Space'] = mod_key + 'Space'

        # スペース
        keymap_global[mod_key + 'U0-B'] = mod_key + 'Space'

        # ファンクションキー
        for i, key in enumerate([str(x) for x in range(1, 10)] + ['0', 'Minus', 'Caret'], start=1):
            keymap_global[mod_key + 'U0-' + key] = mod_key + 'F' + str(i)

        # 右手
        keymap_global[mod_key + 'U0-H'] = mod_key + 'Left'
        keymap_global[mod_key + 'U0-J'] = mod_key + 'Down'
        keymap_global[mod_key + 'U0-K'] = mod_key + 'Up'
        keymap_global[mod_key + 'U0-L'] = mod_key + 'Right'
        keymap_global[mod_key + 'U0-U'] = mod_key + 'Home'
        keymap_global[mod_key + 'U0-O'] = mod_key + 'End'
        keymap_global[mod_key + 'U0-P'] = mod_key + 'Enter'
        keymap_global[mod_key + 'U0-Y'] = mod_key + 'Esc'

        # 左手
        keymap_global[mod_key + 'U0-E'] = mod_key + 'Up'
        keymap_global[mod_key + 'U0-S'] = mod_key + 'Left'
        keymap_global[mod_key + 'U0-D'] = mod_key + 'Down'
        keymap_global[mod_key + 'U0-F'] = mod_key + 'Right'
        keymap_global[mod_key + 'U0-A'] = mod_key + 'Home'
        keymap_global[mod_key + 'U0-G'] = mod_key + 'End'
        keymap_global[mod_key + 'U0-W'] = mod_key + 'PageUp'
        keymap_global[mod_key + 'U0-R'] = mod_key + 'PageDown'
        keymap_global[mod_key + 'U0-T'] = mod_key + 'Enter'
        keymap_global[mod_key + 'U0-Q'] = mod_key + 'Esc'

        # 両手で対称
        keymap_global[mod_key + 'U0-Tab']    = mod_key + 'Back'
        keymap_global[mod_key + 'U0-Atmark'] = mod_key + 'Delete'

    # ランチャー(PowerToys Run)
    keymap_global['O-U0-LCtrl'] = 'A-Space'

    # ウィンドウ切替
    keymap_global['O-U0-LShift'] = 'D-Alt', 'Tab'
    keymap_mvf = keymap.defineWindowKeymap(exe_name='explorer.exe', class_name='MultitaskingViewFrame')
    keymap_mvf['U-Space'] = 'U-Alt' # スペースを離したら確定する

    # ウィンドウ切替
    keymap_global['O-U0-RShift'] = 'A-Esc'

    # 入力補助
    keymap_global['U0-Semicolon'] = keymap.defineMultiStrokeKeymap()
    ## 日時入力
    keymap_global['U0-Semicolon']['Semicolon'] = lambda: keymap.InputTextCommand(datetime.datetime.now().strftime('%Y/%m/%d'))()
    keymap_global['U0-Semicolon']['Colon'] = lambda: keymap.InputTextCommand(datetime.datetime.now().strftime('%H:%M:%S'))()
    keymap_global['U0-Semicolon']['J'] = lambda: keymap.InputTextCommand(datetime.datetime.now().strftime('%Y%m%d'))()
    keymap_global['U0-Semicolon']['K'] = lambda: keymap.InputTextCommand(datetime.datetime.now().strftime('%H%M%S'))()
    ## 括弧の入力
    keymap_global['U0-Semicolon']['2'] = 'S-2', 'S-2', 'Left'
    keymap_global['U0-Semicolon']['7'] = 'S-7', 'S-7', 'Left'
    keymap_global['U0-Semicolon']['Atmark'] = 'S-Atmark', 'S-Atmark', 'Left'
    keymap_global['U0-Semicolon']['8'] = 'S-8', 'S-9', 'Left'
    keymap_global['U0-Semicolon']['9'] = 'S-8', 'S-9', 'Left'
    keymap_global['U0-Semicolon']['OpenBracket']  = 'OpenBracket', 'CloseBracket', 'Left'
    keymap_global['U0-Semicolon']['CloseBracket'] = 'OpenBracket', 'CloseBracket', 'Left'
    keymap_global['U0-Semicolon']['S-OpenBracket']  = 'S-OpenBracket', 'S-CloseBracket', 'Left'
    keymap_global['U0-Semicolon']['S-CloseBracket'] = 'S-OpenBracket', 'S-CloseBracket', 'Left'
    keymap_global['U0-Semicolon']['Comma']  = 'S-Comma', 'S-Period', 'Left'
    keymap_global['U0-Semicolon']['Period'] = 'S-Comma', 'S-Period', 'Left'
    ## クリップボード
    keymap_global['U0-Semicolon']['V'] = keymap.command_ClipboardList

    # 矢印キー
    keymap_global['U0-Up']    = 'PageUp'
    keymap_global['U0-Down']  = 'PageDown'
    keymap_global['U0-Left']  = 'Home'
    keymap_global['U0-Right'] = 'End'

    # アプリケーションで上書きされることもあるキー
    keymap_global['U0-X'] = 'C-W' # 閉じる
    keymap_global['U0-Z'] = 'C-Z' # 戻る

    # --------------------------------------------------------------------
    # 無変換/変換

    for mod_key in MOD_KEYS_COMBS:
        # ワンショット
        keymap_global['O-' + mod_key + '(29)'] = mod_key + '(29)'
        keymap_global['O-' + mod_key + '(28)'] = mod_key + '(28)'
        keymap_global['O-' + mod_key + 'U0-(29)'] = mod_key + '(29)'
        keymap_global['O-' + mod_key + 'U0-(28)'] = mod_key + '(28)'

        # 左右逆のモディファイアキーを押していたらShiftにする
        ## 左手
        for key in '12345QWERTASDFGZXCVB':
            keymap_global[mod_key + 'RU1-' + key] = mod_key + 'S-' + key
        ## 右手
        for key in '67890YUIOPHJKLNM':
            keymap_global[mod_key + 'LU1-' + key] = mod_key + 'S-' + key
        for key in ('Minus', 'Caret', 'Yen', 'Atmark', 'OpenBracket', 'Plus', 'Colon', 'CloseBracket', 'Comma', 'Period', 'Slash', 'Underscore'):
            keymap_global[mod_key + 'LU1-' + key] = mod_key + 'S-' + key

        # 無変換/変換を押していれば削除
        keymap_global[mod_key + 'RU1-H'] = mod_key + 'Back'
        keymap_global[mod_key + 'RU1-L'] = mod_key + 'Delete'

        # 無変換/変換を押していれば大きく移動
        keymap_global[mod_key + 'RU1-J'] = mod_key + 'PageDown'
        keymap_global[mod_key + 'RU1-K'] = mod_key + 'PageUp'

        # 無変換/変換を押していればBack/Deleteを反転
        keymap_global[mod_key + 'LU1-Tab']    = mod_key + 'Delete'
        keymap_global[mod_key + 'RU1-Atmark'] = mod_key + 'Back'

    # 無変換/変換でIMEを切替
    keymap_global['O-(29)'] = lambda: keymap.wnd.setImeStatus(0)
    keymap_global['O-(28)'] = lambda: keymap.wnd.setImeStatus(1)

    # 無変換/変換を押していれば削除
    keymap_global['RU1-U'] = 'S-Home', 'Back'
    keymap_global['RU1-O'] = 'S-End', 'Delete'
    keymap_global['LU1-A'] = 'S-Home', 'Back'
    keymap_global['LU1-G'] = 'S-End', 'Delete'

    # モニター間の移動
    keymap_global['LU1-E'] = 'W-Up'
    keymap_global['LU1-S'] = 'W-Left'
    keymap_global['LU1-D'] = 'W-Down'
    keymap_global['LU1-F'] = 'W-Right'
    keymap_global['LU1-W'] = 'W-S-Left'
    keymap_global['LU1-R'] = 'W-S-Right'

    # モニター番号を指定して移動
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

            keymap.InputKeyCommand('Ctrl')() # Ctrlキーを押すとポインターの位置を表示する

        return run

    for i in range(4):
        keymap_global[f'LU1-{i+1}'] = mouse_move_between_monitor_command(i)

    # --------------------------------------------------------------------
    # スペース, 無変換/変換

    # スペースと無変換/変換を同時に押していれば選択する
    for mod_key in MOD_KEYS_COMBS:
        ## 右手
        keymap_global[mod_key + 'U0-U1-H'] = mod_key + 'S-Left'
        keymap_global[mod_key + 'U0-U1-J'] = mod_key + 'S-Down'
        keymap_global[mod_key + 'U0-U1-K'] = mod_key + 'S-Up'
        keymap_global[mod_key + 'U0-U1-L'] = mod_key + 'S-Right'
        keymap_global[mod_key + 'U0-U1-U'] = mod_key + 'S-Home'
        keymap_global[mod_key + 'U0-U1-O'] = mod_key + 'S-End'
        ## 左手
        keymap_global[mod_key + 'U0-U1-E'] = mod_key + 'S-Up'
        keymap_global[mod_key + 'U0-U1-S'] = mod_key + 'S-Left'
        keymap_global[mod_key + 'U0-U1-D'] = mod_key + 'S-Down'
        keymap_global[mod_key + 'U0-U1-F'] = mod_key + 'S-Right'
        keymap_global[mod_key + 'U0-U1-A'] = mod_key + 'S-Home'
        keymap_global[mod_key + 'U0-U1-G'] = mod_key + 'S-End'
        keymap_global[mod_key + 'U0-U1-W'] = mod_key + 'S-PageUp'
        keymap_global[mod_key + 'U0-U1-R'] = mod_key + 'S-PageDown'

    # スペースと無変換/変換を同時に押していれば行を連結
    keymap_global['U0-U1-Tab']    = 'Home', 'Back', 'Home'
    keymap_global['U0-U1-Atmark'] = 'End', 'Delete', 'End'

    # クリップボード
    def paste_clipboard_text():
        keymap.wnd.setImeStatus(0) # IMEオフにする
        keymap.InputTextCommand(getClipboardText().strip())()

    keymap_global['U0-V'] = lambda: paste_clipboard_text()  # プレーンテキストとして貼り付け
    keymap_global['LU1-V'] = 'W-V' # クリップボードの履歴を表示

    # --------------------------------------------------------------------
    # セミコロン
    for mod_key in MOD_KEYS_COMBS:
        keymap_global['O-' + mod_key + 'Semicolon'] = mod_key + 'Semicolon'
    ## 2段目 1段目の記号にする Pに割当てはなし
    for i, key in enumerate('QWERTYUIO', start=1):
        keymap_global['U3-' + key] = f'S-{i}'
    ## 3段目 数字にする 0は左Ctrl
    keymap_global['U3-LCtrl'] = '0'
    for i, key in enumerate('ASDFGHJKL', start=1):
        keymap_global['U3-' + key] = str(i)
    ## 4段目 押しにくい記号
    keymap_global['U3-Z']      = 'Minus' # IMEオンの時にーを入力できるようにInputTextCommandは使わない
    keymap_global['U3-X']      = keymap.InputTextCommand('=')
    keymap_global['U3-C']      = keymap.InputTextCommand('^')
    keymap_global['U3-V']      = keymap.InputTextCommand('~')
    keymap_global['U3-B']      = keymap.InputTextCommand('|')
    keymap_global['U3-N']      = keymap.InputTextCommand('^') # USキーボードの位置から
    keymap_global['U3-M']      = keymap.InputTextCommand('$') # Vimのことを考えると^の右に$が欲しい
    keymap_global['U3-Comma']  = keymap.InputTextCommand('[')
    keymap_global['U3-Period'] = keymap.InputTextCommand(']')

    # --------------------------------------------------------------------
    # フットスイッチ

    # フットスイッチをShiftにする
    for x in string.ascii_uppercase + string.digits:
        keymap_global['U2-' + x] = 'S-' + x
    for x in ('Minus', 'Caret', 'Yen', 'Atmark', 'OpenBracket', 'Plus', 'Colon', 'CloseBracket', 'Comma', 'Period', 'Slash', 'Underscore'):
        keymap_global['U2-' + x] = 'S-' + x

    # ワンショット
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
    keymap_mintty['RU1-U'] = 'C-U'
    keymap_mintty['RU1-O'] = 'C-O'
    keymap_mintty['LU1-A'] = 'C-U'
    keymap_mintty['LU1-G'] = 'C-O'

    # VLC
    keymap_vlc = keymap.defineWindowKeymap(exe_name='vlc.exe')
    keymap_vlc['U0-Z'] = 'C-J'
    keymap_vlc['U0-C'] = 'C-Left'
    keymap_vlc['U0-V'] = 'C-Right'
    keymap_vlc['U0-M'] = 'OpenBracket'
    keymap_vlc['U0-Comma'] = 'CloseBracket'
    keymap_vlc['U0-Period'] = 'A-C-Left'
    keymap_vlc['U0-Slash'] = 'A-C-Right'
    keymap_vlc['O-(124)'] = lambda: None # ワンショットモディファイアを無効化する
    keymap_vlc['O-(126)'] = lambda: None # ワンショットモディファイアを無効化する
    keymap_vlc['D-(124)'] = 'Left'  # 押された瞬間に入力する
    keymap_vlc['D-(126)'] = 'Right' # 押された瞬間に入力する
    keymap_vlc['D-LU2-(124)'] = 'Left'  # 押されている間ずっと入力する
    keymap_vlc['D-RU2-(126)'] = 'Right' # 押されている間ずっと入力する
    keymap_vlc['D-(125)'] = lambda: None # 長押しされても入力しない
    keymap_vlc['U-(125)'] = 'Space' # 離されたときに入力する

    # Splashtop
    keymap_splashtop = keymap.defineWindowKeymap(exe_name='strwinclt.exe')
    keymap_splashtop['O-(29)'] = '(29)'
    keymap_splashtop['O-(28)'] = '(28)'

    # Minecraft
    # ワンショットモディファイアの無効化と押されているときにずっと入力する様にした方がいいかも?
    keymap_minecraft = keymap.defineWindowKeymap(exe_name='javaw.exe', window_text='Minecraft*')
    keymap_minecraft['D-Space'] = 'D-Space'
    keymap_minecraft['U-Space'] = 'U-Space'

    # Grand Theft Auto V
    keymap_gta5 = keymap.defineWindowKeymap(exe_name='GTA5.exe')
    keymap_gta5['D-Space'] = 'D-Space'
    keymap_gta5['U-Space'] = 'U-Space'

    # Fusion 360
    keymap_fusion360 = keymap.defineWindowKeymap(exe_name='Fusion360.exe')
    keymap_fusion360['O-(124)'] = lambda: None # ワンショットモディファイアを無効化する
    keymap_fusion360['D-(124)'] = 'D-S-MButton'
    keymap_fusion360['U-(124)'] = 'U-S-MButton'
    keymap_fusion360['O-(126)'] = lambda: None # ワンショットモディファイアを無効化する
    keymap_fusion360['D-(126)'] = 'D-MButton'
    keymap_fusion360['U-(126)'] = 'U-MButton'

    # Cura
    keymap_cura = keymap.defineWindowKeymap(exe_name='Cura.exe')
    keymap_cura['O-(124)'] = lambda: None # ワンショットモディファイアを無効化する
    keymap_cura['D-(124)'] = 'D-RButton'
    keymap_cura['U-(124)'] = 'U-RButton'
    keymap_cura['O-(126)'] = lambda: None # ワンショットモディファイアを無効化する
    keymap_cura['D-(126)'] = 'D-MButton'
    keymap_cura['U-(126)'] = 'U-MButton'

    # GnuCash
    keymap_cura = keymap.defineWindowKeymap(exe_name='gnucash.exe')
    keymap_cura['C-V'] = 'S-Insert' # Ctrlのショートカットキーが効かないのでCtrl-Vの代わりにShift-Insertを入力する
