import heapq


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __eq__(self, other):
        if other is None or not isinstance(other, Node):
            return False
        return self.freq == other.freq

    def __lt__(self, other):
        return self.freq < other.freq


class Heap:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.mapping = {}

    def make_heap(self, freq):
        for key in freq:
            node = Node(key, freq[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = Node(None, (node1.freq + node2.freq))
            merged.left = node2
            merged.right = node1

            heapq.heappush(self.heap, merged)

    def make_codes(self, root, current):
        # Base Case
        if root is None:
            return
        if root.char is not None:
            print(root.char, current)
            self.codes[root.char] = current
            self.mapping[current] = root.char
            return

        self.make_codes(root.right, current + "1")
        self.make_codes(root.left, current + "0")

    def init_codes(self):
        root = heapq.heappop(self.heap)
        current = ""
        self.make_codes(root, current)

    def pad_encoded_text(self, file):
        encoded_text = ""
        for char in file:
            encoded_text += self.codes[char]

        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)
        b = bytearray()
        for i in range(len(padded_encoded_text)):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b
