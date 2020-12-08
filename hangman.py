# Problem Set 2, hangman.py
# Name: Perederei Bogdan
# Collaborators: -
# Time spent: 5 hours


import random
import string

WORDLIST_FILENAME = "words.txt"
EN_VOWELS = {"a", "e", "i", "o", "u"}
GUESSES_AT_START = 6
WARNINGS_AT_START = 3
SYMBOL_FOR_HINTS = '*'
LOWER_BAR = '_'


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    letters_guessed = set(letters_guessed)
    new_set = set(secret_word)
    if letters_guessed | new_set == letters_guessed:
    #This command combine two sets, if  whole new_set is in letters_guessed, this will give us set letters_guessed
    #If whole new_set is not in letters_guessed, than it will give us set, which is bigger, than letters_guessed
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    list_guessed_word = []
    for symbol in secret_word:
        if symbol in letters_guessed:
            list_guessed_word.append(symbol)
        else:
            list_guessed_word.append(LOWER_BAR + ' ')
    #Part of function below is needed to delete space, if not guessed letter is in the end of the word
    if list_guessed_word[-1] == LOWER_BAR + ' ':
        list_guessed_word[-1] = LOWER_BAR
    return ''.join(list_guessed_word)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    list_of_avaible_letters = []
    for letters in string.ascii_lowercase:
        if letters not in letters_guessed:
            list_of_avaible_letters .append(letters)
    return ''.join(list_of_avaible_letters)

def output_brief_hangman(secret_word):
    '''
    Instructions to the game for player
    '''
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have 3 warnings left")


def input_information(guesses_left, letters_guessed):
    '''
    Main information for the player
    '''
    print("You have", guesses_left, "guesses left")
    print("Available letters:", get_available_letters(letters_guessed))
    guessed_letter = input("Please guess a letter: ")
    return guessed_letter


def not_correct_input_losing_warnings(warnings_left, secret_word, letters_guessed):
    '''
    System of losing warnings when letter wasn't input
    '''
    warnings_left -= 1
    print("Oops! That is not a valid letter. You have", warnings_left, "warnings left:",
          get_guessed_word(secret_word, letters_guessed))
    return warnings_left

def not_correct_input_losing_guesses(guesses_left, secret_word, letters_guessed):
    '''
    System of losing guesses when letter wasn't input and not having warnings left.
    '''
    guesses_left -= 1
    print("Oops! That is not a valid letter. You have no warnings left so you lose one guess:",
          get_guessed_word(secret_word, letters_guessed))
    return guesses_left

def guessed_before_losing_warnings(warnings_left, secret_word, letters_guessed):
    '''
    System of losing warnings for entering letter which was guessed before
    '''
    warnings_left -= 1
    print("Oops! You've already guessed that letter. You have", warnings_left, "warnings left:",
          get_guessed_word(secret_word, letters_guessed))
    return warnings_left

def guessed_before_losing_guesses(guesses_left, secret_word, letters_guessed):
    '''
    System of losing guesses for entering letter which was guessed before and not having
    warnings left.
    '''
    guesses_left -= 1
    print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:",
          get_guessed_word(secret_word, letters_guessed))
    return guesses_left


def results(guessed_letter, guesses_left, secret_word, letters_guessed):
    '''
    Showing results of current guessing
    '''
    letters_in_secret_word = set(secret_word)
    if guessed_letter in letters_in_secret_word:
        # Part of code for correct guess
        print("Good guess:", get_guessed_word(secret_word, letters_guessed))
        return guesses_left
    else:
        # System of losing guesses for incorrect guessed word
        if guessed_letter in EN_VOWELS:
            guesses_left -= 2
        else:
            guesses_left -= 1
        print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
        return guesses_left


def end_of_the_game(winning, guesses_left, secret_word):
    '''
    Showing information about losing or winning
    '''
    if winning:
        total_score = guesses_left * len(set(secret_word))
        print("Congratulations, you won! Your total score for this game is:", total_score)
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)


def main_match_win_or_lose(guesses_left, letters_guessed, secret_word, warnings_left, hints_switch):
    '''
    This function is the main part of game hangman.
    Is works with functions during match and showing needed information for the player.
    It returns true or false, which is understood as winning or losing in hangman.
    '''
    while True:
        print("--------------------------------------")
        if guesses_left <= 0:
            return False
        guessed_letter = input_information(guesses_left, letters_guessed)
        if hints_switch and guessed_letter == SYMBOL_FOR_HINTS:
            #Game with hints activated
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        if guessed_letter.isalpha() and len(guessed_letter) == 1 and guessed_letter in string.ascii_letters:
            guessed_letter = guessed_letter.lower()
        else:
            #System of losing warnings/guesses activated
            if warnings_left == 0:
                guesses_left = not_correct_input_losing_guesses(guesses_left, secret_word, letters_guessed)
            else:
                warnings_left = not_correct_input_losing_warnings(warnings_left, secret_word, letters_guessed)
            continue
        if guessed_letter in letters_guessed:
            #System of losing warnings/guesses activated
            if warnings_left == 0:
                guesses_left = guessed_before_losing_guesses(guesses_left, secret_word, letters_guessed)
            else:
                warnings_left = guessed_before_losing_warnings(warnings_left, secret_word, letters_guessed)
            continue
        else:
            letters_guessed.add(guessed_letter)
            guesses_left = results(guessed_letter, guesses_left, secret_word, letters_guessed)
        if is_word_guessed(secret_word, letters_guessed):
            return True

def hangman(secret_word, hints_switch = False):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    output_brief_hangman(secret_word)
    guesses_left = GUESSES_AT_START
    warnings_left = WARNINGS_AT_START
    letters_guessed = set()
    winning = main_match_win_or_lose(guesses_left, letters_guessed, secret_word, warnings_left, hints_switch)
    end_of_the_game(winning, guesses_left, secret_word)


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    #Two lists above are needed to delete  space gaps in my_word
    #Then they are used to compare lengths of my_word without space gaps and then compare every symbols
    if len(my_word) != len(other_word):
        return False
    for letter_index in range(0, len(my_word)):
        if my_word[letter_index] != LOWER_BAR and my_word[letter_index] != other_word[letter_index]:
            return False
        #Code below is needed for not showing words, if they have same letters and length,
        #but my_word has any letter and other_word has two same letters as letter in my_word
        #For example, function doesn't show word 'apple' if my_word is 'a_ ple'
        if my_word[letter_index] == LOWER_BAR:
            #Counting number of every letter in both words and comparing them
            letter_occurrence_my_word = my_word.count(other_word[letter_index])
            letter_occurrence_other_word = other_word.count(other_word[letter_index])
            if letter_occurrence_my_word != letter_occurrence_other_word and letter_occurrence_my_word != 0:
                return False
    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    hint_list = []
    my_word = my_word.replace(' ', '')
    for other_word in wordlist:
        if match_with_gaps(my_word, other_word):
            hint_list.append(other_word)
    if hint_list == []:
        print("No matches found")
    else:
        print("Possible word matches are:", ' '.join(hint_list))


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    hangman(secret_word, hints_switch = True)


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
