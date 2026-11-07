import pickle

def save_words_to_file(words, filename):
    with open(filename, 'wb') as file:
        pickle.dump(words, file)

words_to_save = ['hello', 'world', 'python', 'coding',
                 'study', 'apple', 'ball', 'cat',
                 'dog', 'elephant', 'fish', 'gun', 'hat']
save_words_to_file(words_to_save, 'words_file.dat')
