from modules import util
import string


def test_uniqid():
    # Expect the length of the ID to be 16
    assert len(util.uniqid()) is 16

    # Expect the length of the ID to be changeable
    assert len(util.uniqid(length=8)) is 8

    # Expect the ID to only have numbers and lowercase letters
    uid = util.uniqid()
    for c in uid:
        assert c in string.ascii_lowercase + string.digits
