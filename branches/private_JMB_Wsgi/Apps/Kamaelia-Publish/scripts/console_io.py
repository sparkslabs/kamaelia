def prompt_yesno(text):
    """
    Just a generic function to determine if the user wants to continue or not.
    Will repeat if input is unrecognizable.
    """
    user_input = raw_input(text)
    
    if user_input[0] == 'y' or user_input[0] == 'Y':
        return True
    elif user_input[0] == 'n' or user_input[0] == 'N':
        return False
    else:
        print 'Unrecognizable input.  Please try again'
        return prompt_yesno(text)
    
def prompt_corrupt(corrupt):
    print 'The following files appear to be corrupted: \n', corrupt, \
        '\n There may be more corrupted files.'
    if not prompt_yesno('Would you like to continue anyway? [y/n]'):
        print "Halting!"
        sys.exit(1)
