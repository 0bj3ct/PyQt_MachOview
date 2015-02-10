# -*- coding: utf-8 -*-
#file: macho_header.py
#author: 0bj3ct
#description: macho文件格式头解析模块

from ctypes import *

CPU_TYPE_NAMES = {
    -1:     'ANY',
    1:      'VAX',
    6:      'MC680x0',
    7:      'i386',
    8:      'MIPS',
    10:     'MC98000',
    11:     'HPPA',
    12:     'ARM',
    13:     'MC88000',
    14:     'SPARC',
    15:     'i860',
    16:     'Alpha',
    18:     'PowerPC',
}

_MH_EXECUTE_SYM = "__mh_execute_header"
MH_EXECUTE_SYM = "_mh_execute_header"
_MH_BUNDLE_SYM = "__mh_bundle_header"
MH_BUNDLE_SYM = "_mh_bundle_header"
_MH_DYLIB_SYM = "__mh_dylib_header"
MH_DYLIB_SYM = "_mh_dylib_header"
_MH_DYLINKER_SYM = "__mh_dylinker_header"
MH_DYLINKER_SYM = "_mh_dylinker_header"

(
    MH_OBJECT, MH_EXECUTE, MH_FVMLIB, MH_CORE, MH_PRELOAD, MH_DYLIB,
    MH_DYLINKER, MH_BUNDLE, MH_DYLIB_STUB, MH_DSYM
) = range(0x1, 0xb)

(
    MH_NOUNDEFS, MH_INCRLINK, MH_DYLDLINK, MH_BINDATLOAD, MH_PREBOUND,
    MH_SPLIT_SEGS, MH_LAZY_INIT, MH_TWOLEVEL, MH_FORCE_FLAT, MH_NOMULTIDEFS,
    MH_NOFIXPREBINDING
) = map((1).__lshift__, range(11))

MH_MAGIC = 0xfeedfaceL
MH_CIGAM = 0xcefaedfeL
MH_MAGIC_64 = 0xfeedfacfL
MH_CIGAM_64 = 0xcffaedfeL

integer_t = c_uint
cpu_type_t = integer_t
cpu_subtype_t = integer_t

MH_FILETYPE_NAMES = {
    MH_OBJECT:      'relocatable object',
    MH_EXECUTE:     'demand paged executable',
    MH_FVMLIB:      'fixed vm shared library',
    MH_CORE:        'core',
    MH_PRELOAD:     'preloaded executable',
    MH_DYLIB:       'dynamically bound shared library',
    MH_DYLINKER:    'dynamic link editor',
    MH_BUNDLE:      'dynamically bound bundle',
    MH_DYLIB_STUB:  'shared library stub for static linking',
    MH_DSYM:        'symbol information',
}

MH_FILETYPE_SHORTNAMES = {
    MH_OBJECT:      'object',
    MH_EXECUTE:     'execute',
    MH_FVMLIB:      'fvmlib',
    MH_CORE:        'core',
    MH_PRELOAD:     'preload',
    MH_DYLIB:       'dylib',
    MH_DYLINKER:    'dylinker',
    MH_BUNDLE:      'bundle',
    MH_DYLIB_STUB:  'dylib_stub',
    MH_DSYM:        'dsym',
}

MH_FLAGS_NAMES = {
    MH_NOUNDEFS:    'no undefined references',
    MH_INCRLINK:    'output of an incremental link',
    MH_DYLDLINK:    'input for the dynamic linker',
    MH_BINDATLOAD:  'undefined references bound dynamically when loaded',
    MH_PREBOUND:    'dynamic undefined references prebound',
    MH_SPLIT_SEGS:  'split read-only and read-write segments',
    MH_LAZY_INIT:   '(obsolete)',
    MH_TWOLEVEL:    'using two-level name space bindings',
    MH_FORCE_FLAT:  'forcing all imagges to use flat name space bindings',
    MH_NOMULTIDEFS: 'umbrella guarantees no multiple definitions',
    MH_NOFIXPREBINDING: 'do not notify prebinding agent about this executable',
}

