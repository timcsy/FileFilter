# using UTF-8 encoding
# author: 張頌宇

import utils

def main():
    """主程式

    """
    input_root = input('Please enter the input folder (default: input): ')
    if input_root == '':
        input_root = 'input'
    output_root = input('Please enter the output folder (default: output): ')
    if output_root == '':
        output_root = 'output'

    tree = utils.get_files(input_root, output_root)

    for id in tree:
        for day in tree[id]:
            print("Start merging: " + day)
            utils.merge(tree[id][day])

if __name__ == "__main__":
    main()