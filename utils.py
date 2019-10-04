# using UTF-8 encoding
# author: 張頌宇

import os
import csv
import datetime
import re
from openpyxl import load_workbook

def parse_date(text):
    """分析日期字串

    Args:
        text (str): 日期字串

    Returns:
        datetime.datetime: 如果是日期就回傳datetime object
        bool: 否則回傳False

    """
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

def is_date(text):
    """判斷是否為日期字串

    Args:
        text (str): 日期字串

    Returns:
        bool: 是就回傳True，否則回傳False

    """
    if parse_date(text) is not None:
        return True
    else:
        return False

def is_time(text):
    """判斷是否為時間字串

    Args:
        text (str): 時間字串

    Returns:
        bool: 是就回傳True，否則回傳False

    """
    if parse_time(text):
        return True
    else:
        return False

def is_datetime(text):
    """判斷是否為日期時間字串

    Args:
        text (str): 日期時間字串

    Returns:
        bool: 是就回傳True，否則回傳False

    """
    if parse_datetime(text):
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
                if not line.startswith('#') or not line == '':
                    row = line.strip().split(' ') # 以空格分隔這行並存成陣列
                    day = row[0] # 天數
                    start = parse_datetime(row[1] + ' ' + row[2]) # 睡覺時間
                    end = parse_datetime(row[3] + ' ' + row[4]) # 起床時間
                    times[day] = [start, end] # [0]: 睡覺時間, [1]: 起床時間
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
            'device': 機器名稱（第一個單字）,
            'place': 測試位置,
            'day': 受試天數,
            'state': R（未修改）或C（已修改）,
            'suffix': 在R以後的字串,
            'extension': 副檔名（不含.）,
            'start': 睡覺時間,
            'end': 起床時間,
            'in': 讀入資料夾路徑,
            'out': 輸出資料夾路徑
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
        info['device'] = match_object.group(3) # e.g. EDIMAX
        info['place'] = match_object.group(4) # e.g. I
        info['day'] = match_object.group(5) # e.g. D1
        info['state'] = match_object.group(6) # e.g. R
        info['suffix'] = match_object.group(7) # e.g. .
        info['extension'] = match_object.group(8) # e.g. csv
        info['start'] = times[info['day']][0]
        info['end'] = times[info['day']][1]
        info['in'] = in_folder
        # 確保輸出資料夾存在，否則建立新資料夾
        if not os.path.exists(out_folder):
            try:
                os.makedirs(out_folder)
            except OSError:
                print("Creation of the directory %s failed" % out_folder)
        info['out'] = out_folder
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
    if os.path.exists(input_root) and os.path.isdir(input_root):
        for id_dir in os.listdir(input_root):
            id_path = input_root + '/' + id_dir
            if os.path.exists(id_path) and os.path.isdir(id_path):
                print('id: ' + id_dir)
                time_path = id_path + '/' + 'time.txt'
                if os.path.exists(time_path) and os.path.isfile(time_path):
                    times = read_times(time_path)

                    tree[id_dir] = {}
                    for day in times:
                        tree[id_dir][day] = []
                    for device_dir in os.listdir(id_path):
                        device_path = id_path + '/' + device_dir
                        output_path = output_root + '/' + id_dir + '/' + device_dir
                        if os.path.exists(device_path) and os.path.isdir(device_path):
                            for f in os.listdir(device_path):
                                info = get_info(f, device_path, output_path, times)
                                if info is not None:
                                    tree[info['id']][info['day']].append(info)
    return tree

def read_rows(info):
    """讀取檔案的列資料

    Args:
        info (dict): 檔案資訊

    Returns:
        list: row的每個元素（date和time會merge）

    """
    input_path = info['in'] + '/' + info['filename']
    print("Start processing file: " + input_path)
    if not os.path.exists(input_path):
        return

    rows = []
    if info['extension'] == 'csv':
        with open(input_path) as fin:
            for row in csv.reader(fin):
                # 用 Regular Expression 找出標題列
                match_object = re.search('[A-Za-z]+', row[1])
                if match_object == None: # 這行非標題列
                    r = []
                    time = ''
                    for v in row:
                        match_object = re.search('\"?([^\"]*)\"?', v)
                        if match_object != None:
                            value = match_object.group(1)
                            if parse_date(value) != False:
                                time = value
                            elif parse_time(value) != False:
                                time += value
                                r.append(parse_datetime(time))
                            elif parse_datetime(value) != False:
                                time = value
                                r.append(parse_datetime(time))
                            else:
                                r.append(value)
                    rows.append(r)
    elif info['extension'] == 'xlsx':
        wb = load_workbook(input_path)
        ws = wb.active
        for row in ws.rows:
            r = []
            time = None
            for cell in row:
                if isinstance(cell.value, datetime.datetime):
                    if time == None:
                        time = cell.value
                    else:
                        time += cell.value
                        r.append(time)
                else:
                    r.append(cell.value)
            rows.append(r)

    return rows

