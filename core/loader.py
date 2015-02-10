# -*- coding: utf-8 -*-
#file: macho_header.py
#author: 0bj3ct
#description: macho文件格式头解析模块

from ctypes import *

'''
struct mach_header {
	uint32_t	magic;		/* mach magic number identifier */
	cpu_type_t	cputype;	/* cpu specifier */
	cpu_subtype_t	cpusubtype;	/* machine specifier */
	uint32_t	filetype;	/* type of file */
	uint32_t	ncmds;		/* number of load commands */
	uint32_t	sizeofcmds;	/* the size of all the load commands */
	uint32_t	flags;		/* flags */
};
'''

class mach_header(Structure):
	_fields_ = [
        ("magic", c_uint),
        ("cputype", c_uint),
        ("cpusubtype", c_uint),
        ("filetype", c_uint),
        ("ncmds", c_uint),
        ("sizeofcmds", c_uint),
        ("flags", c_uint)];
MH_MAGIC = 0xfeedface
MH_CIGAM = 0xcefaedfe

class mach_header_64(Structure):
	_fields_ = [
        ("magic", c_uint),
        ("cputype", c_uint),
        ("cpusubtype", c_uint),
        ("filetype", c_uint),
        ("ncmds", c_uint),
        ("sizeofcmds", c_uint),
        ("flags", c_uint),
        ("reserved", c_uint)];

MH_MAGIC_64 = 0xfeedfacf
MH_CIGAM_64 = 0xcffaedfe

'''
/* Constant for the magic field of the mach_header (32-bit architectures) */
#define	MH_MAGIC	0xfeedface	/* the mach magic number */
#define MH_CIGAM	0xcefaedfe	/* NXSwapInt(MH_MAGIC) */

/*
 * The 64-bit mach header appears at the very beginning of object files for
 * 64-bit architectures.
 */
struct mach_header_64 {
	uint32_t	magic;		/* mach magic number identifier */
	cpu_type_t	cputype;	/* cpu specifier */
	cpu_subtype_t	cpusubtype;	/* machine specifier */
	uint32_t	filetype;	/* type of file */
	uint32_t	ncmds;		/* number of load commands */
	uint32_t	sizeofcmds;	/* the size of all the load commands */
	uint32_t	flags;		/* flags */
	uint32_t	reserved;	/* reserved */
};

/* Constant for the magic field of the mach_header_64 (64-bit architectures) */
#define MH_MAGIC_64 0xfeedfacf /* the 64-bit mach magic number */
#define MH_CIGAM_64 0xcffaedfe /* NXSwapInt(MH_MAGIC_64) */
'''

class load_command(Structure):
	_fields_ = [
        ("cmd", c_uint),
        ("cmdsize", c_uint)];

'''
struct load_command {
	uint32_t cmd;		/* type of load command */
	uint32_t cmdsize;	/* total size of command in bytes */
};
'''

class segment_command(Structure):
	_fields_ = [
        ("cmd", c_uint),
        ("cmdsize", c_uint),
        ("segname", c_char*16),
        ("vmaddr", c_uint),
        ("vmsize", c_uint),
        ("fileoff", c_uint),
        ("filesize", c_uint),
        ("maxprot", c_uint),
        ("initprot", c_uint),
        ("nsects", c_uint),
        ("flags", c_uint)];

class segment_command_64(Structure):
	_fields_ = [
        ("cmd", c_uint),
        ("cmdsize", c_uint),
        ("segname", c_char*16),
        ("vmaddr", c_ulonglong),
        ("vmsize", c_ulonglong),
        ("fileoff", c_ulonglong),
        ("filesize", c_ulonglong),
        ("maxprot", c_uint),
        ("initprot", c_uint),
        ("nsects", c_uint),
        ("flags", c_uint)];

