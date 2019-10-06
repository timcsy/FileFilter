# using UTF-8 encoding
# author: 張頌宇

import os # 內建的系統相關函式庫，這裡用來處理資料夾和檔案
import datetime # 內建的日期時間函式庫
import re # 內建的 Regular Expression (正則表達式)函式庫
import pandas as pd # 需要先安裝，而且還要再安裝xlrd

def parse_date(text):
    """分析日期字串

    Args:
        text (str): 日期字串

    Returns:
        datetime.datetime: 如果是日期就回傳datetime object
        bool: 否則回傳False

    """
    text = str(text).strip() # 去掉前後空白
    # 判斷格式
    try:
        return datetime.datetime.strptime(text, '%Y-%m-%d')
    except:
        try:
            return datetime.datetime.strptime(text, '%Y/%m/%d')
        except:
            try:
                return datetime.datetime.strptime(text, '%Y %m %d')
            except:
                return False

def parse_time(text):
    """分析時間字串

    Args:
        text (str): 時間字串

    Returns:
        datetime.datetime: 如果是時間就回傳datetime object
        bool: 否則回傳False

    """
    text = str(text).strip() # 去掉前後空白
    # 判斷格式
    try:
        return datetime.datetime.strptime(text, '%H:%M:%S')
    except:
        try:
            return datetime.datetime.strptime(text, '%H:%M:%S.%f')
        except:
            return False

def parse_datetime(text):
    """分析日期時間字串

    Args:
        text (str): 日期時間字串

    Returns:
        datetime.datetime: 如果是日期時間就回傳datetime object
        bool: 否則回傳False

    """
    text = str(text).strip() # 去掉前後空白
    # 判斷格式
    try:
        return datetime.datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
    except:
        try:
            return datetime.datetime.strptime(text, '%Y/%m/%d %H:%M:%S')
        except:
            try:
                return datetime.datetime.strptime(text, '%Y-%m-%d %H:%M')
            except:
                try:
                    return datetime.datetime.strptime(text, '%Y/%m/%d %H:%M')
                except:
                    try:
                        return datetime.datetime.strptime(text, '%Y%m%d %H:%M')
                    except:
                        try:
                            return datetime.datetime.strptime(text, '%Y-%m-%d %H:%M:%S.%f')
                        except:
                            try:
                                return datetime.datetime.strptime(text, '%Y/%m/%d %H:%M.%f')
                            except:
                                return False

def is_date(value):
    """判斷是否為日期字串

    Args:
        value (str): 日期字串

    Returns:
        bool: 是就回傳True，否則回傳False

    """
    if parse_date(value):
        return True
    else:
        return False

def is_time(value):
    """判斷是否為時間字串

    Args:
        value (str): 時間字串

    Returns:
        bool: 是就回傳True，否則回傳False

    """
    if parse_time(value):
        return True
    else:
        return False

def is_datetime(value):
    """判斷是否為日期時間字串

    Args:
        value (str): 日期時間字串

    Returns:
        bool: 是就回傳True，否則回傳False

    """
    if parse_datetime(value):
        return True
    else:
        return False

def read_times(file_path):
    """讀取time.txt

    Args:
        file_path (str): time.txt的檔案路徑

    Returns:
        dict: 回傳第幾天對應到的睡覺起床時間資料
        {
            day: [start, end]
        }

    """
    times = {}
    if os.path.exists(file_path) and os.path.isfile(file_path): # 檢查檔案是否存在
        with open(file_path) as time_file: # 開啟檔案
            lines = time_file.readlines() # 讀取一行
            for line in lines:
                if not line.startswith('#'):
                    row = line.replace('\r', '').replace('\n', '').strip().split(' ') # 去掉前後空白，以空格分隔這行並存成陣列
                    if len(row) == 5: # 符合格式設定
                        day = row[0] # 天數
                        start = parse_datetime(row[1] + ' ' + row[2]) # 睡覺時間
                        end = parse_datetime(row[3] + ' ' + row[4]) # 起床時間
                        times[day] = [start, end] # [0]: 睡覺時間, [1]: 起床時間
                    elif len(row) != 1: # len(row) == 1 時為空行
                        print(row)
                        print('The time.txt format is wrong!') # 格式錯誤
            time_file.close() # 關閉檔案
    return times

