def usernameCheck(username):
    if len(username)<4 or len(username)>15:
        return 2

    for ch in username:
        if ch!='_' and ch.isalnum()==False:
            return 3

    return 1

def passwordCheck(password):
    if len(password)<6 or len(password)>30:
        return 2

    letter = False
    digit = False

    for ch in password:
        if ch.isalpha():
            letter = True
        if ch.isdigit():
            digit = True

    if letter and digit:
        return 1
    return 3