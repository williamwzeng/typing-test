""" Typing Test implementation """

from utils import *
from ucb import main

# BEGIN Q1-5
"*** YOUR CODE HERE ***"
def lines_from_file(path):
    file = open(path, 'r')
    lst = []
    for word in file:
        lst.append(strip(word))
    return lst

def new_sample(path, i):
    return lines_from_file(path)[i]

def analyze(sample_paragraph, typed_string, start_time, end_time):
    wpm = ((len(typed_string) / 5) / (end_time - start_time)) * 60

    def accuracy(sample_paragraph, typed_string):
        reference_list = split(sample_paragraph)
        typed_list = split(typed_string)
        correct_words = 0
        i = 0
        if not typed_list:
            return 0.0
        while i < min(len(typed_list), len(reference_list)):
            if reference_list[i] == typed_list[i]:
                correct_words += 1
            i += 1
        return round(correct_words / min(len(reference_list), len(typed_list)) * 100, 2)
            
    return [wpm, accuracy(sample_paragraph, typed_string)]


def pig_latin(word):
    if word[0] in 'aeiou':
        return word + 'way'
    else:
        consonants = ''
        i = 0
        while i < len(word) and word[i] not in 'aeiou':
            consonants += word[i]
            i += 1
        return word[i:] + consonants + 'ay'
        
def autocorrect(user_input, words_list, score_function):
    if user_input in words_list:
        return user_input
    else:
        return min(words_list, key=lambda x: score_function(user_input, x))

def swap_score(string1, string2):
    if min(len(string1), len(string2)) == 0:
        return 0
    else:
        if string1[0] == string2[0]:
            return 0 + swap_score(string1[1:], string2[1:])
        else:
            return 1 + swap_score(string1[1:], string2[1:])
# END Q1-5

# Question 6

def score_function(word1, word2):
    """A score_function that computes the edit distance between word1 and word2."""
    # BEGIN Q6
    "*** YOUR CODE HERE ***"
    if not word1 or not word2:
        return max(len(word1), len(word2))
    elif word1[0] == word2[0]:
        return score_function(word1[1:], word2[1:])
    else:
        add_char = 1 + score_function(word1, word2[1:])
        remove_char = 1 + score_function(word1[1:], word2)
        substitute_char = 1 + score_function(word1[1:], word2[1:])
    return min(add_char, remove_char, substitute_char)
    # END Q6

KEY_DISTANCES = get_key_distances()

# BEGIN Q7-8
"*** YOUR CODE HERE ***"
def score_function_accurate(word1, word2):
    if not word1 or not word2:
        return max(len(word1), len(word2))
    elif word1[0] == word2[0]:
        return score_function_accurate(word1[1:], word2[1:])
    else:
        add_char = 1 + score_function_accurate(word1, word2[1:])
        remove_char = 1 + score_function_accurate(word1[1:], word2)
        substitute_char = KEY_DISTANCES[(word1[0], word2[0])] + score_function_accurate(word1[1:], word2[1:])
    return min(add_char, remove_char, substitute_char)



cache = {}
def score_function_final(word1, word2):
    if not word1 or not word2:
        return max(len(word1), len(word2))
    elif (word1, word2) not in cache and (word2, word1) not in cache:
        if word1[0] == word2[0]:
            return score_function_final(word1[1:], word2[1:]) 
        else:
            add_char = 1 + score_function_final(word1, word2[1:])
            remove_char = 1 + score_function_final(word1[1:], word2)
            substitute_char = KEY_DISTANCES[(word1[0], word2[0])] + score_function_final(word1[1:], word2[1:])
        cache[(word1, word2)] = min([add_char, remove_char, substitute_char])
        return cache[(word1, word2)]
    else:
        if (word1, word2) in cache:
            return cache[(word1, word2)]
        elif (word2, word1) in cache:
            return cache[(word2, word1)]
# END Q7-8
