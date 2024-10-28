import numpy as np
import zlib
class PNGwrite:
    '''Contains methods to create PNG header information from provided
    file metadata and compress a provided numpy array of pixel data 
    to PNG format using zlib.'''

    def __init__(self):
        self.metadata = None
        self.IHDR = None
        self.IDAT = None
        self.IEND = None
        self.width = None
        self.height = None

    def header(self, metadata):
        '''Creates a PNG IHDR chunk from a provided metadata dictionary.
         Parameters:
            - metadata : Dictionary of categorized header data parsed from a prior file format.
            - bitDepth : indicates bits-per-channel of image data. Always set to 8 for this program.
            - colorType : Must be 6 if RGBA or 2 if RGB only, according to the PNG IHDR specification.
            - compressionType : Default of 0, as DEFLATE is the only supported form of compression.
            - filterMethod : Also has defaults to 0 as no filtering is required for DEFLATE.
            - interlaceMethod : Unused for my purposes and is defaulted to 0.'''

        if metadata:

            '''Parse file metadata dictionary for crucial values.'''
            self.metadata = metadata
            self.width = metadata["width"]
            self.height = metadata["height"]
            if metadata["alpha"]:
                alpha = True
            else:
                alpha = False
            #I want to add support to transfer metadata in the future.
            # EXIF = metadata["EXIF metadata"] if\
            # metadata["EXIF metadata"] is not None else None
            # XMP = metadata["XMP metadata"] if\
            # metadata["XMP metadata"] is not None else None 
            #Prepare header data
            bitDepth = 8
            if alpha:
                colorType = 6
            else:
                colorType = 2
            compressionType = 0
            filterMethod = 0
            interlaceMethod = 0
            #Write header data
            print("width", self.width)
            print("height", self.height)
            headerData = self.width.to_bytes(4, 'big') + self.height.to_bytes(4, 'big') + \
            bytes([bitDepth, colorType, compressionType, filterMethod, interlaceMethod])
            self.IHDR = self.chunkUtil(b'IHDR', headerData)

        else:
            raise UserWarning("metadata is None.")
    
    def data(self, data):
        '''Writes the IDAT chunk containing filtered and compressed
        image data. Compression occurs via the DEFLATE algorithm. I didn't have time to learn
        to write this myself so I am using the DEFLATE functionaliy built into zlib.
        Funnily enough, PNG and .zip use the same compression algorithm.
        By default, no filter is applied, but a 0 still needs to be appended to the start of 
        each matrix row to adhere to PNG format standards.
        Parameters:
            - data : a numpy array of RGB or RGBA values.
            - bytesPerPixel : Equivalent to header bitDepth * number of channels.
            - colorType : Equivalent to header colorType'''
        height, width, channels = data.shape
        print("Channels:", channels)
        print("data:", data)
        if channels not in [3, 4]:
            raise ValueError("Invalid channel count. Must be RGB or RGBA.")
        alpha = channels == 4
        bytesPerPixel = 4 if alpha else 3
        colorType = 6 if alpha else 2
        if channels != bytesPerPixel:
            raise ValueError("Channel count incorrect for given header data.")
        #Construct file structure
        scanLines = bytearray()
        for row in data:
            scanLines.append(0)
            rowData = row.astype(np.uint8).tobytes()
            scanLines.extend(rowData)
        #Compress file structure
        compressedData = zlib.compress(scanLines)
        #write data chunk
        self.IDAT = self.chunkUtil(b'IDAT', compressedData)

    def end(self):
        '''Writes the IEND chunk at the end of file. This chunk contains no data.'''
        self.IEND = self.chunkUtil(b'IEND', b'')

    def chunkUtil(self, chunkType, data):
        '''Packages chunk data given an encoded description and data field.
        A checksum is appended to the returned value.
        Parameters:
            - chunkType : example: b'IDAT'
            - data : a bytestream of compressed or uncompressed data
            
        Returns:
            - A complete PNG chunk as a bytestream.'''
        chunk = chunkType + data
        length = len(data).to_bytes(4, byteorder='big')
        checksum = zlib.crc32(chunk).to_bytes(4, byteorder='big')
        return length + chunk + checksum
    
    def write(self, path):
        '''Writes the converted data to a complete PNG file given a path with filename.'''
        with open(path, 'wb') as outFile:
            outFile.write(b'\x89PNG\r\n\x1a\n')
            outFile.write(self.IHDR)
            outFile.write(self.IDAT)
            outFile.write(self.IEND)