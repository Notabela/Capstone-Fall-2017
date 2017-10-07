# HUFFMAN ENCODING: Capstone Assignment
# Fall 2017 - CSC 598
# October 4, 2017
# <Multiple Authors>

from Heap import Heap

# Probably can't do this faster than O(nlogn) without a priori sorted array.

input_file = open("input.txt", "r")
file = input_file.read()


# More efficient way of doing frequency dict
def freq_dict(file):
    freq = {}
    for char in file:
        freq[char] = freq.get(char, 0) + 1
    print(freq)
    return freq


# Runs O(log n)
def encode_huffman():
    huffman = Heap()
    huffman.make_heap(freq_dict(file))
    huffman.merge_nodes()
    huffman.init_codes()
    encoded = huffman.encode_text(file)
    print(encoded)
    b = huffman.byte_array(encoded)
    #padded = huffman.pad_encoded_text(file)
    #print(padded)
    #b = huffman.byte_array(padded)

    with open("output.bin", "wb") as output:
        output.write(bytes(b))

encode_huffman()
