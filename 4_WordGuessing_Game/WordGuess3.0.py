import random
import pickle

def load_words_from_file(filename):
    with open(filename, 'rb') as file:
        words = pickle.load(file)
    return words

def display_word(word, revealed_letters):
    return ''.join([char if char in revealed_letters else '_' for char in word])

def initial_reveal(word):
    revealed_letters = ['_' if char.isalpha() and random.random() < 0.5 else char for char in word]
    return revealed_letters

def update_revealed_letters(hidden_word, revealed_letters, user_input):
    for index, char in enumerate(hidden_word):
        if char.isalpha() and user_input == char:
            revealed_letters[index] = char

def guess(hidden_word):
    revealed_letters = initial_reveal(hidden_word)
    user_input = []
    max_tries = len(hidden_word) + 2

    tries = 0

    while tries < max_tries:
        coded_word = display_word(hidden_word, revealed_letters)
        print(f"Coded Word is: '{coded_word}', Guess in {max_tries - tries} tries")

        user_input1 = input("Enter a letter: ").lower()

        if not user_input1:
            print("Please enter something.")
        elif len(user_input1) > 1:
            print("Please enter only one letter at a time.")
        elif user_input1 in user_input:
            print("You've already entered that letter. Try something else.")
            print(f"Alphabets already used: '{' '.join(user_input)}'")
        else:
            user_input.append(user_input1)
            user_input.sort()

            if user_input1 in hidden_word:
                update_revealed_letters(hidden_word, revealed_letters, user_input1)
                print("You guessed right!")
            else:
                tries += 1
                print(f"Sorry, wrong guess. {max_tries - tries} tries left.")

            print(f"Alphabets already used: '{' '.join(user_input)}'")

            if all(char.isalpha() and char != '_' for char in revealed_letters):
                print(f"Congratulations! You guessed the word. The word was '{hidden_word}' in {tries + 1} tries.\n")
                break

    if tries == max_tries:
        print(f"Sorry, you've exhausted all tries. The correct answer was: '{hidden_word}'")

def main():
    loaded_words = load_words_from_file('words_file.dat')
    guess(loaded_words[random.randint(0, len(loaded_words))])

    while True:
        ch=input("Do you want to play again (Y/N)")
        if ch in "Yy":
            main()
        elif ch in "Nn":
            break
        else:
            print("Wrong Choice !!")

if __name__ == "__main__":
    main()