def get_info(filename, in_folder, out_folder, times):
    """獲取檔案資訊

    Args:
        filename (str): 檔案名稱
        in_folder (str): 讀入資料夾路徑
        out_folder (str): 輸出資料夾路徑
        times (dict): 時間資料

    Returns:
        dict: 檔案資訊
        {
            'filename': 檔名,
            'prefix': 在R以前的字串,
            'id': 受試者編號,
            'machine': 機器名稱（第一個單字）,
            'place': 測試位置,
            'day': 受試天數,
            'state': R（未修改）或C（已修改）,
            'suffix': 在R以後的字串,
            'extension': 副檔名（不含.）,
            'start': 睡覺時間,
            'end': 起床時間,
            'in': 讀入資料夾路徑,
            'out': 輸出資料夾路徑,
            'device': 裝置名稱簡寫
        }

    """
    info = None
    # 用 Regular Expression 找出檔名的一些關鍵部分
    match_object = re.search('(([^_]+)_([^_]+)_[^IO]*(I|O?).*_(D\d+)_)(R|C)(.*\.)(csv|xlsx)', filename)
    if match_object != None:
        info = {}
        info['filename'] = match_object.group(0) # e.g. 003_EDIMAX_D(O)_20190909_D1_R.xlsx
        info['prefix'] = match_object.group(1) # e.g. 003_EDIMAX_D(O)_20190909_D1_
        info['id'] = match_object.group(2) # e.g. 003
        info['machine'] = match_object.group(3) # e.g. EDIMAX
        info['place'] = match_object.group(4) # e.g. I
        info['day'] = match_object.group(5) # e.g. D1
        info['state'] = match_object.group(6) # e.g. R
        info['suffix'] = match_object.group(7) # e.g. .
        info['extension'] = match_object.group(8) # e.g. csv
        info['start'] = times[info['day']][0] # start
        info['end'] = times[info['day']][1] # end
        info['in'] = in_folder
        # 確保輸出資料夾存在，否則建立新資料夾
        if not os.path.exists(out_folder):
            try:
                os.makedirs(out_folder)
            except OSError:
                print("Creation of the directory %s failed" % out_folder)
        info['out'] = out_folder
        # 裝置名稱簡寫（機器＋地點）
        if info['machine'] == 'TEMPPAL':
            info['device'] = 'T'
        elif info['machine'] == 'HEARTHERMO':
            info['device'] = 'H'
        elif info['machine'] == 'AXIVITY':
            if info['suffix'] == '.':
                info['device'] = 'A'
            else:
                info['device'] = 'A_TL'
        elif info['machine'] == 'EDIMAX':
            if info['place'] == 'O':
                info['device'] = 'E_O'
            elif info['place'] == 'I':
                info['device'] = 'E_I'
            else:
                info['device'] = 'E'
        elif info['machine'] == 'AIRBOX':
            info['device'] = 'Air'

    return info

def get_files(input_root, output_root):
    """獲取資料夾與檔案架構

    Args:
        input_root (str): 讀入根目錄路徑
        output_root (str): 輸出根目錄路徑

    Returns:
        dict: 檔案架構樹
        {
            id: {
                day: [info]
            }
        }

    """
    tree = {}
    # 判斷輸入跟目錄是否存在
    if os.path.exists(input_root) and os.path.isdir(input_root):
        # 羅列出受試者
        for id_dir in os.listdir(input_root):
            id_path = input_root + '/' + id_dir
            # 判斷受試者目錄是否存在
            if os.path.exists(id_path) and os.path.isdir(id_path):
                print('id: ' + id_dir)
                # 讀取分析time.txt
                time_path = id_path + '/' + 'time.txt'
                if os.path.exists(time_path) and os.path.isfile(time_path):
                    times = read_times(time_path)

                    # 幫受試者的一天建一個list
                    tree[id_dir] = {}
                    for day in times:
                        tree[id_dir][day] = []
                    # 羅列機器目錄
                    for device_dir in os.listdir(id_path):
                        device_path = id_path + '/' + device_dir
                        output_path = output_root + '/' + id_dir + '/' + device_dir
                        if os.path.exists(device_path) and os.path.isdir(device_path):
                            # 讀取機器目錄下的檔案，並提取重要資訊並存到tree
                            for f in os.listdir(device_path):
                                info = get_info(f, device_path, output_path, times)
                                if info is not None:
                                    tree[info['id']][info['day']].append(info)
    return tree

