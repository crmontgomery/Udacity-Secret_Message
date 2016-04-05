import os
import random
import shutil
import sys
#Quick proof of concept

#alphabet constant based on the images available to create a message
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
def message_seed():
    return 0.2978

#method used to scramble or descramble a message
#http://stackoverflow.com/questions/9072955/random-shuffle-randomness
def scramble_message(secret_directory, message, code_form):
    scrambled_message = message
    #shuffles the message based on a user-defined seed
    random.shuffle(scrambled_message, message_seed)
    
    new_letter_num = 0
    for letter in scrambled_message:
        if code_form == 'encode':
            os.rename(secret_directory + '\\' + str(letter) + '.jpg', secret_directory + '\\_' + str(new_letter_num) + '.jpg')
        elif code_form == 'decode':
            os.rename(secret_directory + '\\_' + str(new_letter_num) + '.jpg', secret_directory + '\\' + str(letter) + '.jpg')
        new_letter_num += 1

def encode(secret_directory):
    for index, letter_num in enumerate(secret_list):
        secret_list[index] = index

    scrambled_message = secret_list
    scramble_message(secret_directory, scrambled_message, 'encode')

#http://stackoverflow.com/questions/4967580/how-to-get-the-size-of-a-string-in-python    
def decode(secret_directory):
    message_contents = os.listdir(secret_directory)
    message_length = len(message_contents)
    message_numbers = []

    new_number = 0
    for i in xrange(message_length):
        message_numbers.append(new_number)
        new_number += 1

    scrambled_message = message_numbers
    scramble_message(secret_directory, scrambled_message, 'decode')

#creates a list out of the users message
#http://stackoverflow.com/questions/10610158/how-do-i-convert-string-characters-into-a-list
def create_message_list(message):
    return list(message.lower())

#change letters to numbers
def convert_to_numbers(messageList):
    for message in messageList:
        for index, letter in enumerate(ALPHABET):
            if message == letter:
                secret_list.append(index)
                break

#change numbers to letters
def convert_to_letters(messageList):
    for message in messageList:
        for index, letter in enumerate(ALPHABET):
            if message == letter:
                secret_list.append(letter)
                break

#copies the letter from the alphabet folder
#into the new message folder
def create_message(secret_directory):
    letter_num = 0
    for letter in secret_list:
        shutil.copy2(ALPHABET_DIR + str(letter) + '.jpg', secret_directory + '\\' + str(letter_num) + '.jpg')
        letter_num += 1

#verifies that the directory is empty
#this allows for the letters of the message to be copied over
def is_dir_empty(directory):
    if os.listdir(directory):
        print 'is not empty, do not add message'
    else:
        print 'is empty, add message'

#################
# PROGRAM START #
#################

#prompt user: 1-encode message, 2=decode message, 0-quit
while True:
    try:
        user_choice = int(raw_input('What would you like to do?\n1-Encode Message. 2-Decode Message. 0-Quit --> '))
            #quit the program
        if user_choice == 0:
            print 'Good Bye'
            sys.exit()

        #encode Message
        elif user_choice == 1:
            new_directory_created = False
            message_complete = False
            new_secret_directory = ''

            while new_directory_created == False:
                #prompt user for message title
                message_title = raw_input('What would you like the title to be? ')

                #verify title doesnt already exist
                #http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
                if not os.path.exists(MESSAGES_DIR + message_title):
                    os.makedirs(MESSAGES_DIR + message_title)
                    new_secret_directory = MESSAGES_DIR + message_title
                    new_directory_created = True
                else:
                    #title already exists
                    print 'Sorry, that message already exists. \nPlease choose another. \n\n'

            #prompt user for message body
            while message_complete == False:
                message_body = raw_input('What would you like your message to say? \n')

                if message_body != '':
                    #split the message into a list
                    message = create_message_list(message_body)
                    #convert message to numbers
                    message = convert_to_numbers(message)
                    #copy message to new folder (title)
                    create_message(new_secret_directory)
                    #encode the message
                    encode(new_secret_directory)
                    print 'Your message is complete.'
                    secret_list = []
                    message_complete = True
                else: 
                    print 'Your message was left blank. Please try again.'

        #decode message
        # TODO loop the decode option to select another message
        elif user_choice == 2:
            #prompt the user with a dir listing and choice
            #TODO ensure the directory is not empty
            message_listing = os.listdir(MESSAGES_DIR)
            list_num = 0
            for message in message_listing:
                print str(list_num) + ' - ' + message
                list_num += 1
            
            try:
                message_selection = int(raw_input('\nPlease select a message from the list: '))
                message_contents = ''
                message_directory = ''
                ready_to_decode = False
                #message_split = []

                #prompt the user for a seed value
                #inform user if seed is incorrect message is permantly destroyed (maybe create fallback?)
                for index, message in enumerate(message_listing):
                    if int(index) == message_selection:
                        message_contents = os.listdir(MESSAGES_DIR + message)
                        message_directory = MESSAGES_DIR + message

                #upon selection verify message is not already decoded
                for letter in message_contents:
                    if letter.startswith('_'):
                        ready_to_decode = True

                if ready_to_decode: 
                    decode(message_directory)
                else:
                    print 'There is an error with the message. Either it has already been decoded or has been tampered with. Please select a new message.'
                
            except ValueError:
                print 'Decode: That is not an integer. Please select a valid option number.'
                
        else:
            print 'That is not an option.'

    except ValueError:
        print 'Primary: That is not an integer. Please select a valid option number.'
