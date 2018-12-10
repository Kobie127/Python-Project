"""This is the spellotron.  This program is based off of the autocorrection system that is found in
most smart systems in computers and phones.  This is the project for CSCI 141 at Rochester Institute of Technology
file: spellotron.py
author: Kobie Arndt"""

import sys #This imports sys which is used for command line arguments.
import re #This imports re which is used for searching some of the characters such as decimals.



#This is used for the capital letters that are found in the alphabet.
CAPITAL_LETTER_ALPHABET = list(chr(code) for code in range(ord('A'), ord('Z')+1))

#This is used for the lower case letters in the alphabet.
LOWER_LETTER_ALPHABET = list(chr(code) for code in range(ord('a'), ord('z')+1))

def adjacent():
    """The function adjacent opens the keyboard-letters.txt file and stores them in the dictionary.
    The reason for thos function is to store all of the keys that are adjacent to one another on a standard
    keyboard."""
    dict_adj = {} #This is the overall dictionary that will be used to store the adjacent keys.
    with open("keyboard-letters.txt") as file: #This line opens the file as specifies it as file for further use.
        for letters in file:
            lst = letters.strip().split() #This is used for stripping and splitting the letters in the file.
            dict_adj[lst[0]] = lst[1:]
    return dict_adj
Key_Adjacent = adjacent() #This becomes a global variable that all functions can use.

def decimals(st):
    """This function uses the import statement re.  A re is a special sequence of characters
    that helps you match or find other strings or sets of strings,
    using a specialized syntax held in a pattern. """
    return re.search("\d", st) #This uses re and searches for any decimals in the word or phrase.

def punc(str):
    """This function is used for punctuations in the overall program.  It looks for them and handles
    them accordingly. """
    strip_str = ''
    if not re.search("[a-zA-Z0-9]", str): #This uses re and specifies the characters to search for.
        return str, '' , ''
    elif re.search("[a-zA-Z0-9]",str):
        punc = re.split("([a-zA-Z0-9])", str)
        for x in punc[1: -1]:
            strip_str = strip_str + x
        return punc[0], strip_str, punc[-1]

def legal():
    """This function is for keeping all of the legal words in the american english dictionary in a set."""
    x = set() #This line declares the variable name and makes it a set()
    with open("american-english.txt") as file: #This specifies the opening of the file as file.
        for words in file:
            x.add(words.strip()) #This adds and strips the words in the file.
    return x
legal_words = legal() #This sets it as a global variable for other functions to use.


def adjacent_tester(word):
    """This is the tester function to see if there are any adjacent letters in the word or phrase inputted.
    This is used for the correction process also to see what key on the keyboard is next to what and see if
    it is the likely choice for the misspelled word."""
    (punctuation_left, strip_w, punctuation_right) = punc(word) #This is used for holding variables and uses the punc function.
    f_L = strip_w[0] #f_L stands for first letter in the word and will use strip_w at index 0 for the rest of the process.
    if strip_w == '':
        return word
    if f_L in CAPITAL_LETTER_ALPHABET: #This sees if the first letter is in the Capital letter alphabet.
        strip_w = strip_w.lower()
    if decimals(strip_w): #This checks to see if there are decimals.
        return "Is Number"
    if strip_w in legal_words:
        return word
    else:
        for i in range(len(strip_w)):
            chr = strip_w[i]
            if chr not in Key_Adjacent:
                continue
            else:
                for x in Key_Adjacent[chr]: #This uses the global variable from the previous function at index chr.
                    words_fixed = strip_w[:i] + x + strip_w[i+1:]
                    if words_fixed in legal_words:
                        if f_L in CAPITAL_LETTER_ALPHABET:
                            words_fixed = words_fixed.capitalize()
                        return punctuation_left + words_fixed + punctuation_right
        if words_fixed not in legal_words:
            return False


def missing_tester(word):
    """This missing_tester function will fix the missing letter in the misspelled word."""
    (punctuation_left, strip_w, punctuation_right) = punc(word) #This is used for holding variables and uses the punc function.
    f_L = strip_w[0] #f_L stands for first letter in the word and will use strip_w at index 0 for the rest of the process.
    if strip_w == '':
        return word
    if f_L[0] in CAPITAL_LETTER_ALPHABET: #This sees if the first letter is in the Capital letter alphabet.
        strip_w = strip_w.lower()
    if decimals(strip_w): #This checks to see if there are decimals.
        return "Is Number"
    elif strip_w in legal_words:
        return word
    else:
        for i in range(len(strip_w)):
            for x in LOWER_LETTER_ALPHABET:
                words_fixed = strip_w[:i] + x + strip_w[i:]
                if words_fixed in legal_words:
                    if f_L[0] in CAPITAL_LETTER_ALPHABET:
                        print(words_fixed)
                        words_fixed = words_fixed.capitalize()
                    return punctuation_left + words_fixed + punctuation_right
        if words_fixed not in legal_words:
            return False


