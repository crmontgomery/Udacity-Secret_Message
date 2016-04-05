import os
import random
import shutil

class Cryptograph(object):
    #Base class for all encoding and decoding
    pass
        
    #constant: alphabet based on the images available to create a message
    ALPHABET = ['a','b','c','d','e','f','g','h','i',
                'j','k','l','m','n','o','p','q','r',
                's','t','u','v','w','x','y','z','.',
                ' ']

    PROGRAM_DIR = os.getcwd() + '\\' #program directory
    ALPHABET_DIR = PROGRAM_DIR + 'alphabet\\' #alphabet source
    MESSAGES_DIR = PROGRAM_DIR + 'messages\\' #location where messages are stored

    #SHOULD FIX: Empty global to store the users message before encoding
    secret_list = []

    #seed used as a key for decrypting the message correctly every time.
    #TODO allow user defined key
    def message_seed(self):
        return 0.2978

    #method used to scramble or descramble a message
    #http://stackoverflow.com/questions/9072955/random-shuffle-randomness
    def scramble_message(self, secret_directory, message, code_form):
        scrambled_message = message
        #shuffles the message based on a user-defined seed
        random.shuffle(scrambled_message, self.message_seed)
    
        new_letter_num = 0
        for letter in scrambled_message:
            if code_form == 'encode':
                os.rename(secret_directory + '\\' + str(letter) + '.jpg', secret_directory + '\\_' + str(new_letter_num) + '.jpg')
            elif code_form == 'decode':
                os.rename(secret_directory + '\\_' + str(new_letter_num) + '.jpg', secret_directory + '\\' + str(letter) + '.jpg')
            new_letter_num += 1

    def encode(self, secret_directory):
        for index, letter_num in enumerate(self.secret_list):
            self.secret_list[index] = index

        scrambled_message = self.secret_list
        self.scramble_message(secret_directory, scrambled_message, 'encode')

    #http://stackoverflow.com/questions/4967580/how-to-get-the-size-of-a-string-in-python    
    def decode(self, secret_directory):
        message_contents = os.listdir(secret_directory)
        message_length = len(message_contents)
        message_numbers = []

        new_number = 0
        for i in xrange(message_length):
            message_numbers.append(new_number)
            new_number += 1

        scrambled_message = message_numbers
        self.scramble_message(secret_directory, scrambled_message, 'decode')

    #creates a list out of the users message
    #http://stackoverflow.com/questions/10610158/how-do-i-convert-string-characters-into-a-list
    def create_message_list(self, message):
        return list(message.lower())

    #change letters to numbers
    def convert_to_numbers(self, messageList):
        for message in messageList:
            for index, letter in enumerate(self.ALPHABET):
                if message == letter:
                    self.secret_list.append(index)
                    break

    #change numbers to letters
    def convert_to_letters(self, messageList):
        for message in messageList:
            for index, letter in enumerate(self.ALPHABET):
                if message == letter:
                    self.secret_list.append(letter)
                    break

    #copies the letter from the alphabet folder
    #into the new message folder
    def create_message(self, secret_directory):
        letter_num = 0
        for letter in self.secret_list:
            shutil.copy2(self.ALPHABET_DIR + str(letter) + '.jpg', secret_directory + '\\' + str(letter_num) + '.jpg')
            letter_num += 1

    #verifies that the directory is empty
    #this allows for the letters of the message to be copied over
    def is_dir_empty(self, directory):
        if os.listdir(directory):
            print 'is not empty, do not add message'
        else:
            print 'is empty, add message'

   
