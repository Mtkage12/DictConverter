import os
import sys
import pandas as pd
import pyperclip as pp
from pathlib import Path
from tkinter import messagebox

class Argv:
    def __init__(self, argv) -> None:
        self.target_file = argv
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

class Argvs:
    # Argvをまとめたクラス
    books = []
    flags = False
    dics= {}
    def __init__(self) -> None:
        print(sys.argv)
        if len(sys.argv) > 1:
            for idx in range(1,len(sys.argv)):
                print(sys.argv[idx])
                Argvs.books(Argv(sys.argv[idx]))
        else:
            Argvs.books.append(Argv(sys.argv[-1]))
        self.merge_dict()
        self.merge_flags()
        
    def merge_flags(self):
        flags = [book.flag for book in Argvs.books]
        if True in flags:
            Argvs.flags = True 
        else:
            pass

    def merge_dict(self):
        buf_dic = {}
        for book in Argvs.books:
            buf_dic.update(book.dic)
        Argvs.dics = buf_dic

class Engine:
    # 単一想定用取り込みクラス
    def __init__(self):
        argv = Argv(sys.argv[-1])
        self.dic = argv.dic
        self.alert_msg = argv.alert_msg
        self.flag = argv.flag

class Switch_Engine:
    # 複数想定用取り込みクラス
    def __init__(self):
        argvs = Argvs()
        print(argvs.dics)
        self.dic = argvs.dics
        self.flag = argvs.flags
        
def main():
    # D&Dファイルが単一
    engine = Engine()
    
    # D&Dファイルが複数
    # engine = Switch_Engine()
    
    # D＆Dファイルがpklファイル、csvファイル以外なら処理中止
    if engine.flag==True:
        messagebox.showinfo('中止', '想定外のエラー')
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
    
