import os
import csv
import datetime

def file_path(in_folder, out_folder, keyword):
    input_file_path = ''
    output_file_path = ''
    if not os.path.exists(out_folder):
        try:
            os.makedirs(out_folder)
        except OSError:
            print("Creation of the directory %s failed" % out_folder)
    for file in os.listdir(in_folder):
        if file.find(keyword) != -1 and file.find('.csv') != -1:
            input_file_path = in_folder + '/' + file
            output_file_path = out_folder + '/' + file
            print("Start processing file: " + file)
            break
    return input_file_path, output_file_path

def airbox(in_folder, out_folder, start, end):
    input_file_path, output_file_path = file_path(in_folder, out_folder, 'AIRBOX')
    data = []
    if os.path.exists(input_file_path):
        with open(input_file_path) as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[0] != 'time':
                    date_time = datetime.datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S')
                    if start <= date_time and date_time <= end:
                        data.append(row)
                else:
                    data.append(row)
            csvfile.close()
    
    with open(output_file_path, 'w', newline='') as output:
        for row in data:
            output.write(','.join(row) + '\n')
        output.close()
    
    return data

def axivity(in_folder, out_folder, start, end):
    input_file_path, output_file_path = file_path(in_folder, out_folder, 'AXIVITY')
    data = []
    if os.path.exists(input_file_path):
        with open(input_file_path) as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[0] != 'time':
                    date_time = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
                    if start <= date_time and date_time <= end:
                        data.append(row)
                else:
                    data.append(row)
            csvfile.close()
    
    with open(output_file_path, 'w', newline='') as output:
        for row in data:
            output.write(','.join(row) + '\n')
        output.close()
    
    return data

def edimax(in_folder, out_folder, start, end):
    input_file_path, output_file_path = file_path(in_folder, out_folder, 'EDIMAX')
    data = []
    if os.path.exists(input_file_path):
        with open(input_file_path) as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[1] != 'time':
                    date_time = datetime.datetime.strptime(row[1], '%Y/%m/%d %H:%M')
                    if start <= date_time and date_time <= end:
                        data.append(row)
                else:
                    data.append(row)
            csvfile.close()
    
    with open(output_file_path, 'w', newline='') as output:
        for row in data:
            output.write(','.join(row) + '\n')
        output.close()

    return data

def hearthermo(in_folder, out_folder, start, end):
    input_file_path, output_file_path = file_path(in_folder, out_folder, 'HEARTHERMO')
    data = []
    if os.path.exists(input_file_path):
        with open(input_file_path) as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[1] != 'time':
                    date_time = datetime.datetime.strptime(row[0] + ' ' + row[1], '%Y-%m-%d %H:%M:%S')
                    if start <= date_time and date_time <= end:
                        data.append(row)
                else:
                    data.append(row)
            csvfile.close()
    
    with open(output_file_path, 'w', newline='') as output:
        for row in data:
            output.write('\"' + '\",\"'.join(row) + '\"\n')
        output.close()
    
    return data

def temppal(in_folder, out_folder, start, end):
    input_file_path, output_file_path = file_path(in_folder, out_folder, 'TEMPPAL')
    data = []
    if os.path.exists(input_file_path):
        with open(input_file_path) as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[2] != 'time ':
                    date_time = datetime.datetime.strptime(row[2], '%Y/%m/%d %H:%M')
                    if start <= date_time and date_time <= end:
                        data.append(row)
                else:
                    data.append(row)
            csvfile.close()
    
    with open(output_file_path, 'w', newline='') as output:
        for row in data:
            output.write(','.join(row) + '\n')
        output.close()
    
    return data