'''
class mach_version_helper(Structure):
    _fields_ = (
        ('major', p_ushort),
        ('minor', p_ubyte),
        ('rev', p_ubyte),
    )
    def __str__(self):
        return '%s.%s.%s' % (self.major, self.minor, self.rev)

class mach_timestamp_helper(c_uint):
    def __str__(self):
        return time.ctime(self)

def read_struct(f, s, **kw):
    return s.from_fileobj(f, **kw)
'''

class mach_header(Structure):
    _fields_ = (
        ('magic', c_uint),
        ('cputype', cpu_type_t),
        ('cpusubtype', cpu_subtype_t),
        ('filetype', c_uint),
        ('ncmds', c_uint),
        ('sizeofcmds', c_uint),
        ('flags', c_uint),
    )
    def _describe(self):
        bit = 1L
        flags = self.flags
        dflags = []
        while flags and bit < (1<<32L):
            if flags & bit:
                dflags.append(MH_FLAGS_NAMES.get(bit, str(bit)))
                flags = flags ^ bit
            bit <<= 1L
        return (
            ('magic', '0x%08X' % self.magic),
            ('cputype', CPU_TYPE_NAMES.get(self.cputype, self.cputype)),
            ('cpusubtype', self.cpusubtype),
            ('filetype', MH_FILETYPE_NAMES.get(self.filetype, self.filetype)),
            ('ncmds', self.ncmds),
            ('sizeofcmds', self.sizeofcmds),
            ('flags', dflags),
        )

class mach_header_64(mach_header):
    _fields_ = mach_header._fields_ + (('reserved', c_uint),)

class load_command(Structure):
    _fields_ = (
        ('cmd', c_uint),
        ('cmdsize', c_uint),
    )

LC_REQ_DYLD = 0x80000000L

(
    LC_SEGMENT, LC_SYMTAB, LC_SYMSEG, LC_THREAD, LC_UNIXTHREAD, LC_LOADFVMLIB,
    LC_IDFVMLIB, LC_IDENT, LC_FVMFILE, LC_PREPAGE, LC_DYSYMTAB, LC_LOAD_DYLIB,
    LC_ID_DYLIB, LC_LOAD_DYLINKER, LC_ID_DYLINKER, LC_PREBOUND_DYLIB,
    LC_ROUTINES, LC_SUB_FRAMEWORK, LC_SUB_UMBRELLA, LC_SUB_CLIENT,
    LC_SUB_LIBRARY, LC_TWOLEVEL_HINTS, LC_PREBIND_CKSUM
) = range(0x1, 0x18)

LC_LOAD_WEAK_DYLIB = LC_REQ_DYLD | 0x18

LC_SEGMENT_64 = 0x19
LC_ROUTINES_64 = 0x1a
LC_UUID = 0x1b
LC_RPATH = (0x1c | LC_REQ_DYLD)
LC_CODE_SIGNATURE = 0x1d
LC_CODE_SEGMENT_SPLIT_INFO = 0x1e
LC_REEXPORT_DYLIB = 0x1f | LC_REQ_DYLD
LC_LAZY_LOAD_DYLIB = 0x20
LC_ENCRYPTION_INFO = 0x21
LC_DYLD_INFO = 0x22
LC_DYLD_INFO_ONLY = 0x22 | LC_REQ_DYLD
LC_LOAD_UPWARD_DYLIB = (0x23 | LC_REQ_DYLD)
LC_VERSION_MIN_MACOSX = 0x24
LC_VERSION_MIN_IPHONEOS = 0x25
LC_FUNCTION_STARTS = 0x26
LC_DYLD_ENVIRONMENT = 0x27
LC_MAIN = (0x28|LC_REQ_DYLD)
LC_DATA_IN_CODE = 0x29
LC_SOURCE_VERSION = 0x2A
LC_DYLIB_CODE_SIGN_DRS = 0x2B

# this is really a union.. but whatever
class lc_str(c_uint):
    pass

p_str16 = pypackable('p_str16', str, '16s')

