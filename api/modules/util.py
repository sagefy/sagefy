"""
Short, one-off methods that could potentially be reused anywhere.
"""

import random
import string


def uniqid(length=8):
    """
    Generates a unique string with 8 characters.
    http://stackoverflow.com/a/2257449
    """
    return ''.join(
        random.choice(string.ascii_lowercase + string.digits)
        for i in range(length)
    )
