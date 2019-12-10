import enum


class Format(enum.Enum):
    free_text = 1
    yes_no = 2
    numeric = 3
    column_name = 4
    item_in_list = 5
    press_enter = 6


class InputError(Exception):

    def __init__(self, msg): 
        self.msg = msg


def get_text_input(prompt, input_format, message='\n', validation=[]):
    print(message)

    while True:
        try:
            text_input = input(f'{prompt}\n')

            if input_format == 2:
                if text_input != 'yes' and text_input != 'no':
                    raise InputError("Please enter 'yes' or 'no'.")
                return text_input == 'yes'

            elif input_format == 3:
                try:
                    text_input = float(text_input)
                except:
                    raise InputError("Only numeric input accepted.")

            elif input_format == 4 and text_input not in validation:
                    raise InputError(f"Input must be one of the following: \n{validation}.")
                
            elif input_format == 5:
                if  text_input not in validation.keys():
                    raise InputError(f"Input must be one of the following: \n{validation.keys()}.")
                else:
                    return validation[text_input]

            return text_input
        
        except InputError as err:
            print(err.msg)
            