vm_prot_t = c_uint
class segment_command(Structure):
    _fields_ = (
        ('segname', c_char*16),
        ('vmaddr', c_uint),
        ('vmsize', c_uint),
        ('fileoff', c_uint),
        ('filesize', c_uint),
        ('maxprot', vm_prot_t),
        ('initprot', vm_prot_t),
        ('nsects', c_uint), # read the section structures ?
        ('flags', c_uint),
    )

class segment_command_64(Structure):
    _fields_ = (
        ('segname', c_char*16),
        ('vmaddr', c_ulonglong),
        ('vmsize', c_ulonglong),
        ('fileoff', c_ulonglong),
        ('filesize', c_ulonglong),
        ('maxprot', vm_prot_t),
        ('initprot', vm_prot_t),
        ('nsects', c_uint), # read the section structures ?
        ('flags', c_uint),
    )

SG_HIGHVM = 0x1
SG_FVMLIB = 0x2
SG_NORELOC = 0x4

class section(Structure):
    _fields_ = (
        ('sectname', c_char*16),
        ('segname', c_char*16),
        ('addr', c_uint),
        ('size', c_uint),
        ('offset', c_uint),
        ('align', c_uint),
        ('reloff', c_uint),
        ('nreloc', c_uint),
        ('flags', c_uint),
        ('reserved1', c_uint),
        ('reserved2', c_uint),
    )

class section_64(Structure):
    _fields_ = (
        ('sectname', c_char*16),
        ('segname', c_char*16),
        ('addr', c_ulonglong),
        ('size', c_ulonglong),
        ('offset', c_uint),
        ('align', c_uint),
        ('reloff', c_uint),
        ('nreloc', c_uint),
        ('flags', c_uint),
        ('reserved1', c_uint),
        ('reserved2', c_uint),
        ('reserved3', c_uint),
    )

SECTION_TYPE = 0xffL
SECTION_ATTRIBUTES = 0xffffff00L
S_REGULAR = 0x0
S_ZEROFILL = 0x1
S_CSTRING_LITERALS = 0x2
S_4BYTE_LITERALS = 0x3
S_8BYTE_LITERALS = 0x4
S_LITERAL_POINTERS = 0x5
S_NON_LAZY_SYMBOL_POINTERS = 0x6
S_LAZY_SYMBOL_POINTERS = 0x7
S_SYMBOL_STUBS = 0x8
S_MOD_INIT_FUNC_POINTERS = 0x9
S_MOD_TERM_FUNC_POINTERS = 0xa
S_COALESCED = 0xb

SECTION_ATTRIBUTES_USR = 0xff000000L
S_ATTR_PURE_INSTRUCTIONS = 0x80000000L
S_ATTR_NO_TOC = 0x40000000L
S_ATTR_STRIP_STATIC_SYMS = 0x20000000L
SECTION_ATTRIBUTES_SYS = 0x00ffff00L
S_ATTR_SOME_INSTRUCTIONS = 0x00000400L
S_ATTR_EXT_RELOC = 0x00000200L
S_ATTR_LOC_RELOC = 0x00000100L


SEG_PAGEZERO =    "__PAGEZERO"
SEG_TEXT =    "__TEXT"
SECT_TEXT =   "__text"
SECT_FVMLIB_INIT0 = "__fvmlib_init0"
SECT_FVMLIB_INIT1 = "__fvmlib_init1"
SEG_DATA =    "__DATA"
SECT_DATA =   "__data"
SECT_BSS =    "__bss"
SECT_COMMON = "__common"
SEG_OBJC =    "__OBJC"
SECT_OBJC_SYMBOLS = "__symbol_table"
SECT_OBJC_MODULES = "__module_info"
SECT_OBJC_STRINGS = "__selector_strs"
SECT_OBJC_REFS = "__selector_refs"
SEG_ICON =     "__ICON"
SECT_ICON_HEADER = "__header"
SECT_ICON_TIFF =   "__tiff"
SEG_LINKEDIT =    "__LINKEDIT"
SEG_UNIXSTACK =   "__UNIXSTACK"

#
#  I really should remove all these _command classes because they
#  are no different.  I decided to keep the load commands separate,
#  so classes like fvmlib and fvmlib_command are equivalent.
#

