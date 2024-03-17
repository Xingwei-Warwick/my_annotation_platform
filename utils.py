import random
import string


def text_preprocess(text):
    if type(text) == list:
        text = '\n\n'.join(text)
    elif type(text) != str:
        text = str(text)
    text = text.replace('$', '\$')
    return text

def get_random_string(length=12):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


