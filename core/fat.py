# -*- coding: utf-8 -*-
#file: fat.py
#author: 0bj3ct
#description: fat.h头文件实现

from loader import cpu_type_t,cpu_subtype_t
from ctypes import *

FAT_MAGIC = 0xcafebabeL
FAT_CIGAM = 0xbebafecaL

class fat_header(Structure):
    _fields_ = (
        ('magic', c_uint),
        ('nfat_arch', c_uint),
    )

class fat_arch(Structure):
    _fields_ = (
        ('cputype', cpu_type_t),
        ('cpusubtype', cpu_subtype_t),
        ('offset', c_uint),
        ('size', c_uint),
        ('align', c_uint),
    )