class fvmlib(Structure):
    _fields_ = (
        ('name', lc_str),
        ('minor_version', mach_version_helper),
        ('header_addr', c_uint),
    )

class fvmlib_command(Structure):
    _fields_ = fvmlib._fields_

class dylib(Structure):
    _fields_ = (
        ('name', lc_str),
        ('timestamp', mach_timestamp_helper),
        ('current_version', mach_version_helper),
        ('compatibility_version', mach_version_helper),
    )

# merged dylib structure
class dylib_command(Structure):
    _fields_ = dylib._fields_

class sub_framework_command(Structure):
    _fields_ = (
        ('umbrella', lc_str),
    )

class sub_client_command(Structure):
    _fields_ = (
        ('client', lc_str),
    )

class sub_umbrella_command(Structure):
    _fields_ = (
        ('sub_umbrella', lc_str),
    )

class sub_library_command(Structure):
    _fields_ = (
        ('sub_library', lc_str),
    )

class prebound_dylib_command(Structure):
    _fields_ = (
        ('name', lc_str),
        ('nmodules', c_uint),
        ('linked_modules', c_uint),
    )

class dylinker_command(Structure):
    _fields_ = (
        ('name', lc_str),
    )

class thread_command(Structure):
    _fields_ = (
    )

class routines_command(Structure):
    _fields_ = (
        ('init_address', c_uint),
        ('init_module', c_uint),
        ('reserved1', c_uint),
        ('reserved2', c_uint),
        ('reserved3', c_uint),
        ('reserved4', c_uint),
        ('reserved5', c_uint),
        ('reserved6', c_uint),
    )

class routines_command_64(Structure):
    _fields_ = (
        ('init_address', c_ulonglong),
        ('init_module', c_ulonglong),
        ('reserved1', c_ulonglong),
        ('reserved2', c_ulonglong),
        ('reserved3', c_ulonglong),
        ('reserved4', c_ulonglong),
        ('reserved5', c_ulonglong),
        ('reserved6', c_ulonglong),
    )

class symtab_command(Structure):
    _fields_ = (
        ('symoff', c_uint),
        ('nsyms', c_uint),
        ('stroff', c_uint),
        ('strsize', c_uint),
    )

class dysymtab_command(Structure):
    _fields_ = (
        ('ilocalsym', c_uint),
        ('nlocalsym', c_uint),
        ('iextdefsym', c_uint),
        ('nextdefsym', c_uint),
        ('iundefsym', c_uint),
        ('nundefsym', c_uint),
        ('tocoff', c_uint),
        ('ntoc', c_uint),
        ('modtaboff', c_uint),
        ('nmodtab', c_uint),
        ('extrefsymoff', c_uint),
        ('nextrefsyms', c_uint),
        ('indirectsymoff', c_uint),
        ('nindirectsyms', c_uint),
        ('extreloff', c_uint),
        ('nextrel', c_uint),
        ('locreloff', c_uint),
        ('nlocrel', c_uint),
    )

INDIRECT_SYMBOL_LOCAL = 0x80000000L
INDIRECT_SYMBOL_ABS = 0x40000000L

class dylib_table_of_contents(Structure):
    _fields_ = (
        ('symbol_index', c_uint),
        ('module_index', c_uint),
    )

class dylib_module(Structure):
    _fields_ = (
        ('module_name', c_uint),
        ('iextdefsym', c_uint),
        ('nextdefsym', c_uint),
        ('irefsym', c_uint),
        ('nrefsym', c_uint),
        ('ilocalsym', c_uint),
        ('nlocalsym', c_uint),
        ('iextrel', c_uint),
        ('nextrel', c_uint),
        ('iinit_iterm', c_uint),
        ('ninit_nterm', c_uint),
        ('objc_module_info_addr', c_uint),
        ('objc_module_info_size', c_uint),
    )

