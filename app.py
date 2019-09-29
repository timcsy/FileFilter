import os
import utils
import datetime
import csv

def filter(in_folder, out_folder, start, end):
    utils.airbox(in_folder, out_folder, start, end)
    utils.axivity(in_folder, out_folder, start, end)
    utils.edimax(in_folder, out_folder, start, end)
    utils.hearthermo(in_folder, out_folder, start, end)
    utils.temppal(in_folder, out_folder, start, end)

def main():
    input_root = input('Please enter the input folder (e.g. input): ')
    output_root = input('Please enter the input folder (e.g. output): ')

    if os.path.exists(input_root):
        for user_dir in os.listdir(input_root):
            user_path = input_root + '/' + user_dir
            if os.path.exists(user_path) and os.path.isdir(user_path):
                print('id: ' + user_dir)
                for f in os.listdir(user_path):
                    if f.find('time') != -1:
                        with open(user_path + '/' + f) as time:
                            lines = time.readlines()
                            for line in lines:
                                if not line.startswith('#'):
                                    row = line.strip().split(' ')
                                    in_folder = user_path + '/' + row[0]
                                    out_folder = output_root + '/' + user_dir + '/' + row[0]
                                    start = datetime.datetime.strptime(row[1] + ' ' + row[2], '%Y%m%d %H:%M')
                                    end = datetime.datetime.strptime(row[3] + ' ' + row[4], '%Y%m%d %H:%M')
                                    if os.path.exists(in_folder):
                                        print('folder: ' + row[0] + ' from ' + str(start) + ' to ' + str(end))
                                        filter(in_folder, out_folder, start, end)

if __name__ == "__main__":
    main()