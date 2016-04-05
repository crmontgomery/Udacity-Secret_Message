import os
import sys
from cryptograph import Cryptograph

cryptograph = Cryptograph()

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
                if not os.path.exists(cryptograph.MESSAGES_DIR + message_title):
                    os.makedirs(cryptograph.MESSAGES_DIR + message_title)
                    new_secret_directory = cryptograph.MESSAGES_DIR + message_title
                    new_directory_created = True
                else:
                    #title already exists
                    print 'Sorry, that message already exists. \nPlease choose another. \n\n'

            #prompt user for message body
            while message_complete == False:
                message_body = raw_input('What would you like your message to say? \n')

                if message_body != '':
                    #split the message into a list
                    message = cryptograph.create_message_list(message_body)
                    #convert message to numbers
                    message = cryptograph.convert_to_numbers(message)
                    #copy message to new folder (title)
                    cryptograph.create_message(new_secret_directory)
                    #encode the message
                    cryptograph.encode(new_secret_directory)
                    print 'Your message is complete.'
                    cryptograph.secret_list = []
                    message_complete = True
                else: 
                    print 'Your message was left blank. Please try again.'

        #decode message
        # TODO loop the decode option to select another message
        elif user_choice == 2:
            #prompt the user with a dir listing and choice
            #TODO ensure the directory is not empty
            message_listing = os.listdir(cryptograph.MESSAGES_DIR)
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
                        message_contents = os.listdir(cryptograph.MESSAGES_DIR + message)
                        message_directory = cryptograph.MESSAGES_DIR + message

                #upon selection verify message is not already decoded
                for letter in message_contents:
                    if letter.startswith('_'):
                        ready_to_decode = True

                if ready_to_decode: 
                    cryptograph.decode(message_directory)
                else:
                    print 'There is an error with the message. Either it has already been decoded or has been tampered with. Please select a new message.'
                
            except ValueError:
                print 'Decode: That is not an integer. Please select a valid option number.'
                
        else:
            print 'That is not an option.'

    except ValueError:
        print 'Primary: That is not an integer. Please select a valid option number.'
