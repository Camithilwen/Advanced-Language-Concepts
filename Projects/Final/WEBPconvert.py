import re
from PIL import Image
import numpy as np
from webptools import *
from PNGwrite import *
class WEBPconvert:
    '''Contains methods necessary to parse a WEBP file for important header data,
    decompress raw pixel data, and, currently, re-write to a PNG.'''
    def __init__(self):
        self.inData = None
        self.path = None
        self.png = PNGwrite()
        
   
    def fileOpen(self, path):
        """Open a binary file
        Returns: 
            - "OK" on success or exception data on reciept."""
        try:
            with open(path, 'rb') as inFile:
                self.inData = inFile.read()
                self.path = path
            return "OK"
        except FileNotFoundError as ex:
            status = str(ex)
            return status
        except Exception as ex:
            status = str(ex)
            return status
    
    def fileConvert(self):
        """Calls to parse file header,
        uses Pillow to decompress WEBP image data to a numpy array,
        constructs a PNG file header and uses zlib to recompress data,
        writes result to a new byte string.
        """
        fileHeader = self.headerParse()
        '''Opens the image file and parses for alpha information. Nonstandard color spaces are
        converted to RGBA.'''
        with Image.open(self.path) as img:
            if img.mode != 'RGBA' and fileHeader.get("alpha", False):
                img = img.convert('RGBA')
            elif img.mode == 'P':
                img = img.convert('RGBA')
            imageData = np.array(img)
        print("imageData:", imageData)
        self.png.header(fileHeader)
        self.png.data(imageData)
        self.png.end()
        '''I ran out of time to learn how to implement the decoding process for WEBP
        on my own (VP8 involves Huffman trees and Discrete Cosine Transformations) so I 
        am using Pillow and numpy to extract the raw pixel data to a numpy array.'''
        
    def isWEBP(self, header):
        """Checks a provided file header for RIFF and WEBP
        format declaration.
        Returns:
            - true or false."""
        webpHeader = re.compile(b'RIFF....WEBP')
        return webpHeader.match(header)
    
    def fileType(self, header):
        """Checks a provided WEBP file header to determine and return the file's subtype.
        Returns:
            - File subtype of VP8X (extended), VP8L (lossless), or VP8 (lossy)."""
        if re.search(b'^RIFF....WEBPVP8X', header):
            return "VP8X" #extended file type - may contain additional data chunks.
        elif re.search(b'^RIFF....WEBPVP8L', header):
            return "VP8L" #simple lossless
        elif re.search(b'^RIFF....WEBPVP8', header):
            return "VP8" #simple lossy         
        else:
            raise UserWarning("Unknown WEBP subtype.") 
        
    def headerParse(self, header=None):
        """Parses a provided WEBP file header by file subtype
        and returns values as a dictionary.
        Returns:
            - Dictionary containing header data specific to each file subtype."""
        header = header or self.inData
        if self.isWEBP(header):

            if self.fileType(header) == "VP8":
                return self.parseVP8(header)

            elif self.fileType(header) == "VP8L":
               return self.parseVP8L(header)

            elif self.fileType(header) == "VP8X":
                return self.parseVP8X(header)
               
        raise UserWarning("Not a valid WEBP file.")

    def parseVP8(self, header=None):
        '''Parses simple lossy encoding for width and height information.'''
        header = header or self.inData
        vp8Match = re.search(b'VP8 (.{10})(.{2})(.{2})', header, re.DOTALL)
        if vp8Match:
            widthBytes = vp8Match.group(2)
            heightBytes = vp8Match.group(3)
            width = int.from_bytes(widthBytes, byteorder='little')
            height = int.from_bytes(heightBytes, byteorder='little') 

            return {
                "width": width,
                "height": height,
                "alpha": False #simple VP8 does not support an alpha channel.
            }
        raise UserWarning("Invalid VP8 subtype.")
    
    def parseVP8L(self, header=None):
        '''Parses simple lossless encoding for width, height, and color space information.'''
        header = header or self.inData
        vp8lMatch = re.search(b'VP8L(.{5})', header, re.DOTALL)
        if vp8lMatch:
            widthBytes = int.from_bytes(header[21:23], byteorder='little')
            heightBytes = int.from_bytes(header[23:25], byteorder='little') 
            lastTwoDigits = (widthBytes & 0xC000) >> 14
            '''VP8L width and height information are encoded as 14-bit values
            across byte pairs. Unused bits are masked out.
            The total values are stored as <value> -1, so 1 is added at the end'''
            width = (widthBytes & 0x3FFF) + 1 
            height = ((heightBytes & 0xFFF) << 2 | lastTwoDigits) + 1
            alphaBit = bool(vp8lMatch.group(1)[4] & 0x10)
            return {
                "width": width,
                "height": height,
                "alpha": alphaBit
            }
        raise UserWarning("Invalid VP8L subtype.")

    def parseVP8X(self, header=None):
        '''Parses the extended file format for width, height, color space, bitstream encoding, animation presence, and metadata'''
        header = header or self.inData
        vp8xMatch = re.search(b'VP8X(.{7})(.{3})(.{3})', header, re.DOTALL)
        if vp8xMatch:
            #Determine file contents from header bit flags
            flagByte = vp8xMatch.group(1)[0]

            #Check for alpha channel
            alphaBit = bool(flagByte & 0b00010000)

            #Check for ICCP chunk
            ICCPbit = bool(flagByte & 0b00100000)
            colorSpace = "Other (non-sRGB)" if ICCPbit else "sRGB"

            #Check for EXIF and XMP metadata
            EXIFbit = bool(flagByte & 0b00001000)
            XMPbit = bool(flagByte & 0b00000100)

            #Check for animation chunks
            animBit = bool(flagByte & 0b00000010) 
            
            #Determine bitstream compression type
            compressionMatch = re.search(b'VP8X.*(VP8 )', header, re.DOTALL)\
                                or re.search(b'VP8X.*(VP8L)', header, re.DOTALL)
            if compressionMatch.group(1) == b'VP8 ':
                compressionType = "VP8"
            elif compressionMatch.group(1) == b'VP8L':
                compressionType = "VP8L"
            else:
                raise UserWarning("Unknown bitstream compression type.")

            #Determine image width.
            '''1 is added because VP8X width and height information are encoded
            as 24 bit integers with a value of 1 less than true size.
            leading 0 values are stripped from the match result to ensure
            the correct decimalized integer value, but all-0 values are allowed to pass.'''
            widthBytes = vp8xMatch.group(2).lstrip(b'\x00') or b'\x00'
            width = int.from_bytes(widthBytes, byteorder='little') + 1

            #Determine image height.
            heightBytes = vp8xMatch.group(3).lstrip(b'\x00') or b'\x00'
            height = int.from_bytes(heightBytes, byteorder='little') + 1


            #Retrieve EXIF metadata
            '''Chunk size in RIFF containers (such as used by WEBP) is indicated in the
            first four bytes following the four character chunk identifier code.'''
            if EXIFbit:
                EXIFstart = re.search(b'VP8X.*(EXIF)(.{4})', header, re.DOTALL)
                if EXIFstart:
                    EXIFsize = int.from_bytes(EXIFstart.group(2), byteorder='little')
                    EXIFpattern = f'VP8X.*EXIF.{{4}}(.{{{EXIFsize}}})'.encode()
                    EXIFdata = re.search(EXIFpattern, header, re.DOTALL).group(1)
                else: EXIFdata = None
            else:
                EXIFdata = None

            if XMPbit:
                XMPstart = re.search(b'VP8X.*(XMP)(.{4})', header, re.DOTALL)
                if XMPstart:
                    XMPsize = int.from_bytes(XMPstart.group(2), byteorder='little')
                    XMPpattern = f'VP8X.*XMP.{{4}}(.{{{XMPsize}}})'.encode()
                    XMPdata = re.search(XMPpattern, header, re.DOTALL).group(1)
                else:
                    XMPdata = None
            else:
                XMPdata = None
            return {
                "width": width,
                "height": height,
                "alpha": alphaBit,
                "ICC Profile": colorSpace,
                "animated": animBit,
                "compression type": compressionType,
                "EXIF metadata": EXIFdata,
                "XMP metadata": XMPdata
            }
        raise UserWarning("Invalid VP8X subtype.")

    def fileSave(self, path):
        self.png.write(path)