class dylib_module_64(Structure):
    _fields_ = (
        ('module_name', c_uint),
        ('iextdefsym', c_uint),
        ('nextdefsym', c_uint),
        ('irefsym', c_uint),
        ('nrefsym', c_uint),
        ('ilocalsym', c_uint),
        ('nlocalsym', c_uint),
        ('iextrel', c_uint),
        ('nextrel', c_uint),
        ('iinit_iterm', c_uint),
        ('ninit_nterm', c_uint),
        ('objc_module_info_size', c_uint),
        ('objc_module_info_addr', c_ulonglong),
    )

class dylib_reference(Structure):
    _fields_ = (
        # XXX - ick, fix
        ('isym_flags', c_uint),
        #('isym', p_ubyte * 3),
        #('flags', p_ubyte),
    )

class twolevel_hints_command(Structure):
    _fields_ = (
        ('offset', c_uint),
        ('nhints', c_uint),
    )

class twolevel_hint(Structure):
    _fields_ = (
      # XXX - ick, fix
      ('isub_image_itoc', c_uint),
      #('isub_image', p_ubyte),
      #('itoc', p_ubyte * 3),
  )

class prebind_cksum_command(Structure):
    _fields_ = (
        ('cksum', c_uint),
    )

class symseg_command(Structure):
    _fields_ = (
        ('offset', c_uint),
        ('size', c_uint),
    )

class ident_command(Structure):
    _fields_ = (
    )

class fvmfile_command(Structure):
    _fields_ = (
        ('name', lc_str),
        ('header_addr', c_uint),
    )

class uuid_command (Structure):
    _fields_ = (
        ('uuid', p_str16),
    )

class rpath_command (Structure):
    _fields_ = (
        ('path', lc_str),
    )

class linkedit_data_command (Structure):
    _fields_ = (
        ('dataoff',   c_uint),
        ('datassize', c_uint),
    )
class version_min_command(Structure):
    _fields_ = (
        ('version', c_uint),
        ('sdk', c_uint),
    )

class entry_point_command(Structure):
    _fields_ = (
        ('entryoff', c_ulonglong),
        ('stacksize', c_ulonglong),
    )       

class source_version_command(Structure):
    _fields_ = (
        ('version', c_ulonglong),
    )
                
LC_REGISTRY = {
    LC_SEGMENT:         segment_command,
    LC_IDFVMLIB:        fvmlib_command,
    LC_LOADFVMLIB:      fvmlib_command,
    LC_ID_DYLIB:        dylib_command,
    LC_LOAD_DYLIB:      dylib_command,
    LC_LOAD_WEAK_DYLIB: dylib_command,
    LC_SUB_FRAMEWORK:   sub_framework_command,
    LC_SUB_CLIENT:      sub_client_command,
    LC_SUB_UMBRELLA:    sub_umbrella_command,
    LC_SUB_LIBRARY:     sub_library_command,
    LC_PREBOUND_DYLIB:  prebound_dylib_command,
    LC_ID_DYLINKER:     dylinker_command,
    LC_LOAD_DYLINKER:   dylinker_command,
    LC_THREAD:          thread_command,
    LC_UNIXTHREAD:      thread_command,
    LC_ROUTINES:        routines_command,
    LC_SYMTAB:          symtab_command,
    LC_DYSYMTAB:        dysymtab_command,
    LC_TWOLEVEL_HINTS:  twolevel_hints_command,
    LC_PREBIND_CKSUM:   prebind_cksum_command,
    LC_SYMSEG:          symseg_command,
    LC_IDENT:           ident_command,
    LC_FVMFILE:         fvmfile_command,
    LC_SEGMENT_64:      segment_command_64,
    LC_ROUTINES_64:     routines_command_64,
    LC_UUID:            uuid_command,
    LC_RPATH:           rpath_command,
    LC_CODE_SIGNATURE:  linkedit_data_command,
    LC_CODE_SEGMENT_SPLIT_INFO:  linkedit_data_command,
    LC_REEXPORT_DYLIB:  dylib_command,
    LC_LAZY_LOAD_DYLIB: dylib_command,
    LC_ENCRYPTION_INFO: dylib_command,
    LC_DYLD_INFO:       dylib_command,
    LC_DYLD_INFO_ONLY:  dylib_command,
    LC_LOAD_UPWARD_DYLIB:  dylib_command,
    LC_VERSION_MIN_MACOSX: version_min_command,
    LC_VERSION_MIN_IPHONEOS: version_min_command,
    LC_FUNCTION_STARTS: linkedit_data_command,
    LC_DYLD_ENVIRONMENT:dylinker_command,
    LC_MAIN:            entry_point_command,
    LC_DATA_IN_CODE:    linkedit_data_command,
    LC_SOURCE_VERSION:  source_version_command,
    LC_DYLIB_CODE_SIGN_DRS:linkedit_data_command,
}

