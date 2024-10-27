# import re


# header = b'RIFF\x86&\x06\x00WEBPVP8X\n\x00\x00\x00<\x00\x00\x00\xff\x04\x00D\x04\x00ICCP'

# # Locate the start position of 'VP8X' in the header
# vp8x_start = header.find(b'VP8X')
# print("VP8X found at position:", vp8x_start)

# # If 'VP8X' is found, extract the bytes directly for examination
# if vp8x_start != -1:
#     # Print the 20 bytes after VP8X to check structure
#     post_vp8x = header[vp8x_start + 4:vp8x_start + 24]
#     print("Bytes after VP8X:", post_vp8x)
# else:
#     print("VP8X not found")


# import re

# # Pattern to match any sequence after 'VP8X' for inspection
# pattern = b'VP8X(.+)'

# # Attempt to match and capture bytes following 'VP8X'
# vp8x_match = re.search(pattern, header)
# if vp8x_match:
#     print("Data after VP8X:", vp8x_match.group(1))
# else:
#     print("No match found")


# if vp8x_start != -1:
#     # Skip 8 bytes after 'VP8X' for padding
#     flag_byte = header[vp8x_start + 4]
#     width_bytes = header[vp8x_start + 12:vp8x_start + 15]
#     height_bytes = header[vp8x_start + 15:vp8x_start + 18]

#     # Display extracted bytes and convert to integer for width and height
#     print("Flag byte:", flag_byte)
#     print("Width bytes:", width_bytes)
#     print("Height bytes:", height_bytes)
#     width = int.from_bytes(width_bytes, byteorder='little') + 1
#     height = int.from_bytes(height_bytes, byteorder='little') + 1
#     print("Width:", width)
#     print("Height:", height)
# else:
#     print("VP8X chunk not found")

import re

# Example binary string with a known pattern to test byte-by-byte matching
binary_data = b'VP8X1234567abc123xyz'
with open("garf.webp", 'rb') as inFile:
    inData = inFile.read()
print(rb'inData')

# Match 'VP8X', then 7 bytes, then 3 bytes (for width), then 3 bytes (for height)
pattern = b'VP8X(.{7})(.{3})(.{3})'
#match = re.search(pattern, binary_data)
match = re.search(pattern, inData, re.DOTALL)

if match:
    print("Group 1 (7 bytes):", match.group(1))  # Expected to be '1234567'
    print("Group 2 (3 bytes):", match.group(2))  # Expected to be 'abc'
    print("Group 3 (3 bytes):", match.group(3))  # Expected to be '123'
else:
    print("No match found")
