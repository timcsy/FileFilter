FileFilter （CSV 醫學檔案資料過濾）
===

使用說明
---

### 安裝Python
官網：https://www.python.org/
找到載點後下載Python最新版並安裝
設定好環境變數：
教學(Windows)：https://ericjhang.github.io/archives/ad5450f3.html

### 下載本軟體
載點：https://github.com/timcsy/FileFilter/archive/master.zip
解壓縮到任意一個地方

之後參考input資料夾內的檔案分類範例：
最外面是受試者編號的資料夾，受試者資料夾「必須」要有一個time.txt檔案，可以複製範例去修改

time.txt 說明
```
#format: 每天的資料夾名稱(YYYYMMDD) 睡覺日期(YYYYMMDD) 睡覺時間(HH:MM) 起床日期(YYYYMMDD) 起床時間(HH:MM)
20190912 20190912 00:30 20190912 07:30
20190913 20190912 01:23 20190912 08:19
```

在受試者資料夾內有每天的資料夾，格式是(YYYYMMDD)，裡面放5種儀器的資料（「必須」是.csv檔）

執行app.py

輸入「輸入資料夾（input）」及「輸出資料夾（output）」，等待一陣子，過濾後的資料將會存在output資料夾內。