import sys
import os
import datetime
import itertools
import string

import pyauto
from keyhac import *
from time import time


def configure(keymap):
    # --------------------------------------------------------------------
    # 定数の定義

    # 標準のモディファイアキーの組み合わせ
    MOD_KEYS = ['A-', 'C-', 'S-', 'W-']
    MOD_KEYS_COMBS = []
    for i in range(len(MOD_KEYS)+1):
        MOD_KEYS_COMBS += [''.join(x) for x in itertools.combinations(MOD_KEYS, i)]

    # --------------------------------------------------------------------
    # 汎用クラス

    # キー入力のクラス
    class Key():
        def __init__(self, key):
            #print(self, key)
            self.key = key
            self.last_time = time()

        def inputCommand(self, count=1, interval=0):
            def func():
                #print(self, self.key, self.last_time)
                if time() > self.last_time + interval:
                    for i in range(count):
                        keymap.InputKeyCommand(self.key)()
                    self.last_time = time()
                    #print(self, self.key, self.last_time, 'input')
            return func

    # --------------------------------------------------------------------
    # 環境依存の特殊キーの定義

    ## フットスイッチの仮想キーコード
    VK_FOOT_LEFT   = 124
    VK_FOOT_CENTER = 125
    VK_FOOT_RIGHT  = 126

    ## フットスイッチのキー記述
    KEY_FOOT_LEFT   = f'({VK_FOOT_LEFT})'
    KEY_FOOT_CENTER = f'({VK_FOOT_CENTER})'
    KEY_FOOT_RIGHT  = f'({VK_FOOT_RIGHT})'

    # --------------------------------------------------------------------
    # デフォルトのモディファイアキーと組み合わせて押すキー
    # リストを作り最後にまとめてマッピングする

    keys = {
        'F1': [],
        'F2': [],
        'F3': [],
        'F4': [],
        'F5': [],
        'F6': [],
        'F7': [],
        'F8': [],
        'F9': [],
        'F10': [],
        'F11': [],
        'F12': [],
        'Left': [],
        'Up': [],
        'Right': [],
        'Down': [],
        'Space': [],
        'Back': [],
        'Enter': [],
        'Escape': [],
        'Insert': [],
        'Delete': [],
        'Home': [],
        'End': [],
        'PageUp': [],
        'PageDown': [],
    }

    # --------------------------------------------------------------------
    # Pop List

    def command_KeyhacMenuList():
        # If the list window is already opened, just close it
        if keymap.isListWindowOpened():
            keymap.cancelListWindow()
            return

        def popListWindow():
            items = [
                ("Edit config.py",   keymap.command_EditConfig),
                ("Reload config.py", keymap.command_ReloadConfig),
            ]

            listers = [
                ("Keyhac Menu", cblister_FixedPhrase(items)),
            ]

            item, mod = keymap.popListWindow(listers)

            if item:
                item[1]()

        # Because the blocking procedure cannot be executed in the key-hook,
        # delayed-execute the procedure by delayedCall().
        keymap.delayedCall(popListWindow, 0)

    # --------------------------------------------------------------------
    # クリップボード

    # Add quote mark to current clipboard contents
    def quoteClipboardText():
        s = getClipboardText()
        lines = s.splitlines(True)
        s = ""
        for line in lines:
            s += keymap.quote_mark + line
        return s

    # Indent current clipboard contents
    def indentClipboardText():
        s = getClipboardText()
        lines = s.splitlines(True)
        s = ""
        for line in lines:
            if line.lstrip():
                line = " " * 4 + line
            s += line
        return s

    # Unindent current clipboard contents
    def unindentClipboardText():
        s = getClipboardText()
        lines = s.splitlines(True)
        s = ""
        for line in lines:
            for i in range(4+1):
                if i>=len(line) : break
                if line[i]=='\t':
                    i+=1
                    break
                if line[i]!=' ':
                    break
            s += line[i:]
        return s

    full_width_chars = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～０１２３４５６７８９　"
    half_width_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}～0123456789 "

    # Convert to half-with characters
    def toHalfWidthClipboardText():
        s = getClipboardText()
        s = s.translate(str.maketrans(full_width_chars,half_width_chars))
        return s

    # Convert to full-with characters
    def toFullWidthClipboardText():
        s = getClipboardText()
        s = s.translate(str.maketrans(half_width_chars,full_width_chars))
        return s

    def command_CustomizedClipboardList():
        # If the list window is already opened, just close it
        if keymap.isListWindowOpened():
            keymap.cancelListWindow()
            return

        def popListWindow():
            items = [
                ("Quote clipboard",    quoteClipboardText),
                ("Indent clipboard",   indentClipboardText),
                ("Unindent clipboard", unindentClipboardText),
                ("To Half-Width",      toHalfWidthClipboardText),
                ("To Full-Width",      toFullWidthClipboardText),
            ]

            listers = [
                ("Customized Clipboard", cblister_FixedPhrase(items)),
            ]

            item, mod = keymap.popListWindow(listers)

            if item:
                item[1]()

        # Because the blocking procedure cannot be executed in the key-hook,
        # delayed-execute the procedure by delayedCall().
        keymap.delayedCall(popListWindow, 0)

    # --------------------------------------------------------------------
    # キーマップ

    keymap_global = keymap.defineWindowKeymap()

    # --------------------------------------------------------------------
    # ユーザモディファイアキーの定義

    ## スペース
    keymap.defineModifier('Space', 'User0')
    ## 無変換/変換
    keymap.defineModifier(29, 'LUser1') # 無変換
    keymap.defineModifier(28, 'RUser1') # 変換
    ## フットスイッチ
    keymap.defineModifier(VK_FOOT_LEFT,  'LUser2') # 左
    keymap.defineModifier(VK_FOOT_RIGHT, 'RUser2') # 右
    ## コロン
    keymap.defineModifier('Colon', 'RUser3')

    # --------------------------------------------------------------------
    # スペース

    # スペース
    keys['Space'].append('U0-B')
    keys['Space'].append('O-Space')
    keys['Space'].append('O-U1-Space')

    # ファンクションキー
    for i, key in enumerate([str(x) for x in range(1, 10)] + ['0', 'Minus', 'Caret'], start=1):
        keys['F' + str(i)].append('U0-' + key)

    # 右手
    keys['Left'    ].append('U0-H')
    keys['Down'    ].append('U0-J')
    keys['Up'      ].append('U0-K')
    keys['Right'   ].append('U0-L')
    keys['Home'    ].append('U0-U')
    keys['End'     ].append('U0-O')
    keys['Enter'   ].append('U0-P')
    keys['Escape'  ].append('U0-Y')
    keys['PageUp'  ].append('U0-OpenBracket')
    keys['PageDown'].append('U0-CloseBracket')

    # 左手
    keys['Up'      ].append('U0-E')
    keys['Left'    ].append('U0-S')
    keys['Down'    ].append('U0-D')
    keys['Right'   ].append('U0-F')
    keys['Home'    ].append('U0-A')
    keys['End'     ].append('U0-G')
    keys['PageUp'  ].append('U0-W')
    keys['PageDown'].append('U0-R')
    keys['Enter'   ].append('U0-T')
    keys['Escape'  ].append('U0-Q')

    # 両手で対称
    keys['Back'  ].append('U0-Tab')
    keys['Delete'].append('U0-Atmark')

    # 矢印キー
    keys['PageUp'  ].append('U0-Up')
    keys['PageDown'].append('U0-Down')
    keys['Home'    ].append('U0-Left')
    keys['End'     ].append('U0-Right')


    # ランチャー(PowerToys Run)
    keymap_global['O-U0-LCtrl'] = 'A-Space'
    keymap_global['U0-Colon'] = 'A-Space'

    # 入力補助
    keymap_global['U0-Semicolon'] = keymap.defineMultiStrokeKeymap(";=%Y/%m/%d :=%H:%M:%S j=%Y%m%d k=%H%M%S v=Clipboard m=KeyhacMenu 2=\"\" 7='' @=`` 8=() 9=() [=[] ]=[] {={} }={} ,=<> .=<>")
    ## 日時入力
    keymap_global['U0-Semicolon']['Semicolon'] = lambda: keymap.InputTextCommand(datetime.datetime.now().strftime('%Y/%m/%d'))()
    keymap_global['U0-Semicolon']['Colon'] = lambda: keymap.InputTextCommand(datetime.datetime.now().strftime('%H:%M:%S'))()
    keymap_global['U0-Semicolon']['J'] = lambda: keymap.InputTextCommand(datetime.datetime.now().strftime('%Y%m%d'))()
    keymap_global['U0-Semicolon']['K'] = lambda: keymap.InputTextCommand(datetime.datetime.now().strftime('%H%M%S'))()
    ## リストウィンドウ
    keymap_global['U0-Semicolon']['V'] = keymap.command_ClipboardList
    keymap_global['U0-Semicolon']['M'] = command_KeyhacMenuList
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


    # アプリケーションで上書きされることもあるキー
    keymap_global['U0-Z'] = 'C-Z' # 戻る
    keymap_global['U0-X'] = 'C-W' # 閉じる
    keymap_global['U0-C'] = 'Up', 'End', 'S-Home' # 上の行を選択
    keymap_global['U0-V'] = 'Home', 'S-End', 'S-Right' # 現在の行を選択


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
    keys['Back'  ].append('RU1-H')
    keys['Delete'].append('RU1-L')

    # 無変換/変換を押していれば大きく移動
    keys['PageDown'].append('RU1-J')
    keys['PageUp'  ].append('RU1-K')

    # 無変換/変換でIMEを切替
    keymap_global['O-(29)'] = lambda: keymap.wnd.setImeStatus(0)
    keymap_global['O-(28)'] = lambda: keymap.wnd.setImeStatus(1)

    # ターミナルではCtrlの機能が変わるため無変換でショートカットを入力できるようにする アプリケーションによっては上書きする
    keymap_global['LU1-Z'] = 'C-Z'
    keymap_global['LU1-X'] = 'C-X'
    keymap_global['LU1-C'] = 'C-C'
    keymap_global['LU1-V'] = 'C-V'

    # ウィンドウの移動
    keymap_global['LU1-E'] = 'W-Up'
    keymap_global['LU1-S'] = 'W-Left'
    keymap_global['LU1-D'] = 'W-Down'
    keymap_global['LU1-F'] = 'W-Right'
    keymap_global['LU1-C-E'] = 'W-C-A-Up'
    keymap_global['LU1-C-S'] = 'W-C-A-Left'
    keymap_global['LU1-C-D'] = 'W-C-A-Down'
    keymap_global['LU1-C-F'] = 'W-C-A-Right'
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

    # FancyZonesのレイアウト変更
    global fancy_zone_layout
    fancy_zone_layout = 1
    def fancy_zone_layout_change_command(step):
        def run():
            global fancy_zone_layout
            fancy_zone_layout = (fancy_zone_layout + step - 1) % 9 + 1
            keymap.InputKeyCommand('W-C-A-' + str(fancy_zone_layout))()
        return run

    keymap_global[f'LU1-Q'] = fancy_zone_layout_change_command(-1)  # なぜかQを押すとモディファイアキーがキャンセルされる
    keymap_global[f'LU1-T'] = fancy_zone_layout_change_command(+1)


    # --------------------------------------------------------------------
    # コロン

    ## ワンショット
    for mod_key in MOD_KEYS_COMBS:
        keymap_global['O-' + mod_key + 'Colon'] = mod_key + 'Colon'

    ## 1段目 USキーボードの配列
    keymap_global['U3-Esc'] = keymap.InputTextCommand('~')
    for i, text in enumerate('!@#$%^&*(', start=1):
        keymap_global[f'U3-{i}'] = keymap.InputTextCommand(text)
    keymap_global['U3-0'] = keymap.InputTextCommand(')')

    ## 2段目
    ### JISキーボードの1段目の記号 Pに割当てはなし
    for i, key in enumerate('QWERTYUIO', start=1):
        keymap_global['U3-' + key] = f'S-{i}'
    ### Tabは独自割当て
    keymap_global['U3-Tab'] = 'Minus'

    ## 3段目 数字
    ### 左Ctrlは0
    keymap_global['D-U3-LCtrl']   = keymap.InputTextCommand('0') # 押されている間入力する
    keymap_global['D-C-U3-LCtrl'] = keymap.InputTextCommand('0') # 押されている間入力する
    ### 1-9
    for i, key in enumerate('ASDFGHJKL', start=1):
        keymap_global['U3-' + key] = str(i)
    ### 0
    keymap_global['U3-' + 'Semicolon'] = '0'

    ## 4段目 押しにくい記号
    keymap_global['D-U3-LShift']   = keymap.InputTextCommand('=') # 押されている間入力する
    keymap_global['D-S-U3-LShift'] = keymap.InputTextCommand('=') # 押されている間入力する
    keymap_global['U3-Z']          = 'Minus' # IMEオンの時にーを入力できるようにInputTextCommandは使わない
    keymap_global['U3-X']          = keymap.InputTextCommand('+')
    keymap_global['U3-C']          = keymap.InputTextCommand('*')
    keymap_global['U3-V']          = 'S-Caret' # IMEオンの時に～を入力できるようにInputTextCommandは使わない
    keymap_global['U3-B']          = keymap.InputTextCommand('|')
    keymap_global['U3-N']          = keymap.InputTextCommand('^') # USキーボードの位置から
    keymap_global['U3-M']          = keymap.InputTextCommand('$') # Vimのことを考えると^の右に$が欲しい
    keymap_global['U3-Comma']      = keymap.InputTextCommand('{')
    keymap_global['U3-Period']     = keymap.InputTextCommand('}')

    ## 5段目 押しにくい記号
    keymap_global['O-U3-(29)']  = keymap.InputTextCommand('`')
    keymap_global['O-U3-Space'] = keymap.InputTextCommand('_')
    keymap_global['O-U3-(28)']  = keymap.InputTextCommand('\\')

    # --------------------------------------------------------------------
    # フットスイッチ

    # フットスイッチ内
    keymap_global['O-' + KEY_FOOT_LEFT] = 'Esc'
    keymap_global[KEY_FOOT_CENTER] = 'Space'
    keymap_global['O-' + KEY_FOOT_RIGHT] = 'Enter'
    keymap_global['LU2-' + KEY_FOOT_CENTER] = 'Right'
    keymap_global['RU2-' + KEY_FOOT_CENTER] = 'Left'

    # フットスイッチとキーボード
    # フットスイッチをShiftにする
    for x in string.ascii_uppercase + string.digits:
        keymap_global['U2-' + x] = 'S-' + x
    for x in ('Minus', 'Caret', 'Yen', 'Atmark', 'OpenBracket', 'Plus', 'Colon', 'CloseBracket', 'Comma', 'Period', 'Slash', 'Underscore'):
        keymap_global['U2-' + x] = 'S-' + x

    # フットスイッチとテンキー
    keys['Insert'  ].append('U2-Num0')
    keys['Down'    ].append('U2-Num2')
    keys['Left'    ].append('U2-Num4')
    keys['Space'   ].append('U2-Num5')
    keys['Right'   ].append('U2-Num6')
    keys['Up'      ].append('U2-Num8')
    keys['Delete'  ].append('U2-Decimal')
    keys['Home'    ].append('U2-Divide')
    keys['PageUp'  ].append('U2-Subtract')
    keys['PageDown'].append('U2-Add')
    keys['End'     ].append('U2-Multiply')
    keymap_global['U2-Num1'] = 'Left', 'Down'
    keymap_global['U2-Num3'] = 'Right', 'Down'
    keymap_global['U2-Num7'] = 'Left', 'Up'
    keymap_global['U2-Num9'] = 'Right', 'Up'

    # --------------------------------------------------------------------
    # 機能観点

    # テキスト編集
    ## 単語削除
    keymap_global['U0-U1-H'] = 'C-Back'
    keymap_global['U0-U1-L'] = 'C-Delete'
    ## 行頭、行末まで削除
    keymap_global['RU1-U'] = 'S-Home', 'Back'
    keymap_global['RU1-O'] = 'S-End', 'Delete'
    keymap_global['LU1-A'] = 'S-Home', 'Back'
    keymap_global['LU1-G'] = 'S-End', 'Delete'
    ## 行削除
    keymap_global['U1-Tab']    = 'Left', 'Home', 'S-End', 'Delete', 'Delete' # 上の行を削除
    keymap_global['LU1-Atmark'] = 'Home', 'S-End', 'Delete', 'Delete' # 現在の行を削除 左右別に定義必要だった
    keymap_global['RU1-Atmark'] = 'Home', 'S-End', 'Delete', 'Delete' # 現在の行を削除 左右別に定義必要だった
    ## 行連結
    keymap_global['U0-U1-Tab']    = 'Home', 'Back', 'Home'
    keymap_global['U0-U1-Atmark'] = 'End', 'Delete', 'End'

    # ウィンドウ切替
    ## 左
    keymap_global['O-U0-LShift']  = 'D-Alt', 'S-Tab' # Alt+Shiftが実行されないようにしたいがやり方がわからない
    ## 右
    keymap_global['O-U0-RShift']  = 'D-Alt', 'Tab'   # Alt+Shiftが実行されないようにしたいがやり方がわからない
    keymap_global['U0-BackSlash'] = 'D-Alt', 'Tab'
    ## 確定時にAltのKeyUpを発生させる
    keymap_mvf = keymap.defineWindowKeymap(exe_name='explorer.exe', class_name='MultitaskingViewFrame')
    for key in ['U-Space'] + keys['Enter'] + keys['Escape']:
        keymap_mvf[key] = 'U-Alt'

    # 仮想デスクトップ
    keymap_global['U0-U1-BackSlash'] = 'W-C-D'
    keymap_global['U0-U1-S-BackSlash'] = 'W-C-F4'
    keymap_global['O-U1-LShift'] = 'W-C-Left'
    keymap_global['O-U1-RShift'] = 'W-C-Right'
    keymap_global['LU1-BackSlash'] = 'W-C-Right'
    keymap_global['RU1-BackSlash'] = 'W-C-Right'

    # --------------------------------------------------------------------
    # デフォルトのモディファイアキーと組み合わせて押すキーのマッピング
    for mod_key in MOD_KEYS_COMBS:
        for output_key, input_keys in keys.items():
            for input_key in input_keys:
                tokens = input_key.split('-')
                if tokens[0] in ['D', 'U', 'O']:
                    condition = tokens[0] + '-'
                    input_key = '-'.join(tokens[1:])
                else:
                    condition = ''
                    input_key = '-'.join(tokens)
                keymap_global[condition + mod_key + input_key] = mod_key + output_key

    # --------------------------------------------------------------------
    # アプリケーション別の設定

    # フットスイッチを矢印キーにするアプリケーション
    keymap_foot_arrow = keymap.defineWindowKeymap(check_func=lambda window: window.getProcessName() in ('mpc-be64.exe', 'Whirligig.exe'))
    keymap_foot_arrow['O-'     + KEY_FOOT_LEFT]  = lambda: None # ワンショットモディファイアを無効化
    keymap_foot_arrow['D-'     + KEY_FOOT_LEFT]  = 'D-Left'     # 押された瞬間にKeyDown
    keymap_foot_arrow['D-LU2-' + KEY_FOOT_LEFT]  = 'D-Left'     # 押されている間KeyDown
    keymap_foot_arrow['U-'     + KEY_FOOT_LEFT]  = 'U-Left'     # 離したときKeyUp
    keymap_foot_arrow['O-'     + KEY_FOOT_RIGHT] = lambda: None # ワンショットモディファイアを無効化
    keymap_foot_arrow['D-'     + KEY_FOOT_RIGHT] = 'D-Right'    # 押された瞬間にKeyDown
    keymap_foot_arrow['D-RU2-' + KEY_FOOT_RIGHT] = 'D-Right'    # 押されている間KeyDown
    keymap_foot_arrow['U-'     + KEY_FOOT_RIGHT] = 'U-Right'    # 離したときKeyUp

    # Explorer
    keymap_explorer = keymap.defineWindowKeymap(exe_name='explorer.exe')
    keymap_explorer['U0-Z'] = 'A-Up'
    keymap_explorer['U0-X'] = 'C-W'
    keymap_explorer['U0-M'] = 'A-Left'
    keymap_explorer['U0-Comma'] = 'A-Right'
    keymap_explorer['U0-Period'] = 'C-R'
    keymap_explorer['U0-I'] = 'F2'

    # ブラウザ
    keymap_browser = keymap.defineWindowKeymap(check_func=lambda window: window.getProcessName() in ('firefox.exe', 'chrome.exe', 'msedge.exe'))
    keymap_browser['U0-Z'] = 'C-S-T'
    keymap_browser['U0-X'] = 'C-W'
    keymap_browser['U0-C'] = 'C-PageUp'
    keymap_browser['U0-V'] = 'C-PageDown'
    keymap_browser['U0-N'] = 'C-T'
    keymap_browser['U0-M'] = 'A-Left'
    keymap_browser['U0-Comma'] = 'A-Right'
    keymap_browser['U0-Period'] = 'C-R'
    keymap_browser['U0-Slash'] = 'C-L'
    keymap_browser['U0-I'] = 'C-L'

    # mintty
    keymap_mintty = keymap.defineWindowKeymap(exe_name='mintty.exe')
    keymap_mintty['LU1-C'] = 'C-Insert' # コピー
    keymap_mintty['LU1-V'] = 'S-Insert' # 貼り付け
    keymap_mintty['LU1-A'] = 'C-U'
    keymap_mintty['LU1-G'] = 'C-O'
    keymap_mintty['RU1-U'] = 'C-U'
    keymap_mintty['RU1-O'] = 'C-O'

    # Windows Terminal
    keymap_windows_terminal = keymap.defineWindowKeymap(exe_name='WindowsTerminal.exe')
    keymap_windows_terminal['U0-Z'] = lambda: None
    keymap_windows_terminal['U0-X'] = 'C-S-W'
    keymap_windows_terminal['U0-C'] = 'C-S-Tab'
    keymap_windows_terminal['U0-V'] = 'C-Tab'
    keymap_windows_terminal['U0-N'] = 'C-S-T' # 新しいタブ
    keymap_windows_terminal['U0-Slash'] = 'C-S-P' # コマンドパレット
    keymap_windows_terminal['LU1-C'] = 'C-Insert' # コピー
    keymap_windows_terminal['LU1-V'] = 'S-Insert' # 貼り付け
    keymap_windows_terminal['LU1-A'] = 'C-U'
    keymap_windows_terminal['LU1-G'] = 'C-O'
    keymap_windows_terminal['RU1-U'] = 'C-U'
    keymap_windows_terminal['RU1-O'] = 'C-O'
    ## 単語削除 C-BackがC-Hになってしまい.inputrcで別々に変更できないため、keyhacで変更する
    for key in ['Back'] + keys['Back']:
        keymap_windows_terminal['C-' + key] = 'C-W'
    keymap_windows_terminal['U0-U1-H'] = 'C-W'

    # VLC
    keymap_vlc = keymap.defineWindowKeymap(exe_name='vlc.exe')
    keymap_vlc['U0-Z'] = 'C-J'
    keymap_vlc['U0-C'] = 'C-Left'
    keymap_vlc['U0-V'] = 'C-Right'
    keymap_vlc['U0-M'] = 'OpenBracket'
    keymap_vlc['U0-Comma'] = 'CloseBracket'
    keymap_vlc['U0-Period'] = 'A-C-Left'
    keymap_vlc['U0-Slash'] = 'A-C-Right'

    ## フットスイッチ
    ### 左右のスイッチを長押ししていたら0.5秒あたり30秒移動
    key_left = Key('Left')
    key_right = Key('Right')
    keymap_vlc['O-'     + KEY_FOOT_LEFT]  = lambda: None                                  # ワンショットモディファイアを無効化
    keymap_vlc['D-'     + KEY_FOOT_LEFT]  = key_left.inputCommand(count=3)                # 押された瞬間に入力
    keymap_vlc['D-LU2-' + KEY_FOOT_LEFT]  = key_left.inputCommand(count=3, interval=0.5)  # 押されている間入力
    keymap_vlc['O-'     + KEY_FOOT_RIGHT] = lambda: None                                  # ワンショットモディファイアを無効化
    keymap_vlc['D-'     + KEY_FOOT_RIGHT] = key_right.inputCommand(count=3)               # 押された瞬間に入力
    keymap_vlc['D-RU2-' + KEY_FOOT_RIGHT] = key_right.inputCommand(count=3, interval=0.5) # 押されている間入力

    ### 中央のスイッチで再生・一時停止
    keymap_vlc['D-' + KEY_FOOT_CENTER] = lambda: None # 長押しされても入力しない
    keymap_vlc['U-' + KEY_FOOT_CENTER] = 'Space' # 離されたときに入力する

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

    # Autodesk Fusion
    keymap_fusion360 = keymap.defineWindowKeymap(exe_name='Fusion360.exe')
    keymap_fusion360['O-' + KEY_FOOT_LEFT]  = lambda: None  # ワンショットモディファイアを無効化
    keymap_fusion360['D-' + KEY_FOOT_LEFT]  = 'D-S-MButton'
    keymap_fusion360['U-' + KEY_FOOT_LEFT]  = 'U-S-MButton'
    keymap_fusion360['O-' + KEY_FOOT_RIGHT] = lambda: None  # ワンショットモディファイアを無効化
    keymap_fusion360['D-' + KEY_FOOT_RIGHT] = 'D-MButton'
    keymap_fusion360['U-' + KEY_FOOT_RIGHT] = 'U-MButton'

    # Cura
    keymap_cura = keymap.defineWindowKeymap(exe_name='UltiMaker-Cura.exe')
    keymap_cura['O-' + KEY_FOOT_LEFT]  = lambda: None # ワンショットモディファイアを無効化
    keymap_cura['D-' + KEY_FOOT_LEFT]  = 'D-RButton'
    keymap_cura['U-' + KEY_FOOT_LEFT]  = 'U-RButton'
    keymap_cura['O-' + KEY_FOOT_RIGHT] = lambda: None # ワンショットモディファイアを無効化
    keymap_cura['D-' + KEY_FOOT_RIGHT] = 'D-MButton'
    keymap_cura['U-' + KEY_FOOT_RIGHT] = 'U-MButton'

    # PrusaSlicer
    keymap_prusa_slicer = keymap.defineWindowKeymap(exe_name='prusa-slicer.exe')
    keymap_prusa_slicer['O-' + KEY_FOOT_LEFT]  = lambda: None # ワンショットモディファイアを無効化
    keymap_prusa_slicer['D-' + KEY_FOOT_LEFT]  = 'D-LButton'
    keymap_prusa_slicer['U-' + KEY_FOOT_LEFT]  = 'U-LButton'
    keymap_prusa_slicer['O-' + KEY_FOOT_RIGHT] = lambda: None # ワンショットモディファイアを無効化
    keymap_prusa_slicer['D-' + KEY_FOOT_RIGHT] = 'D-MButton'
    keymap_prusa_slicer['U-' + KEY_FOOT_RIGHT] = 'U-MButton'

    # GnuCash
    keymap_gnucash = keymap.defineWindowKeymap(exe_name='gnucash.exe')
    keymap_gnucash['C-V'] = 'S-Insert' # Ctrlのショートカットキーが効かないのでCtrl-Vの代わりにShift-Insertを入力する

    # Visual Studio Code
    keymap_vsc = keymap.defineWindowKeymap(exe_name='Code.exe')
    keymap_vsc['U0-C'] = 'C-S-Tab'
    keymap_vsc['U0-V'] = 'C-Tab'
    keymap_vsc['U0-Slash'] = 'C-S-P' # コマンドパレット

    # --------------------------------------------------------------------
    # クリップボード

    # Add quote mark to current clipboard contents
    def quoteClipboardText():
        s = getClipboardText()
        lines = s.splitlines(True)
        s = ""
        for line in lines:
            s += keymap.quote_mark + line
        return s

    # Indent current clipboard contents
    def indentClipboardText():
        s = getClipboardText()
        lines = s.splitlines(True)
        s = ""
        for line in lines:
            if line.lstrip():
                line = " " * 4 + line
            s += line
        return s

    # Unindent current clipboard contents
    def unindentClipboardText():
        s = getClipboardText()
        lines = s.splitlines(True)
        s = ""
        for line in lines:
            for i in range(4+1):
                if i>=len(line) : break
                if line[i]=='\t':
                    i+=1
                    break
                if line[i]!=' ':
                    break
            s += line[i:]
        return s

    full_width_chars = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～０１２３４５６７８９　"
    half_width_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}～0123456789 "

    # Convert to half-with characters
    def toHalfWidthClipboardText():
        s = getClipboardText()
        s = s.translate(str.maketrans(full_width_chars,half_width_chars))
        return s

    # Convert to full-with characters
    def toFullWidthClipboardText():
        s = getClipboardText()
        s = s.translate(str.maketrans(half_width_chars,full_width_chars))
        return s

    # Menu item list
    other_items = [
        ("Quote clipboard",    quoteClipboardText),
        ("Indent clipboard",   indentClipboardText),
        ("Unindent clipboard", unindentClipboardText),
        ("To Half-Width",      toHalfWidthClipboardText),
        ("To Full-Width",      toFullWidthClipboardText),
        ("Edit config.py",     keymap.command_EditConfig),
        ("Reload config.py",   keymap.command_ReloadConfig),
    ]

    # Clipboard history list extensions
    keymap.cblisters += [
        ("Others", cblister_FixedPhrase(other_items)),
    ]

