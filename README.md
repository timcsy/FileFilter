FileFilter （睡眠與空氣品質檔案資料過濾）
===

使用說明
---

### 安裝Python
官網：https://www.python.org/
找到載點後下載Python最新版並安裝
設定好環境變數：
教學(Windows)：https://ericjhang.github.io/archives/ad5450f3.html

### 安裝套件
在終端機(在Windows為命令提示字元，開始->所有程式->附屬應用程式->命令提示字元)輸入：
```
pip install pandas xlrd
```
如果未安裝pip，請參考[教學](https://medium.com/@CCstruggled/python-%E5%AE%89%E8%A3%9D-pip-%E6%96%BC-windows-%E6%88%96-centos-%E7%B7%9A%E4%B8%8A-%E9%9B%A2%E7%B7%9A%E5%AE%89%E8%A3%9D-pip-101-fb6d8e3c611b)
但一般情況下安裝python時就會附帶安裝pip了，除非你沒打勾

### 下載本軟體
載點：https://github.com/timcsy/FileFilter/archive/master.zip
解壓縮到任意一個地方

### 輸入資料格式說明
input資料夾內的檔案分類範例：
```
輸入資料的根目錄
|- 受試者1
   |- 受試者1_機器1
      |- 受試者1_機器1_D1_R.csv
      |- 受試者1_機器1_D1_R_T+L.csv
      |- 受試者1_機器1_D1_R.xlsx
      |- ...
   |- ...
   |- time.txt
|- ...
```
最外面是受試者編號的資料夾，受試者資料夾「必須」要有一個time.txt檔案，可以複製範例去修改

### time.txt 說明
範例：
```
# format: 每天的資料夾名稱(Dn) 睡覺日期(YYYYMMDD) 睡覺時間(HH:MM) 起床日期(YYYYMMDD) 起床時間(HH:MM)

D1 20190912 00:30 20190912 07:30
D2 20190913 01:23 20190913 08:19

```

在受試者資料夾內有每個儀器的資料夾，裡面放該儀器的資料（「必須」是.csv或是.xlsx檔）

### 執行app.py
Windows: 點開start.bat

Mac: 打開終端機，切換到當前工作目錄

輸入以下指令並Enter
```
python app.py
```
輸入「輸入資料夾（input）」，

輸入「輸出資料夾（output）」，

輸入「時間間隔」，就是說合併的資料中時間間距要多少（以秒為單位）

等待一陣子，過濾、合併後的資料將會存在output資料夾內。

過濾後的檔案會將檔名的R改成C並存在原機器名的資料夾下、合併後的檔案(D1-D6)會存在MERGE資料夾內

如果要中斷執行，就按Ctrl + C

欄位及格式說明
---

### 時間
統一以
```
YYYY-MM-DD HH:mm:ss
```
表示

### 空資料
就空著，對，就是這樣

### TEMPPAL
簡寫為「T」
出現在D1-D6
以下為逗號分隔的欄位名稱
```
name,temperature (degree Celsius),time
```

### HEARTHERMO
簡寫為「H」
出現在D1-D6
以下為逗號分隔的欄位名稱
```
time,HR,temp,move
```

### AXIVITY
分兩種：

沒有溫度和照度的簡寫為「A」
出現在D1-D6
以下為逗號分隔的欄位名稱
```
time,X_Axis,Y_Axis,Z_Axis
```

有溫度和照度的簡寫為「A_TL」
出現在D1-D6
以下為逗號分隔的欄位名稱
```
time,X_Axis,Y_Axis,Z_Axis,temp (T = (counts – 171) / 3.142),lux (Lux = 10(counts/341))
```

### EDIMAX
分三種：

外面的簡寫為「E_O」
出現在D1-D3
以下為逗號分隔的欄位名稱
```
decice,time,pm25,pm10,pm1,t,h,co2,co,hcho,tvoc
```

裡面的簡寫為「E_I」
出現在D1-D3
以下為逗號分隔的欄位名稱
```
decice,time,pm25,pm10,pm1,t,h,co2,co,hcho,tvoc
```

回家的簡寫為「E」
出現在D4-D6
以下為逗號分隔的欄位名稱
```
decice,time,pm25,pm10,pm1,t,h,co2,co,hcho,tvoc
```

### AIRBOX
簡寫為「Air」
出現在D1-D3
以下為逗號分隔的欄位名稱
```
time,CO2,PM1,PM2.5,PM10,PM0.3 cnt,PM0.5 cnt,PM1.0 cnt,PM2.5 cnt,PM5.0 cnt,PM10 cnt
```

### MERGE（合併後）
分兩種：

以下為D1-D3以逗號分隔的欄位名稱
```
Time,temp_T,HR_H,temp_H,move_H,X_Axis_A,Y_Axis_A,Z_Axis_A,temp_A (T = (counts – 171) / 3.142),lux_A (Lux = 10(counts/341)),pm25_E_O,pm10_E_O,pm1_E_O,t_E_O,h_E_O,co2_E_O,co_E_O,hcho_E_O,tvoc_E_O,pm25_E_I,pm10_E_I,pm1_E_I,t_E_I,h_E_I,co2_E_I,co_E_I,hcho_E_I,tvoc_E_I,CO2_Air,PM1_Air,PM2.5_Air,PM10_Air,PM0.3_Air,PM0.5_Air,PM1.0_Air,PM2.5_Air,PM5.0_Air,PM10_Air
```

以下為D4-D6以逗號分隔的欄位名稱
```
Time,temp_T,HR_H,temp_H,move_H,X_Axis_A,Y_Axis_A,Z_Axis_A,temp_A (T = (counts ??171) / 3.142),lux_A (Lux = 10(counts/341)),pm25_E,pm10_E,pm1_E,t_E,h_E,co2_E,co_E,hcho_E,tvoc_E
```