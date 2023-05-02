# Desenvolvimento de Aplicativos - Exercício 1
# Caio Shishito Abe - 148131

class Ex1:
    def start(self):
        words = self.make_word_dict()
        for word in words:
            index = list(words).index(word) + 1  # get the word index
            for i in range(index, len(words)):
                word2 = list(words)[i]           # word to compare

                if len(word) == len(word2):
                    for rotate_num in range(26): # 26 alphabetic letters
                        new_word = self.rotate_word(word, rotate_num)
                        if new_word == word2:
                            print(word, word2, rotate_num)
                            break

    def rotate_word(self, word, n):
        new_word = ""
        for character in word:
            if (ord(character) >= ord('a')) and (ord(character) <= ord('z')): # lower case
                new_character = (chr(ord(character) + n))

                if ord(new_character) > ord('z'):
                    new_character = chr(ord('a') + (ord(new_character) - ord('z') - 1))

            elif (ord(character) >= ord('A')) and (ord(character) <= ord('Z')): # upper case
                new_character = (chr(ord(character) + n))

                if ord(new_character) > ord('Z'):
                    new_character = chr(ord('A') + (ord(new_character) - ord('Z') - 1))

            new_word += new_character

        return new_word

    def make_word_dict(self):
        with open('word.txt') as textFile:
            words_dict = {}

            for line in textFile:
                words_dict[line.strip()] = 0

            return(words_dict)

Ex1().start()
