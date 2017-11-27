from framework.status_codes import status_codes


def test_has_codes():
  """
  Ensure the most common status are available.
  """

  for code in (200, 301, 400, 401, 403, 404, 500):
    assert code in status_codes
