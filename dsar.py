#!/usr/bin/env python3
import argparse
import struct
import io

"""
sDsarHeader:
    char Magic[4]
    uint32 Version
    uint32 numEntries
    uint32 entriesSize
    uint32 unk4
    uint32 unk5
    char[8] padding
"""
sDsarHeader = struct.Struct("<4s I I I I I 8x")

"""
sDsarEntry:
    uint64 offset (Maybe?)
    uint64 size (Compressed or uncompressed?)
    uint32 unk4 (Whatever this is it is, it affects the next entry's offset by adding)
    uint32 unk5
    uint32 unk6
    uint32 unk7 (Timestamp?)
    uint32 unk8 (Timestamp?)
"""
sDsarEntry = struct.Struct("<Q Q I I I I")
class DSAR:
    def __init__(self, handle):
        magic, version, numEntries, entriesSize, unk4, unk5 \
         = sDsarHeader.unpack(handle.read(sDsarHeader.size))
     
        if magic != b"DSAR":
            raise ValueError("Not a valid DSAR file!")
        
        if version & 0x7fffffff != 0x10003:
            raise ValueError("Unknown DSAR version!")
        
        for i in range(numEntries):
            print(sDsarEntry.unpack(handle.read(sDsarEntry.size)))
    
    @classmethod
    def fromFile(cls, handle):
        return cls(handle)
    
    @classmethod
    def fromByte(cls, data):
        return cls(io.BytesIO(data))

if __name__ == "__main__":
    def listDsar(args):
        with open(args.file, "rb") as f:
            DSAR.fromFile(f)
            
    
    parser = argparse.ArgumentParser(description="Extract/Repack DSAR files")
    subparsers = parser.add_subparsers(help='sub-command help', required=True)
    
    #List
    optList = subparsers.add_parser('l', help='list')
    optList.add_argument("file", help='DSAR file')
    optList.set_defaults(func=listDsar)
    
    #Extract
    
    
    args = parser.parse_args()
    args.func(args)
    
    #print(args.accumulate(args.integers))
