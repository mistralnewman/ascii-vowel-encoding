# Code to encode ASCII strings as English words
# By Hannah Newman <HN860433@wcupa.edu>

import random

# input: a text string
# output: binary stored as a string with letters replaced with either 1 or 0
def word_to_bin(string):
    # string is converted to lowercase since uppercase and lowercase letters are equivalent
    string = string.lower()
    # binary is stored as string to conserve leading zeroes
    binary = ""
    for letter in string:
        if is_zero(letter):
            binary += "0"
        else:
            binary += "1"
    return binary

# input: an ASCII string
# output: each character's ASCII index in 8 bits, as a string
def str_to_bin(string):
    binary = ""
    for char in string:
        binary += str(format(ord(char), "b")).zfill(8) # adds leading zeroes until length 8
    return binary

# input: a character
# output: whether or not the letter should be replaced with 0
def is_zero(letter):
    return letter in "aeiouy"

# get words from a file
wordfile = open("english2.txt")
words = wordfile.readlines()

# remove trailing whitespace from each word
words = [word.rstrip() for word in words]

# keys: binary as a string
# values: words which "translate" to this string
words_by_bin = dict()

# initializes current maximum length
maxlen = len(word_to_bin(words[0]))

# adds each word to the list of words with the same binary equivalent
for word in words:
    wordbin = word_to_bin(word)
    length = len(word)
    # if the word has the new biggest length, save its length as maxlen
    if length > maxlen:
        maxlen = length
    if wordbin in words_by_bin:
        words_by_bin[wordbin] += [word]
    else:
        words_by_bin[wordbin] = [word]

# input: plaintext ASCII string
# output: ciphertext matching the ASCII
def binary_encode(string):
    # converts input string to binary string and then passes it to recursive function
    sbin = str_to_bin(string)
    # initializes length of fitting words searched
    length = min(len(sbin), maxlen)
    return bin_to_words(sbin, length)

# input: binary representation of ASCII string, length of word to try
# output: ciphertext matching the ASCII
def bin_to_words(string, length):
    # if the length is 0, return an empty string
    if length <= 0:
        return ""
    # otherwise, find a word of length length and add it
    if string[:length] in words_by_bin:
        # pick a random word with matching binary
        substring = string[:length]
        word = words_by_bin[substring][random.randint(0, len(words_by_bin[substring])) - 1]
        # tail recursion: return the word plus the translation of the rest of the string
        newlen = min((len(string) - length), maxlen)
        return word + " " + bin_to_words(string[length:], newlen)
    # if there is no word of length length, reduce length by one
    return bin_to_words(string, length - 1)

# reverse conversion function
# input: ciphertext
# output: plaintext
def binary_decode(string):
    # remove spaces from the string
    string = string.replace(" ", "")
    string = word_to_bin(string)
    plaintext = ""
    # convert each group of 8 binary digits to a character and add to plaintext
    for i in range(0, len(string), 8):
        plaintext += chr(int(string[i:i+8], 2))
    return plaintext

print binary_encode("Hello world!")
