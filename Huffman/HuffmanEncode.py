# HUFFMAN ENCODING: Capstone Assignment
# Fall 2017 - CSC 598
# October 4, 2017
# <Multiple Authors>

from Heap import Heap

# Probably can't do this faster than O(nlogn) without a priori sorted array.

input_file = open("input.txt", "r")
file = input_file.read()


# Read from text file in same directory. This be O(n)
def freq_dict():
    freq = {}
    for char in file:
        if char not in freq:
            freq[char] = 0
        freq[char] += 1
    return freq

print(freq_dict())


# Runs O(log n)
def encode_huffman():
    huffman = Heap()
    huffman.make_heap(freq_dict())
    huffman.merge_nodes()
    huffman.init_codes()
    padded = huffman.pad_encoded_text(file)
    print(padded)
    b = huffman.byte_array(padded)

    with open("output.bin", "wb") as output:
        output.write(bytes(b))

encode_huffman()
