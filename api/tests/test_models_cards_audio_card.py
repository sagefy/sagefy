import pytest

xfail = pytest.mark.xfail


@xfail
def test_audio_site(app):
    """
    Expect an audio card to require site.
    """

    assert False


@xfail
def test_audio_audio_id(app):
    """
    Expect an audio card to require audio_id.
    """

    assert False