def read_file(info):
    """讀取、處理檔案的資料

    Args:
        info (dict): 檔案資訊

    Returns:
        pd.DataFrame: 檔案的DataFrame（date和time會merge）

    """
    input_path = info['in'] + '/' + info['filename']
    print("Start processing file: " + input_path)
    if not os.path.exists(input_path):
        return
    
    # 依照檔案類型(.csv或.xlsx)及機器類型讀進檔案資料到df(pandas的Dataframe（表格）格式)
    df = None
    if info['extension'] == 'csv':
        if info['machine'] == 'AIRBOX' or info['machine'] == 'EDIMAX' or info['machine'] == 'TEMPPAL':
            # 去掉標題列
            df = pd.read_csv(input_path, header=None, skiprows=1)
        elif info['machine'] == 'AXIVITY' or info['machine'] == 'HEARTHERMO':
            # 本來就沒有標題列
            df = pd.read_csv(input_path, header=None)
    elif info['extension'] == 'xlsx':
        if info['machine'] == 'AIRBOX' or info['machine'] == 'EDIMAX' or info['machine'] == 'TEMPPAL':
            # 去掉標題列
            df = pd.read_excel(input_path, header=None, skiprows=1)
        elif info['machine'] == 'AXIVITY' or info['machine'] == 'HEARTHERMO':
            # 本來就沒有標題列
            df = pd.read_excel(input_path, header=None)
    
    return organize_datetime(df, info)

def organize_datetime(df, info):
    """整理篩選排序時間資料

    預設讀入是無標題列的
    假設如果這筆資料有2欄的時間格式，則把這兩行合併成一欄（經驗來說這兩行相鄰，先日期再時間）
    假設如果這筆資料有1欄的時間格式，這就是日期時間資料
    如果有兩行以上的時間資料，理論上不可能發生

    Args:
        df (pd.DataFrame): pandas資料

    Returns:
        pd.DataFrame: 整理篩選排序日期時間的資料

    """
    time = []
    if df is not None and len(df) > 0:
        # 檢查是否有日期時間格式
        for i in range(len(df.columns)):
            if isinstance(df.iloc[0,i], datetime.datetime) or is_date(df.iloc[0,i]) or is_time(df.iloc[0,i]) or is_datetime(df.iloc[0,i]):
                # 如果該欄位是日期時間格式，則記錄下來
                time.append(i)

    # 只有一欄代表它是日期＋時間
    if len(time) == 1:
        df.iloc[:,time[0]] = df.iloc[:,time[0]].apply(pd.to_datetime)
    # 有兩籃代表它日期時間分開
    elif len(time) == 2:
        df.iloc[:,time[0]] = pd.to_datetime(df.iloc[:,time[0]].astype(str) + ' ' + df.iloc[:,time[1]].astype(str))
        # 刪掉多於欄
        df = df.drop(columns=time[1])
    else:
        return
    
    # 只取時間範圍內的資料
    df = df.loc[(df.iloc[:,time[0]] >= info['start']) & (df.iloc[:,time[0]] <= info['end'])]
    # 將資料排序
    df = df.sort_values(by=time[0])

    return df

