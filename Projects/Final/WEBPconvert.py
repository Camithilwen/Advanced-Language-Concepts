from webptools import dwebp, webpmux_extract
from webp import * 
import os
class WEBPconvert:
    '''Contains methods necessary to parse a WEBP file for important header data,
    decompress raw pixel data, and, currently, re-write to a PNG.'''
    def __init__(self):
        self.inData = None
        self.inputPath = None
        
   
    def fileOpen(self, path):
        """Open a binary file
        Returns: 
            - "OK" on success or exception data on reciept."""
        try:
            with open(path, 'rb') as inFile:
                self.inData = inFile.read()
                self.inputPath = path
            return "OK"
        except FileNotFoundError as ex:
            status = str(ex)
            return status
        except Exception as ex:
            status = str(ex)
            return status

    def isAnimated(self):
        """Checks if the given WEBP file is animated.
        Returns:
            - True if animated, False otherwise."""
        try:
            mux = webpmux.from_file(self.inputPath)
            return mux.is_animated  # Check if the file has animation chunks
        except Exception as ex:
            raise ValueError(f"Error while checking for WEBP animation flag: {ex}")
    
    def convertToGif(self, savePath):
            """
            Converts an animated WEBP to GIF.
            """
            try:
                with open(self.inputPath, "rb") as file:
                    anim_decoder = WebPAnimDecoder(file.read())
                    frames = []
                    while True:
                        frame = anim_decoder.get_next()
                        if frame is None:
                            break
                        frames.append(frame[0])  # Collect frames
                    # Save as GIF
                    frames[0].save(savePath, format="GIF", save_all=True, append_images=frames[1:], loop=0,
                                duration=anim_decoder.frame_durations)
                    print(f"Converted animated WEBP to GIF: {savePath}")
            except Exception as ex:
                raise ValueError(f"Error during GIF conversion: {ex}")

    def fileConvert(self, savePath):
        """Converts the given WEBP file to a PNG or GIF based on the file properties."""
        try:
            if self.isAnimated():
                #Convert animated WEBP to GIF.
                gifPath = f"{os.path.splitext(savePath)[0]}.gif"
                self.convertToGif(gifPath)
            else:
                #Convert static WEBP to PNG.
                dwebp(input_image=self.inputPath, output_image=f"{savePath} + .png", option="-o", logging="-v")
        except Exception as ex:
            raise ValueError(f"Error during conversion: {ex}")
        