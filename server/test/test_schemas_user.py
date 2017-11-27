from schemas.user import encrypt_password


def test_encrypt_password():
  assert encrypt_password('abcd').startswith('$2a$')
  assert encrypt_password('$2a$a') == '$2a$a'
  assert encrypt_password(None) is None