def cut(info):
    """過濾切割檔案

    Args:
        info (dict): 檔案資訊

    Returns:
        dict: 切割後資料
        {
            'device': 裝置名稱簡寫
            'header': [str（說明如下）],
            'df': pd.DataFrame: 檔案的DataFrame,
            'info': 檔案資訊
        }

        header of T: ['name','temperature (degree Celsius)','time']
        header of H: ['time','HR','temp','move']
        header of A: ['time','X_Axis','Y_Axis','Z_Axis']
        header of A_TL: ['time','X_Axis','Y_Axis','Z_Axis','temp (T = (counts – 171) / 3.142)','lux (Lux = 10(counts/341))']
        header of E_O: ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc']
        header of E_I: ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc']
        header of E: ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc']
        header of Air: ['time','CO2','PM1','PM2.5','PM10','PM0.3 cnt','PM0.5 cnt','PM1.0 cnt','PM2.5 cnt','PM5.0 cnt','PM10 cnt']

    """
    # 輸出命名規則
    output_path = info['out'] + '/' + info['prefix'] + 'C' + info['suffix'] + 'csv'

    df = read_file(info)
    if df is None:
        return
    
    # 各裝置對應到的標題列
    headers = {
        'T': ['name','temperature (degree Celsius)','time'],
        'H': ['time','HR','temp','move'],
        'A': ['time','X_Axis','Y_Axis','Z_Axis'],
        'A_TL': ['time','X_Axis','Y_Axis','Z_Axis','temp (T = (counts – 171) / 3.142)','lux (Lux = 10(counts/341))'],
        'E_O': ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc'],
        'E_I': ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc'],
        'E': ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc'],
        'Air': ['time','CO2','PM1','PM2.5','PM10','PM0.3 cnt','PM0.5 cnt','PM1.0 cnt','PM2.5 cnt','PM5.0 cnt','PM10 cnt']
    }
    data = {}
    data['device'] = info['device']
    data['header'] = headers[info['device']]
    data['df'] = df
    data['info'] = info

    # 輸出到個別檔案，附上標題列
    df.to_csv(output_path, header=data['header'], index=False, doublequote=False)
    
    return data

def select_mean(data, device, time, time_col, selected, step):
    """計算在時間區間內列的平均

    Args:
        data (dict): 一天內的資料表列表
        device (str): 裝置名稱
        time (datetime.datetime): 時間（秒）
        time_col (int): 時間所在欄
        selected (list): 所選擇欄位（針對可平均項目以0開始計算）
        step (datetime.timedelta): 時間間隔
    
    Returns:
        list: 平均資料

    """
    row = []
    df = None
    means = None
    if device in data:
        df = data[device]['df']
    # 沒有T+L資料就用一般的AXITIVITY資料
    elif device == 'A_TL' and 'A' in data:
        df = data['A']['df']
    
    # 計算時間區間內平均
    if df is not None:
        means = df.loc[(df.iloc[:,time_col] >= time) & (df.iloc[:,time_col] < time + step)].mean()
    
    # 沒有T+L資料就用一般的AXITIVITY資料
    if device == 'A_TL' and 'A_TL' not in data and means is not None:
        for i in range(0, 3):
            row.append(means.iloc[i])
        row += [None, None]
    # 一般狀況
    elif means is not None:
        for i in selected:
            row.append(means.iloc[i])
    # 如果沒資料或是其他意外狀況就填入None(NaN，not a number)
    else:
        for i in selected:
            row.append(None)
    return row