def get_time(row, info):
    """取得時間

    Args:
        row (list): 列資訊
        info (dict): 檔案資訊

    Returns:
        datetime.datetime: 日期時間

    """
    if info['device'] == 'EDIMAX':
        return row[1]
    elif info['device'] == 'TEMPPAL':
        return row[2]
    else:
        return row[0]

def to_str(x, device):
    """過濾切割檔案

    Args:
        x (str or datetime.datetime): 任意值
        device (str): 裝置名稱簡寫

    Returns:
        str: 轉換後的字串

    """
    if isinstance(x, datetime.datetime):
        if device == 'A' or device == 'A_TL':
            return x.strftime('%Y-%m-%d %H:%M:%S.%3f')
        else:
            return x.strftime('%Y-%m-%d %H:%M:%S')
    return str(x)

def cut(info):
    """過濾切割檔案

    Args:
        info (dict): 檔案資訊

    Returns:
        dict: 切割後資料
        {
            'device': 裝置名稱簡寫
            'header': [str（說明如下）],
            'rows': [[value]],
            'info': 檔案資訊
        }

        header of T: ['name','temperature (degree Celsius)','time']
        header of H: ['time','HR','temp','move']
        header of A: ['time','X_Axis','Y_Axis','Z_Axis']
        header of A_TL: ['time','X_Axis','Y_Axis','Z_Axis','temp (T = (counts – 171) / 3.142)','lux (Lux = 10(counts/341))']
        header of E_O: ['decice'?,'time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc']
        header of E_I: ['decice'?,'time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc']
        header of E: ['decice'?,'time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc']
        header of Air: ['time',' CO2',' PM1',' PM2.5',' PM10',' PM0.3 cnt',' PM0.5 cnt',' PM1.0 cnt',' PM2.5 cnt',' PM5.0 cnt',' PM10 cnt']

    """
    output_path = info['out'] + '/' + info['prefix'] + 'C' + info['suffix'] + 'csv'

    rows = read_rows(info)
    if rows is None:
        return
    rows = list(filter(lambda row: (info['start'] <= get_time(row, info)) and (get_time(row, info) <= info['end']), rows))
    rows.sort(key=lambda row: get_time(row, info))

    data = {}

    if info['device'] == 'TEMPPAL':
        data['device'] = 'T'
    elif info['device'] == 'HEARTHERMO':
        data['device'] = 'HEARTHERMO'
    elif info['device'] == 'AXIVITY':
        if info['suffix'] == '.':
            data['device'] = 'A'
        else:
            data['device'] = 'A_TL'
    elif info['device'] == 'EDIMAX':
        if info['place'] == 'O':
            data['device'] = 'E_O'
        elif info['place'] == 'I':
            data['device'] = 'E_I'
        else:
            data['device'] = 'E'
    elif info['device'] == 'AIRBOX':
        data['device'] = 'Air'

    headers = {
        'T': ['name','temperature (degree Celsius)','time'],
        'H': ['time','HR','temp','move'],
        'A': ['time','X_Axis','Y_Axis','Z_Axis'],
        'A_TL': ['time','X_Axis','Y_Axis','Z_Axis','temp (T = (counts – 171) / 3.142)','lux (Lux = 10(counts/341))'],
        'E_O': ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc'],
        'E_I': ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc'],
        'E': ['decice','time','pm25','pm10','pm1','t','h','co2','co','hcho','tvoc'],
        'Air': ['time',' CO2',' PM1',' PM2.5',' PM10',' PM0.3 cnt',' PM0.5 cnt',' PM1.0 cnt',' PM2.5 cnt',' PM5.0 cnt',' PM10 cnt']
    }

    data['header'] = headers[data['device']]
    data['rows'] = rows
    data['info'] = info
    
    with open(output_path, 'w', newline='') as fout:
        fout.write(','.join(data['header']) + '\n')
        for row in rows:
            fout.write(','.join([s for s in map(lambda x: to_str(x, data['device']), row)]) + '\n')
        fout.close()
    
    return data

def merge(infos):
    """合併資料

    Args:
        infos (array): 檔案資訊陣列

    """
    for info in infos:
        cut(info)
    
    # Start merging