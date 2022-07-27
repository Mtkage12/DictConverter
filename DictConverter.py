import os
import glob
import pandas as pd
import pyperclip as pp
from tkinter import messagebox

class Method:
    @classmethod
    def test(cls):
        return {'4001':'あ', '5001':'い', '123':'う', '1224':'え'}
    @classmethod
    def read_pkl(cls):
        file = glob.glob('*.pkl')[0]
        df = pd.read_pickle(file)
        return dict(zip(df[df.columns[0]],df[df.columns[1]]))
    
class Dic:
    def __init__(self):
        # テスト環境
        # self.dic = Method.test()
        # 本番環境
        self.dic = Method.read_pkl()

def main():
    # 辞書データの読み込み
    d = Dic().dic
    
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
    