def merge(infos, output_root, seconds=1, microseconds=0, minutes=0, hours=0, days=0, weeks=0, milliseconds=0):
    """合併資料

    可以再做效能上的優化（但如果seconds=10速度會遠快於seconds=1）

    Args:
        infos (list): 同受試者同一天檔案資訊陣列
        output_root (str): 輸出根目錄
        seconds (int): 時間間隔的秒
        microseconds (int): 時間間隔的毫秒
        minutes (int): 時間間隔的分
        hours (int): 時間間隔的時
        days (int): 時間間隔的日
        weeks (int): 時間間隔的週
        milliseconds (int): 時間間隔的微秒
    
    Returns:
        pd.Dataframe: 合併後資料

    """
    data = {}
    info = None
    # 過濾一天中每台機器資料並存起來
    for information in infos:
        cut_data = cut(information)
        # 取得該天的基本資訊
        if info is None:
            info = {
                'id': cut_data['info']['id'],
                'day': cut_data['info']['day'],
                'start': cut_data['info']['start'],
                'end': cut_data['info']['end']
            }
        data[cut_data['device']] = cut_data
    
    # Start merging
    out_folder = output_root + '/' + info['id'] + '/' + info['id'] + '_MERGE'
    # 確保輸出資料夾存在，否則建立新資料夾
    if not os.path.exists(out_folder):
        try:
            os.makedirs(out_folder)
        except OSError:
            print("Creation of the directory %s failed" % out_folder)
    # output檔案
    output_path = out_folder + '/' + info['id'] + '_' + info['day'] + '.csv'
    print("Start merging: " + output_path)

    # 刪除不需要用到，但值可能是數字的欄位
    if 'T' in data:
        data['T']['df'] = data['T']['df'].drop(columns=0) # name
    if 'E_O' in data:
        data['E_O']['df'] = data['E_O']['df'].drop(columns=0) # device
    if 'E_I' in data:
        data['E_I']['df'] = data['E_I']['df'].drop(columns=0) # device
    if 'E' in data:
        data['E']['df'] = data['E']['df'].drop(columns=0) # device

    df = None # 要輸出的表格
    # D1-D3 使用的欄位名稱
    if info['day'] == 'D1' or info['day'] == 'D2' or info['day'] == 'D3':
        df = pd.DataFrame(columns=['Time', 'temp_T', 'HR_H', 'temp_H', 'move_H' , 'X_Axis_A', 'Y_Axis_A', 'Z_Axis_A', 'temp_A (T = (counts – 171) / 3.142)', 'lux_A (Lux = 10(counts/341))', 'pm25_E_O', 'pm10_E_O', 'pm1_E_O', 't_E_O', 'h_E_O', 'co2_E_O', 'co_E_O', 'hcho_E_O', 'tvoc_E_O', 'pm25_E_I', 'pm10_E_I', 'pm1_E_I', 't_E_I', 'h_E_I', 'co2_E_I', 'co_E_I', 'hcho_E_I', 'tvoc_E_I', 'CO2_Air', 'PM1_Air', 'PM2.5_Air', 'PM10_Air', 'PM0.3_Air', 'PM0.5_Air', 'PM1.0_Air', 'PM2.5_Air', 'PM5.0_Air', 'PM10_Air'])
    # D4-D6 使用的欄位名稱
    elif info['day'] == 'D4' or info['day'] == 'D5' or info['day'] == 'D6':
        df = pd.DataFrame(columns=['Time', 'temp_T', 'HR_H', 'temp_H', 'move_H' , 'X_Axis_A', 'Y_Axis_A', 'Z_Axis_A', 'temp_A (T = (counts ??171) / 3.142)', 'lux_A (Lux = 10(counts/341))', 'pm25_E', 'pm10_E', 'pm1_E', 't_E', 'h_E', 'co2_E', 'co_E', 'hcho_E', 'tvoc_E'])
    else:
        return

    # 時間區間多寬
    step = datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)
    # 開始合併資料
    time = info['start']
    while time <= info['end']:
        row = [time] # Time
        row += select_mean(data, 'T', time, 1, range(0, 1), step) # T
        row += select_mean(data, 'H', time, 0, range(0, 3), step) # H
        row += select_mean(data, 'A_TL', time, 0, range(0, 5), step) # H
        if info['day'] == 'D1' or info['day'] == 'D2' or info['day'] == 'D3':
            row += select_mean(data, 'E_O', time, 0, range(0, 9), step) # E_O
            row += select_mean(data, 'E_I', time, 0, range(0, 9), step) # E_I
            row += select_mean(data, 'Air', time, 0, range(0, 10), step) # Air
        elif info['day'] == 'D4' or info['day'] == 'D5' or info['day'] == 'D6':
            row += select_mean(data, 'E', time, 0, range(0, 9), step) # E
        
        # 檢查是否全部欄位都空白
        not_blank = False
        for item in row:
            if item is not None:
                not_blank = True
                break
        # 如果不是全部欄位都空白，則加入這列
        if not_blank:
            # 如果時間是整點，顯示一下進度
            if time.minute == 0 and time.second == 0:
                print(time)
            # 加入這一列
            df = df.append(pd.Series(row, index=df.columns), ignore_index=True)

        time += step

    # 輸出合併後檔案，附上標題列
    df.to_csv(output_path, index=False, doublequote=False)

    return df