def additional_tester(word):
    """This function will fix any of the additional letters that are in the word."""
    (punctuation_left, strip_w, punctuation_right) = punc(word)  #This is used for holding variables and uses the punc function.
    f_L = strip_w[0] #f_L stands for first letter in the word and will use strip_w at index 0 for the rest of the process.
    if strip_w == '':
        return word
    if f_L[0] in CAPITAL_LETTER_ALPHABET:  #This sees if the first letter is in the Capital letter alphabet.
        strip_w = strip_w.lower()
    if decimals(strip_w): #This checks to see if there are decimals.
        return "Is Number"
    elif strip_w in legal_words:
        return word
    else:
        for i in range(len(strip_w)):
            words_fixed = strip_w[:i] + strip_w[i+1:]
            if words_fixed in legal_words:
                if f_L[0] in CAPITAL_LETTER_ALPHABET:
                    words_fixed = words_fixed.capitalize()
                return punctuation_left + words_fixed + punctuation_right
        if words_fixed not in legal_words:
            return False


def correction(words):
    """This the correction algorithm that will do a series of checks to see when to do the certain
    corrections that are needed."""
    missing = missing_tester(words) #This is used as a variable for missing letters
    adj = adjacent_tester(words) #This is used as a variable for adjacent letters
    additional = additional_tester(words) #This is used as a variable for additional letters
    if adj == "Is Number":
        return words
    elif adj == words:
        return words
    elif adj == False:
        if missing == "Is Number":
            return words
        elif missing == words:
            return words
        elif missing == False:
            if additional == "Is Number":
                return words
            elif additional == words:
                return words
            elif additional == False:
                return False
            else:
                return additional
        else:
            return missing
    else:
        return adj


def process_file(file):
    """This function is for processing the words mode.  It will keep track of the variables and increment them
    accordingly.  IT also sets up lists to add the words into.  It will also print the correct
    statistical output for the spellotron."""
    word = 0
    correct = 0
    not_known = 0
    words_correct = []
    unknown_words = []
    for line in file:
        list = line.strip().split()
        for words in list:
            word += 1
            spell_correct = correction(words)
            if spell_correct != False:
                if words == spell_correct:
                    continue
                print(words, "->", spell_correct)
                words_correct.append(words)
                correct += 1
            else:
                unknown_words.append(words)
                not_known += 1
    print("The number of words read from the file are" + "" + str(word))
    print("The number of corrected words are" +  " " + str(correct))
    print("The words that were corrected were:")
    print(words_correct)
    print("The number of unknown words are" + " " + str(not_known))
    print("The words that were unknown were:")
    print(unknown_words)


def replace_value(x, y, z):
    """This function will replace the proper key."""
    for i in range(len(x)):
        if x[i] != z:
            pass
        else:
            x[i] = y
    return x


def process_lines(file):
    """This function will process the input in lines mode.  This is different from words mode because it
    shows the entire line corrected rather than the individual word corrected.It will keep track of the variables and increment them
    accordingly.  IT also sets up lists to add the words into.  It will also print the correct
    statistical output for the spellotron."""
    word = 0
    correct = 0
    not_known = 0
    correct_words = []
    additional_words = []
    for line in file:
        list = line.strip().split()
        for words in list:
            word += 1
            spell_correct = correction(words)
            if spell_correct != False:
                if words == spell_correct:
                    continue
                correct += 1
                correct_words.append(words)
                list = replace_value(list, spell_correct, words)
            else:
                not_known += 1
                additional_words.append(words)
        print(' '.join(list))
    print("The number of words read from the file are" + " " + str(word))
    print("The number of corrected words are" + " " + str(correct))
    print("The corrected words were:")
    print(correct_words)
    print("The number of unknown words are" + " " + str(not_known))
    print("The unknown words were:")
    print(additional_words)


def main():
    """This is the main method of the entire program.  It uses command line arguments to access
    lines or words mode.  This is used in the terminal of the program."""
    modes = ['words', 'lines']
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('We have a problem here', file=sys.stderr)
    elif len(sys.argv) == 2:
        if sys.argv[0] != 'spellotron.py' or sys.argv[1] not in modes:
            print('We have a problem here', file=sys.stderr)
        else:
            # file = sys.stdin
            if sys.argv[1] == 'words':
                process_file(sys.stdin)
            elif sys.argv[1] == 'lines':
                process_lines(sys.stdin)
    else:
        if sys.argv[0] != 'spellotron.py' or sys.argv[1] not in modes:
            print('We have a problem here', file=sys.stderr)
        else:
            file = open(sys.argv[2])
            if sys.argv[1] == 'words':
                process_file(file)
            elif sys.argv[1] == 'lines':
                process_lines(file)
            file.close()



main()