# using UTF-8 encoding
# author: 張頌宇

import utils # utils.py

def main():
    """主程式

    """
    # 輸入根目錄
    input_root = input('Please enter the input folder (default: input): ')
    if input_root == '':
        input_root = 'input'
    # 輸出根目錄
    output_root = input('Please enter the output folder (default: output): ')
    if output_root == '':
        output_root = 'output'
    # 時間間隔
    step = input('Please enter the merge step in seconds (default: 1): ')
    if step == '':
        step = '1'

    # 檔案架構樹
    tree = utils.get_files(input_root, output_root) # utils.py裡面的get_files函式

    # 開始合併每位受試者每天的資料
    for id in tree:
        for day in tree[id]:
            print("Start: " + day)
            utils.merge(tree[id][day], output_root, seconds=int(step)) # utils.py裡面的merge函式

if __name__ == "__main__":
    # 開始執行主程式
    main()