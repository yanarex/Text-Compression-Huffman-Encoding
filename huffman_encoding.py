import sys
import heapq


# Reads the input text file and returns a list of tokens.
def get_tokens(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    # Tokenization based on whitespace
    tokens = text.split()
    return tokens


# Writes the output file in binary mode
def write_file_output(filename, treestring, codestring):
    # Convert the binary string into a byte array
    byte_list = []
    for i in range(0, len(codestring), 8):
        byte_chunk = codestring[i:i+8]
        byte_val = int(byte_chunk, 2)
        byte_list.append(byte_val)
    codes = bytes(byte_list)
    
    output_filename = filename + ".enc"
    with open(output_filename, 'wb') as f:
        # Write the Huffman tree header as UTF-8 bytes
        f.write(treestring.encode('utf-8'))
        f.write(b'\n')  
        # Write the encoded binary data
        f.write(codes)
    print("Encoded file written to:", output_filename)


# Constructs a frequency dictionary mapping each token to its frequency
def build_frequency(tokens):
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq


# Builds the Huffman tree using priority queue
# Each leaf node represents a token with its frequency
def build_huffman_tree(freq):
    heap = []
    for token, f in freq.items():
        heapq.heappush(heap, Node(f, token=token))
    # Handle edge case: only one unique token.
    if len(heap) == 1:
        return heapq.heappop(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    return heapq.heappop(heap)


# Recursively traverses the Huffman tree to assign a binary code to each token.
# More frequent tokens receive shorter codes.
def generate_codes(node, prefix="", map=None):
    if map is None:
        map = {}
    if node.token is not None:
        # Special case: if only one token, assign code "0".
        if prefix == "":
            map[node.token] = "0"
        else:
            map[node.token] = prefix
    else:
        generate_codes(node.left, prefix + "0", map)
        generate_codes(node.right, prefix + "1", map)
    return map


# Returns the label for a token for use in the tree header.
# Special tokens (whitespace, newline, etc.) are given special labels.
def get_label(token):
    if token == "\r":
        return "~1"
    elif token == " ":
        return "~2"
    elif token == "\t":
        return "~3"
    elif token == "\n":
        return "~4"
    else:
        return token


# Performs a postorder traversal of the Huffman tree.
# Internal nodes are labeled with a "#"
# The int_nodes list is populated with tuples (left_label, right_label)
# for each internal node, in the order they are created.
def assign_labels(node, int_nodes, counter):
    if node.token is not None:
        return get_label(node.token)
    left_label = assign_labels(node.left, int_nodes, counter)
    right_label = assign_labels(node.right, int_nodes, counter)
    counter[0] += 1
    current_label = "#" + str(counter[0])
    int_nodes.append((left_label, right_label))
    return current_label


# Replaces each token in the input list with its Huffman code 
# Returns the padded codestring and the number of extra 0 bits added.
def encode_text(tokens, map):
    codes_list = [map[token] for token in tokens]
    codestring = "".join(codes_list)
    extra_zeros = (8 - (len(codestring) % 8)) % 8
    codestring += "0" * extra_zeros
    return codestring, extra_zeros

# Node class for building the Huffman tree.
class Node:
    def __init__(self, freq, token=None, left=None, right=None):
        self.freq = freq 
        self.token = token 
        self.left = left
        self.right = right


def main():
    input_filename = sys.argv[1]
    tokens = get_tokens(input_filename)
    if not tokens:
        print("Input file is empty.")
        sys.exit(1)
    
    # Build frequency table and Huffman tree while generating Huffman codes
    freq = build_frequency(tokens)
    root = build_huffman_tree(freq)
    map = generate_codes(root)
    
    # produces the codestring and compute extra zeros.
    codestring, extra_zeros = encode_text(tokens, map)
    
    int_nodes = []
    counter = [0]  # counter for node labeling.
    assign_labels(root, int_nodes, counter)

    # The first line is the number of internal nodes.
    tree_lines = [str(len(int_nodes))]
    # Next, one line per internal node containing its left and right labels.
    for left_label, right_label in int_nodes:
        tree_lines.append(left_label + " " + right_label)
    
    # Final line: the number of extra 0 bits added (padding).
    tree_lines.append(str(extra_zeros))
    treestring = "\n".join(tree_lines)
    
    # Encoded output to file.
    write_file_output(input_filename, treestring, codestring)

if __name__ == '__main__':
    main()
