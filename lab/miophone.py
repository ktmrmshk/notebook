# -*- coding: utf-8 -*-

import pandas as pd
import os
from datetime import time, datetime

class miophone(object):
    def __init__(self):
        self.df = pd.DataFrame()

    def addFractDigit(self, s):
        '''
        in, out
        12.45 => 12.450000
        1.0 =>    1.000000
        12  => 12
        '''
        cnt=0
        in_fract = False
        for i in range(len(s)):
            if s[i] == '.':
                in_fract = True
            elif in_fract:
                cnt+=1
        if cnt > 0 and cnt < 6:
            s+='0'*(6-cnt)
        return s

    def scanMioService(self, df_orig):
        '''
        out: d_time, dur, miophone, familycall
        '''
        d_time=list()
        dur=list()
        miophone=list()
        familycall=list()
        for i, r in df_orig.iterrows():
            # d_time
            s='{} {}'.format(r['通話年月日'], r['通話開始時刻'])
            t=datetime.strptime(s, '%Y%m%d %H:%M:%S')
            d_time.append(t)

            # dur
            d=time.fromisoformat(self.addFractDigit( r['通話時間'] ))
            d_sec = 3600*d.hour + 60 * d.minute + d.second + d.microsecond *1e-6
            dur.append(d_sec)

            # miophone
            if pd.isnull( r['通話の種類'] ):
                miophone.append(False)
            else:
                miophone.append(True)

            # family call
            if r['ファミリー通話割引'] == '-':
                familycall.append(False)
            else:
                familycall.append(True)


        return d_time, dur, miophone, familycall


    def read_mio_csv(self, path):
        # add ending ',' to first line
        buf=None
        with open(path, 'r', encoding='shift_jis') as f:
            buf = f.read()

        lines = buf.split('\n')
        lines[0]+=','
        new_buf = '\n'.join(lines)
        tmp_file = path+'.tmp'
        with open(tmp_file, 'w', encoding='utf-8') as f:
            f.write(new_buf)

        # read from csv
        df_orig = pd.read_csv(tmp_file, dtype = {'お客様の電話番号':'object', '通話先電話番号':'object'})

        # rm tmp_file
        os.remove(tmp_file)

        ### set new data
        self.df['from'] = df_orig['お客様の電話番号']
        self.df['to'] = df_orig['通話先電話番号']
        self.df['toll'] = df_orig['料金']
        d_time, dur, miophone, familycall = self.scanMioService(df_orig)
        self.df['datetime'] = d_time
        self.df['dur'] = dur
        self.df['miophone'] = miophone
        self.df['familycall'] = familycall

def do_test():
    mio=miophone()
    mio.read_mio_csv('call_log.csv')
    print(mio.df.head())

if __name__ == '__main__':
    do_test()


