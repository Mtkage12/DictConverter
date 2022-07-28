import os
import sys
import pandas as pd
import pyperclip as pp
from pathlib import Path
from tkinter import messagebox

class Arg:
    def __init__(self) -> None:
        self.target_file = sys.argv[-1]
        self.dic = {}
        self.alert_msg = ""
        self.flag = False
        self.suffix = Path(self.target_file).suffix
        if self.suffix == '.pkl':
            self.read_pkl()
        elif self.suffix == '.csv':
            self.read_csv()
        elif self.target_file == os.path.abspath(__file__):
            self.test()
        else:
            self.flag = True
            self.alert_msg = "想定外の拡張子が読み込まれました"
    def test(self):
        self.dic = {'4001':'あ', '5001':'い', '123':'う', '1224':'え'}
    def read_pkl(self):
        df = pd.read_pickle(self.target_file)
        self.dic = dict(zip(df[df.columns[0]],df[df.columns[1]]))
    def read_csv(self):
        df = pd.read_csv(self.target_file, encoding='cp932', header=None, dtype=str)
        self.dic = dict(zip(df[df.columns[0]],df[df.columns[1]]))

class Engine:
    def __init__(self):
        arg = Arg()
        self.dic = arg.dic
        self.alert_msg = arg.alert_msg
        self.flag = arg.flag
        
def main():
    # D＆Dファイルがpklファイル、csvファイル以外なら処理中止
    engine = Engine()
    if engine.flag==True:
        messagebox.showinfo('中止', engine.alert_msg)
        sys.exit()
    else:
        pass
    
    # 辞書データの読み込み
    d = engine.dic
    
    # クリップボードから文字列取得
    bb = pp.paste()
    lsts = bb.splitlines()
    
    # 辞書から値を取得
    func = lambda x : d.get(x, "")
    buf = [func(lst) for lst in lsts]
    
    # リストをクリップボードにコピー
    word = '\n'.join(buf)
    pp.copy(word+'\n')
    
    # メッセージを表示
    messagebox.showinfo('完了', 'クリップボードにコピーしました')

if __name__ == '__main__':
    os.chdir(os.getcwd())
    main()
    
