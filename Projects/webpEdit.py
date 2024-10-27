import re
class webpEdit:
    def __init__(self):
        self.inData = None
        
   
    def fileOpen(self, path):
        """Open a binary file
        Returns "OK" on success 
        or exception data on reciept."""
        try:
            with open(path, 'rb') as inFile:
                self.inData = inFile.read()
            return "OK"
        except FileNotFoundError as ex:
            status = str(ex)
            return status
        except Exception as ex:
            status = str(ex)
            return status
    
    def fileConvert(self):
        """Checks for WEBP file formatting using a regex.
        Creates a new binary file with PNG header information and repopulates
        the RGBA data from the WEBP file in PNG format. Compression algorithm used as required?"""
        print(self.headerParse())
    def isWEBP(self, header):
        """Checks a provided file header for RIFF and WEBP
        format declaration and returns a true or false value."""
        webpHeader = re.compile(b'RIFF....WEBP')
        return webpHeader.match(header)
    def fileType(self, header):
        """Checks a provided WEBP file header to determine and return the file's subtype."""
        if re.search(b'^RIFF....WEBPVP8X', header):
            return "VP8X" #extended file type - may contain additional data chunks.
        elif re.search(b'^RIFF....WEBPVP8L', header):
            return "VP8L" #simple lossless
        elif re.search(b'^RIFF....WEBPVP8', header):
            return "VP8" #simple lossy         
        else:
            raise UserWarning("Unknown WEBP compression type.") 
    def headerParse(self, header=None):
        """Parses a provided WEBP file header by file subtype for file size and color space information
        and returns values as a dictionary."""
        header = header or self.inData
        if self.isWEBP(header):

            if self.fileType(header) == "VP8":
                vp8Match = re.search(b'VP8 (.{10})(.{2})(.{2})', header, re.DOTALL)
                if vp8Match:
                    widthBytes = vp8Match.group(2)
                    heightBytes = vp8Match.group(3)
                    width = int.from_bytes(widthBytes, byteorder='little')
                    height = int.from_bytes(heightBytes, byteorder='little') 

                    return {
                        "width": width,
                        "height": height,
                        "color space": "RGB" #simple VP8 does not support an alpha channel.
                    }
                return None
            elif self.fileType(header) == "VP8L":
                vp8lMatch = re.search(b'VP8L(.{5})', header, re.DOTALL)
                if vp8lMatch:
                    widthBytes = int.from_bytes(header[21:23], byteorder='little')
                    heightBytes = int.from_bytes(header[23:25], byteorder='little') 
                    lastTwoDigits = (widthBytes & 0xC000) >> 14
                    #VP8L width and height information are encoded as 14-bit values
                    # across byte pairs. Unused bits are masked out.
                    # The total values are stored as <value> -1, so 1 is added at the end.
                    width = (widthBytes & 0x3FFF) + 1 
                    height = ((heightBytes & 0xFFF) << 2 | lastTwoDigits) + 1
                    alphaBit = bool(vp8lMatch.group(1)[4] & 0x10)
                    colorSpace = "RGBA" if alphaBit else "RGB"
                    return {
                        "width": width,
                        "height": height,
                        "color space": colorSpace
                    }
            elif self.fileType(header) == "VP8X":
                vp8xMatch = re.search(b'VP8X(.{7})(.{3})(.{3})', header, re.DOTALL)
                print(vp8xMatch)
                if vp8xMatch:
                    #Determine color space RGB vs RGBA.
                    flagByte = vp8xMatch.group(1)[0]
                    alphaBit = bool(flagByte & 0b00010000)
                    colorSpace = "RGBA" if alphaBit else "RGB"

                    #Determine image width.
                    # 1 is added because VP8X width and height information are encoded
                    # as 24 bit integers with a value of 1 less than true size.
                    #leading 0 values are stripped from the match result to ensure
                    #the correct decimalized integer value, but all-0 values are allowed to pass.
                    widthBytes = vp8xMatch.group(2).lstrip(b'\x00') or b'\x00'
                    width = int.from_bytes(widthBytes, byteorder='little') + 1

                    #Determine image height.
                    heightBytes = vp8xMatch.group(3).lstrip(b'\x00') or b'\x00'
                    height = int.from_bytes(heightBytes, byteorder='little') + 1

                      # Debug: print to ensure values are what we expect
                    print("Width Bytes (raw):", widthBytes)
                    print("Height Bytes (raw):", heightBytes)
                    return {
                        "width": width,
                        "height": height,
                        "color space": colorSpace
                    }
        return None
        
        
    def fileSave(self):
        pass