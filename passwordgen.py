import random
import string


def catchType(message, err_msg):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print(err_msg)
            pass


def generatePass(n, s, u, len=True):
    if len:
        leng = catchType("Enter Password Length: ", "Please Enter A Digit")
    else:
        leng = 20
    choice = string.ascii_lowercase
    if n:
        choice += str(string.digits)
    if s:
        choice += str("!@#$%^&*()_+}{:'[]=-")
    if u:
        choice += str(string.ascii_uppercase)
    password = ''.join(random.SystemRandom().choice(choice) for _ in range(leng))
    print("Password Generated Succesfully")
    return password


def main(num=False, sym=False, upper=False):
    print('-------------------------------\n'
          '|Password Manager + Generator |\n'
          '-------------------------------\n'
          '|0: Start Password Generation |\n'
          '------------------------------\n'
          f'2: Numbers:   {str(num).ljust(5)} |\n'
          f'3: Symbols:   {str(sym).ljust(5)} |\n'
          f'4: Uppercase: {str(upper).ljust(5)} |\n'
          '---------------------\n'
          )
    select = catchType("Enter A Digit: ", "Please Enter A Digit")
    if select == 0:
        return generatePass(num, sym, upper)
    elif select == 2:
        num = not num
        return main(num, sym, upper)
    elif select == 3:
        sym = not sym
        return main(num, sym, upper)
    elif select == 4:
        upper = not upper
        return main(num, sym, upper)