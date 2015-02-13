# -*- coding: utf-8 -*-
#file: macho_header.py
#author: 0bj3ct
#description: macho文件格式头解析模块

import sys
import loader
import fat
import nlist

(
    FILE_FAT, FILE_MACHO64, FILE_MACHO
) = range(0x1, 0x3)

filetype = {
    FAT_MAGIC : FILE_FAT,
    FAT_CIGAM : FILE_FAT,
    MH_MAGIC  : FILE_MACHO,
    MH_CIGAM  : FILE_MACHO,
    MH_MAGIC_64:FILE_MACHO64,
    MH_CIGAM_64:FILE_MACHO64
}

class file_t(object):
    def __init__(self, filepath):
        super(file_t,self).__init__()
        self.filepath = filepath
        self.fp = open(self.filepath,'rb+')
        magic = self.fp.read(4)
        self.file_type = filetype[magic]
        self.macho_header = [];
        if self.filetype is FILE_FAT:
            nfat_arch = self.fp.read(4)
            for i in xrange (0,nfat_arch):
                self.fat_arch = self.fp.read(len(fat.fat_arch));
                offset = self.fat_arch.offset
                self.fp.seek(offset)
                self.macho_header.append(macho_header_t(fp))
        else:
            self.macho_header.append(macho_header_t(fp))
class macho_header_t(object):
    """docstring for macho_header_t"""
    def __init__(self, fp):
        super(macho_header_t, self).__init__()
        self.arg = arg
        '''macho_64'''
        if 1:
            pass
        '''macho'''
        '''else:
            pass'''