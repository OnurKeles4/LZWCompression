import json
import os
from io import StringIO

import numpy as np
from ImageMethods import npToPIL, imageToArray, readImage


class CompressImage:

    def __init__(self, path):

        self.path_name = os.path.basename(path[:f"{path}".find('.')])  # Left side of the path (name)
        self.path_extension = os.path.basename(path[f"{path}".find('.'):])  # Right side of the path (extension)
        print("path_name: ", self.path_name, "path_exten:", self.path_extension)

        self.path_json = os.path.join(os.path.dirname(path), self.path_name + ".json")

        self.output_path = os.path.join(os.path.dirname(path), self.path_name + ".bin")
        """ self.isGray = False
        if isGray == "gray":
            self.isGray = True
        elif isGray == "color":
            self.isGray = False
        else:
            warnings.warn("wrong color")"""

        self.path = path
        self.codelength = 24
        self.compressed = []        # Individual variables for compress process.
        self.compressImage()

    def LossyArray(self, array):
        n = len(array)
        m = len(array[0])
        darr = np.array(array, copy=True)

        for i in range(n):
            for j in range(1, m):
                # print(f"{i} and {j}")
                darr[i][j] = array[i][j] - array[i][j - 1]

        return darr

    def int_array_to_binary_string(self, int_array):
        #print("int_array:", int_array)
        bitstr = ""
        bits = self.codelength
        for num in int_array:
            for n in range(bits):
                if num & (1 << (bits - 1 - n)):
                    bitstr += "1"
                else:
                    bitstr += "0"
        return bitstr

    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        # print("padded info: ", padded_info)
        encoded_text = padded_info + encoded_text
        """width = self.image.width
        height = self.image.height
        width_byte = bytes(width) height_byte = bytes(height)... try to add this values at the start of the byte 
        array. (issue is their length is not specific values) """

        return encoded_text

    def compress(self, uncompressed):
        """Compress a string to a list of output symbols."""

        # Build the dictionary.
        dict_size = 256
        dictionary = {chr(i): i for i in range(dict_size)}
        w = ""
        for c in uncompressed:
            c = chr(c)
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                self.compressed.append(dictionary[w])
                dictionary[wc] = dict_size
                dict_size += 1
                w = c
        if w:
            self.compressed.append(dictionary[w])

    def compressImage(self):

        with open(self.output_path, 'wb') as output, open(self.path_json, 'w') as json_file:
            path_extension = os.path.basename(self.path[f"{self.path}".find('.'):])

            image = readImage(self.path)

            """if self.isGray:
                image = color2gray(image)"""

            image_array = imageToArray(image) # Returns Matrix
            json.dump({"height": image.height, "width": image.width, "extension": path_extension}, json_file, indent=4)

            uncompressed = self.LossyArray(image_array).flatten()   #Flatten Matrix to 1D array
            #uncompressed_lossy = self.LossyArray(uncompressed)
            #print("uncompressed length: ", len(uncompressed), "")
            self.compress(uncompressed)

            #print(f"compressed length: {len(self.compressed)}")
            binary_string = self.int_array_to_binary_string(self.compressed)
            encoded_text = self.pad_encoded_text(binary_string)
            byte_array = self.get_byte_array(encoded_text)
            output.write(bytes(byte_array))

class DecompressImage:

    def __init__(self, path):
        self.path_name = os.path.basename(path[:f"{path}".find('.')])  # Left side of the path (name)
        self.path_extension = os.path.basename(path[f"{path}".find('.'):])  # Right side of the path (extension)
        #print("path_name: ", self.path_name, "path_exten:", self.path_extension)

        self.path_json = os.path.join(os.path.dirname(path), self.path_name + ".json")


        self.output_path = os.path.join(os.path.dirname(path), self.path_name + "_decompress.png")

        """self.isGray = False
        if isGray == "gray":
            self.isGray = True
        elif isGray == "color":     # Is this necessary
            self.isGray = False
        else:
            warnings.warn("wrong color")
"""
        self.path = path  # Duplicate in ImageMethods ?
        self.codelength = 24
        self.decompressed = []
        self.decompressImage()



    def get_compressed_data(self, file):
        bit_string = ""
        byte = file.read(1)
        while (len(byte) > 0):
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)
        return bit_string

    def decompress(self, int_codes):
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}
        result = StringIO()
        w = chr(int_codes.pop(0))
        result.write(w)
        for k in int_codes:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result.write(entry)
            dictionary[dict_size] = w + entry[0]
            dict_size += 1
            w = entry

        self.decompressed = [ord(c) for c in result.getvalue()]

    # decoder
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        # print("padded:", padded_info)
        # print("padded_encoded_text:", padded_encoded_text)

        extra_padding = int(padded_info, 2)
        # print("extra padding:", extra_padding)
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]
        # print("encoded text len:", len(encoded_text))
        int_codes = []
        for bits in range(0, len(encoded_text), self.codelength):
            int_codes.append(int(encoded_text[bits:bits + self.codelength], 2))
        return int_codes

    def decompressImage(self):
        #print("dd ", self.path)
        with open(self.path, "rb") as input, open(self.path_json, "r") as json_file:

            data = json.load(json_file)
            width = data["width"]
            height = data["height"]
            value = self.get_compressed_data(input)
            #print("bbb", value)
            int_codes = self.remove_padding(value)
            #print("len of bit_string", len(int_codes))
            #print("bit_string: ",bit_string, "length:", len(bit_string))
            self.decompress(int_codes)
            print("decompressed length: ", len(self.decompressed))
            image = (npToPIL(width, height, self.decompressed))
            image.save(self.output_path)


