# Simple functions to make the code more readable

def is_gmail(word):
    if word.upper() == "GMAIL":
        return True
    else:
        return False


def is_sogo(word):
    if word.upper() == "SOGO":
        return True
    else:
        return False


def is_live(word):
    if word.upper() == "LIVE" or word.upper() == "OUTLOOK" or word.upper() == "HOTMAIL":
        return True
    else:
        return False


def is_hena(word):
    if word.upper() == "HENALLUX":
        return True
    else:
        return False