LC_NAME = {
    LC_SEGMENT:         'LC_SEGMENT',
    LC_IDFVMLIB:        'LC_IDFVMLIB',
    LC_LOADFVMLIB:      'LC_LOADFVMLIB',
    LC_ID_DYLIB:        'LC_ID_DYLIB',
    LC_LOAD_DYLIB:      'LC_LOAD_DYLIB',
    LC_LOAD_WEAK_DYLIB: 'LC_LOAD_WEAK_DYLIB',
    LC_SUB_FRAMEWORK:   'LC_SUB_FRAMEWORK',
    LC_SUB_CLIENT:      'LC_SUB_CLIENT',
    LC_SUB_UMBRELLA:    'LC_SUB_UMBRELLA',
    LC_SUB_LIBRARY:     'LC_SUB_LIBRARY',
    LC_PREBOUND_DYLIB:  'LC_PREBOUND_DYLIB',
    LC_ID_DYLINKER:     'LC_ID_DYLINKER',
    LC_LOAD_DYLINKER:   'LC_LOAD_DYLINKER',
    LC_THREAD:          'LC_THREAD',
    LC_UNIXTHREAD:      'LC_UNIXTHREAD',
    LC_ROUTINES:        'LC_ROUTINES',
    LC_SYMTAB:          'LC_SYMTAB',
    LC_DYSYMTAB:        'LC_DYSYMTAB',
    LC_TWOLEVEL_HINTS:  'LC_TWOLEVEL_HINTS',
    LC_PREBIND_CKSUM:   'LC_PREBIND_CKSUM',
    LC_SYMSEG:          'LC_SYMSEG',
    LC_IDENT:           'LC_IDENT',
    LC_FVMFILE:         'LC_FVMFILE',
    LC_SEGMENT_64:      'LC_SEGMENT_64',
    LC_ROUTINES_64:     'LC_ROUTINES_64',
    LC_UUID:            'LC_UUID',
    LC_RPATH:           'LC_RPATH',
    LC_CODE_SIGNATURE:  'LC_CODE_SIGNATURE',
    LC_CODE_SEGMENT_SPLIT_INFO:  'LC_CODE_SEGMENT_SPLIT_INFO',
    LC_REEXPORT_DYLIB:  'LC_REEXPORT_DYLIB',
    LC_LAZY_LOAD_DYLIB: 'LC_LAZY_LOAD_DYLIB',
    LC_ENCRYPTION_INFO: 'LC_ENCRYPTION_INFO',
    LC_DYLD_INFO:       'LC_DYLD_INFO',
    LC_DYLD_INFO_ONLY:  'LC_DYLD_INFO_ONLY',
    LC_LOAD_UPWARD_DYLIB:  'LC_LOAD_UPWARD_DYLIB',
    LC_VERSION_MIN_MACOSX: 'LC_VERSION_MIN_MACOSX',
    LC_VERSION_MIN_IPHONEOS: 'LC_VERSION_MIN_IPHONEOS',
    LC_FUNCTION_STARTS: 'LC_FUNCTION_STARTS',
    LC_DYLD_ENVIRONMENT:'LC_DYLD_ENVIRONMENT',
    LC_MAIN:            'LC_MAIN',
    LC_DATA_IN_CODE:    'LC_DATA_IN_CODE',
    LC_SOURCE_VERSION:  'LC_SOURCE_VERSION',
    LC_DYLIB_CODE_SIGN_DRS:'LC_DYLIB_CODE_SIGN_DRS',
}