'''
struct segment_command { /* for 32-bit architectures */
	uint32_t	cmd;		/* LC_SEGMENT */
	uint32_t	cmdsize;	/* includes sizeof section structs */
	char		segname[16];	/* segment name */
	uint32_t	vmaddr;		/* memory address of this segment */
	uint32_t	vmsize;		/* memory size of this segment */
	uint32_t	fileoff;	/* file offset of this segment */
	uint32_t	filesize;	/* amount to map from the file */
	vm_prot_t	maxprot;	/* maximum VM protection */
	vm_prot_t	initprot;	/* initial VM protection */
	uint32_t	nsects;		/* number of sections in segment */
	uint32_t	flags;		/* flags */
};

/*
 * The 64-bit segment load command indicates that a part of this file is to be
 * mapped into a 64-bit task's address space.  If the 64-bit segment has
 * sections then section_64 structures directly follow the 64-bit segment
 * command and their size is reflected in cmdsize.
 */
struct segment_command_64 { /* for 64-bit architectures */
	uint32_t	cmd;		/* LC_SEGMENT_64 */
	uint32_t	cmdsize;	/* includes sizeof section_64 structs */
	char		segname[16];	/* segment name */
	uint64_t	vmaddr;		/* memory address of this segment */
	uint64_t	vmsize;		/* memory size of this segment */
	uint64_t	fileoff;	/* file offset of this segment */
	uint64_t	filesize;	/* amount to map from the file */
	vm_prot_t	maxprot;	/* maximum VM protection */
	vm_prot_t	initprot;	/* initial VM protection */
	uint32_t	nsects;		/* number of sections in segment */
	uint32_t	flags;		/* flags */
};
'''

class section(Structure):
	_fields_ = [
        ("sectname", c_char*16),
        ("segname", c_char*16),
        ("addr", c_uint),
        ("size", c_uint),
        ("offset", c_uint),
        ("align", c_uint),
        ("reloff", c_uint),
        ("nreloc", c_uint),
        ("flags", c_uint),
        ("reserved1", c_uint),
        ("reserved2", c_uint)];

class section_64(Structure):
	_fields_ = [
        ("sectname", c_char*16),
        ("segname", c_char*16),
        ("addr", c_ulonglong),
        ("size", c_ulonglong),
        ("offset", c_uint),
        ("align", c_uint),
        ("reloff", c_uint),
        ("nreloc", c_uint),
        ("flags", c_uint),
        ("reserved1", c_uint),
        ("reserved2", c_uint),
        ("reserved3", c_uint)];

'''
struct section { /* for 32-bit architectures */
	char		sectname[16];	/* name of this section */
	char		segname[16];	/* segment this section goes in */
	uint32_t	addr;		/* memory address of this section */
	uint32_t	size;		/* size in bytes of this section */
	uint32_t	offset;		/* file offset of this section */
	uint32_t	align;		/* section alignment (power of 2) */
	uint32_t	reloff;		/* file offset of relocation entries */
	uint32_t	nreloc;		/* number of relocation entries */
	uint32_t	flags;		/* flags (section type and attributes)*/
	uint32_t	reserved1;	/* reserved (for offset or index) */
	uint32_t	reserved2;	/* reserved (for count or sizeof) */
};

struct section_64 { /* for 64-bit architectures */
	char		sectname[16];	/* name of this section */
	char		segname[16];	/* segment this section goes in */
	uint64_t	addr;		/* memory address of this section */
	uint64_t	size;		/* size in bytes of this section */
	uint32_t	offset;		/* file offset of this section */
	uint32_t	align;		/* section alignment (power of 2) */
	uint32_t	reloff;		/* file offset of relocation entries */
	uint32_t	nreloc;		/* number of relocation entries */
	uint32_t	flags;		/* flags (section type and attributes)*/
	uint32_t	reserved1;	/* reserved (for offset or index) */
	uint32_t	reserved2;	/* reserved (for count or sizeof) */
	uint32_t	reserved3;	/* reserved */
};
'''

class routines_command(Structure):
	_fields_ = [
        ("cmd", c_uint),
        ("cmdsize", c_uint),
        ("init_address", c_uint),
        ("init_module", c_uint),
        ("reserved1", c_uint),
        ("reserved2", c_uint),
        ("reserved3", c_uint),
        ("reserved4", c_uint),
        ("reserved5", c_uint),
        ("reserved6", c_uint)];

class routines_command(Structure):
	_fields_ = [
        ("cmd", c_uint),
        ("cmdsize", c_uint),
        ("init_address", c_ulonglong),
        ("init_module", c_ulonglong),
        ("reserved1", c_ulonglong),
        ("reserved2", c_ulonglong),
        ("reserved3", c_ulonglong),
        ("reserved4", c_ulonglong),
        ("reserved5", c_ulonglong),
        ("reserved6", c_ulonglong)];

