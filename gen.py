import os
import argparse


def main(file, output):
    exec_cmd = f"pyinstaller -F -w {file} -n {output}"
    os.system(exec_cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="implant 生成工具")
    parser.add_argument("-f", "--file", dest="file", help="input a file")
    parser.add_argument("-o", "--output", dest="output", help="save file path")
    args = parser.parse_args()

    main(args.file, args.output)
