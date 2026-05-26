# Huffman Encoding Compression

This project is a Python implementation of **Huffman Encoding**, a lossless compression algorithm that assigns shorter binary codes to more frequent tokens and longer binary codes to less frequent tokens.

The project was completed as a homework assignment and focuses on file compression, frequency analysis, priority queues, binary trees, and encoding text data into a compressed binary format.

---

## Project Overview

The program reads an input text file, breaks the text into tokens, counts the frequency of each token, and builds a Huffman tree using a priority queue.

After the Huffman tree is created, each token is assigned a binary code. The encoded output is then written to a `.enc` file along with information needed to reconstruct the Huffman tree.

This project also includes a helper script for checking compression information, such as the original file size, encoded file size, compression ratio, and space saved.

---

## Features

### Huffman Encoding

- Reads text input from a file
- Tokenizes text based on whitespace
- Counts token frequencies
- Builds a Huffman tree using a priority queue
- Generates binary Huffman codes for each token
- Writes compressed output to a `.enc` file
- Stores Huffman tree information in the encoded file header

### Compression Information

- Compares original and encoded file sizes
- Calculates compression ratio
- Calculates space saved after encoding
- Displays formatted compression statistics

---

## Technologies Used

- Python 3
- Priority Queue / Heap
- Huffman Trees
- File I/O
- Binary Encoding
- Lossless Compression Concepts

---

## Files

| File | Description |
|---|---|
| `huffman_encoding.py` | Main Huffman encoding program |
| `compression-info.py` | Displays compression size information |
| `examples/small.dec` | Small sample text input |
| `examples/small.enc` | Example encoded output file |

---

## How Huffman Encoding Works

Huffman Encoding is a lossless compression technique. It works by giving shorter binary codes to tokens that appear more often and longer binary codes to tokens that appear less often.

For example, if the word `the` appears many times in a file, it may receive a short code like `01`. A less common word may receive a longer code such as `110101`.

This helps reduce the total number of bits needed to represent the original text.

---

## How to Run

Make sure Python 3 is installed.

To encode a file, run:

```bash
python huffman_encoding.py examples/small.dec