# -*- coding: utf-8 -*-
#file: nlist.py
#author: 0bj3ct
#description: nlist.h头文件实现

from ctypes import *

class nlist(Structure):
    _fields_ = (
        ('n_un', c_uint),
        ('n_type', c_ubyte),
        ('n_sect', c_ubyte),
        ('n_desc', c_ushort),
        ('n_value', c_uint),
    )

class nlist_64(Structure):
    _fields_ = (
        ('n_un', c_uint),
        ('n_type', c_ubyte),
        ('n_sect', c_ubyte),
        ('n_desc', c_ushort),
        ('n_value', c_ulonglong),
    )

N_STAB = 0xe0
N_PEXT = 0x10
N_TYPE = 0x0e
N_EXT = 0x01

N_UNDF = 0x0
N_ABS = 0x2
N_SECT = 0xe
N_PBUD = 0xc
N_INDR = 0xa

NO_SECT = 0
MAX_SECT = 255

REFERENCE_TYPE = 0xf
REFERENCE_FLAG_UNDEFINED_NON_LAZY = 0
REFERENCE_FLAG_UNDEFINED_LAZY = 1
REFERENCE_FLAG_DEFINED = 2
REFERENCE_FLAG_PRIVATE_DEFINED = 3
REFERENCE_FLAG_PRIVATE_UNDEFINED_NON_LAZY = 4
REFERENCE_FLAG_PRIVATE_UNDEFINED_LAZY = 5

REFERENCED_DYNAMICALLY = 0x0010

def GET_LIBRARY_ORDINAL(n_desc):
    return (((n_desc) >> 8) & 0xff)

def SET_LIBRARY_ORDINAL(n_desc, ordinal):
    return (((n_desc) & 0x00ff) | (((ordinal & 0xff) << 8)))

SELF_LIBRARY_ORDINAL = 0x0
MAX_LIBRARY_ORDINAL = 0xfd
DYNAMIC_LOOKUP_ORDINAL = 0xfe
EXECUTABLE_ORDINAL = 0xff

N_DESC_DISCARDED = 0x0020
N_WEAK_REF = 0x0040
N_WEAK_DEF = 0x0080