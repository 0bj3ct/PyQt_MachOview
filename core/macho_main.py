# -*- coding: utf-8 -*-
#file: macho_main.py
#author: 0bj3ct
#description: macho解析的主模块

import sys
import macho_header

def main():
    file_macho = macho_header.file_t("/Volumes/2/work/projects/kiwisec_func_check/kiwisec_func_check/test/iOS_test")
    print file_macho.file_type
if __name__ == '__main__':
    main()