class CompressText:

    def __init__(self, path):
        self.path_name = os.path.basename(path[:f"{path}".find('.')])  # Left side of the path (name)
        self.path_extension = os.path.basename(path[f"{path}".find('.') + 1:])  # Right side of the path (extension)
        print(self.path_extension)

        self.output_path = os.path.join(os.path.dirname(path), self.path_name + ".bin")

        self.path = path
        self.codelength = 12        # Codelength might change depending on the data.
        self.compressed = []
        self.compressText()

    def compress(self, uncompressed):
        """Compress a string to a list of output symbols."""

        # Build the dictionary.
        dict_size = 256
        dictionary = {chr(i): i for i in range(dict_size)}
        w = ""
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                self.compressed.append(dictionary[w])
                dictionary[wc] = dict_size
                dict_size += 1
                w = c
        if w:
            self.compressed.append(dictionary[w])


    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        print("padded info: ", padded_info)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def int_array_to_binary_string(self, compressed):
        bitstr = ""
        bits = self.codelength
        for num in compressed:
            for n in range(bits):
                if num & (1 << (bits - 1 - n)):
                    bitstr += "1"
                else:
                    bitstr += "0"
        return bitstr


    def compressText(self):
        with open(self.path, 'r+') as file, open(self.output_path, 'wb') as output:
            uncompressed = file.read()  # read file
            uncompressed = uncompressed.rstrip()

            self.compress(uncompressed)  # compress
            print("uncompressed:", uncompressed)
            binary_string = self.int_array_to_binary_string(self.compressed)
            encoded_text = self.pad_encoded_text(binary_string)
            byte_array = self.get_byte_array(encoded_text)  # put in byte form and pad text
            output.write(bytes(byte_array))

class DecompressText:

    def __init__(self, path):
        self.path_name = os.path.basename(path[:f"{path}".find('.')])  # Left side of the path (name)
        self.path_extension = os.path.basename(path[f"{path}".find('.') + 1:])  # Right side of the path (extension)
        print(self.path_extension)


        self.output_path_x = os.path.join(os.path.dirname(path), self.path_name + "_decompress.txt")

        self.path = path
        self.codelength = 12
        self.decompressed = []
        self.decompressText()

    def decompress(self, bit_string):
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}
        result = StringIO()
        w = chr(bit_string.pop(0))
        result.write(w)
        for k in bit_string:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result.write(entry)
            dictionary[dict_size] = w + entry[0]
            dict_size += 1
            w = entry

        self.decompressed = result.getvalue()

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]
        int_codes = []
        for bits in range(0, len(encoded_text), self.codelength):
            int_codes.append(int(encoded_text[bits:bits + self.codelength], 2))
        return int_codes

    def get_compressed_data(self, file):
        bit_string = ""
        byte = file.read(1)
        while (len(byte) > 0):
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)
        return bit_string

    def decompressText(self):
        with open(self.path, 'rb') as file, open(self.output_path_x, 'w') as output:
            value = self.get_compressed_data(file)
            int_code = self.remove_padding(value)  # It's not string
            #print(self.compressed)                 # It's not going to work/ old version print
            print("bbb", int_code)
            self.decompress(int_code)
            print("aaaa", self.decompressed)
            #print("wqewqeqw", str(self.decompressed))
            output.write(str(self.decompressed))  # str is not very safe


if __name__ == "__main__":
    CompressText("TOBE.txt")
    DecompressText("TOBE.bin")
    CompressImage("RGBTest.bmp")
    DecompressImage("RGBTest.bin")

