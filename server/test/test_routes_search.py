import pytest

from routes.search import search_route

xfail = pytest.mark.xfail


def test_search():
  """
  Expect to search by query.
  """
  request = {
    'params': {
      'q': 'music',
    },
  }
  code, _ = search_route(request)
  assert code == 200


@xfail
def test_search_sort():
  """
  Expect to sort in search.
  """
  assert False


@xfail
def test_search_paginate():
  """
  Expect to paginate in search.
  """
  assert False


@xfail
def test_search_blank():
  """
  Expect a blank search result.
  """
  assert False


@xfail
def test_sort_created():
  """
  Expect to sort results by created at time.
  """
  assert False


@xfail
def test_sort_modified():
  """
  Expect to sort results by modified time.
  """
  assert False


@xfail
def test_sort_language():
  """
  Expect to filter results by language.
  """
  assert False


@xfail
def test_users():
  """
  Expect to filter results to users.
  """
  assert False


@xfail
def test_user_name():
  """
  Expect to search users by name.
  """
  assert False


@xfail
def test_topic():
  """
  Expect to filter results to topics.
  """
  assert False


@xfail
def test_topic_name():
  """
  Expect to search topics by name.
  """
  assert False


@xfail
def test_topic_entity():
  """
  Expect to filter topics by entity.
  """
  assert False


@xfail
def test_topic_entity_kind():
  """
  Expect to filter topics by entity kind.
  """
  assert False


@xfail
def test_topisession():
  """
  Expect to filter topics by user.
  """
  assert False


@xfail
def test_topic_posts():
  """
  Expect to sort topics by number of posts.
  """
  assert False


@xfail
def test_post():
  """
  Expect to filter results to posts (all kinds).
  """
  assert False


@xfail
def test_post_body():
  """
  Expect to search posts by body.
  """
  assert False


@xfail
def test_post_topic():
  """
  Expect to filter posts by topic.
  """
  assert False


@xfail
def test_post_entity():
  """
  Expect to filter posts by entity.
  """
  assert False


@xfail
def test_post_entity_kind():
  """
  Expect to filter posts by entity kind.
  """
  assert False


@xfail
def test_post_user():
  """
  Expect to filter posts by user.
  """
  assert False


@xfail
def test_proposal():
  """
  Expect to filter to proposals.
  """
  assert False


@xfail
def test_proposal_status():
  """
  Expect to filter proposals by status.
  """
  assert False


@xfail
def test_proposal_action():
  """
  Expect to filter proposals by action.
  """
  assert False


@xfail
def test_vote():
  """
  Expect to filter to votes.
  """
  assert False


@xfail
def test_vote_response():
  """
  Expect to filter votes by response.
  """
  assert False


@xfail
def test_card():
  """
  Expect to filter to cards.
  """
  assert False


@xfail
def test_card_name():
  """
  Expect to search cards by name and contents.
  """
  assert False


@xfail
def test_card_unit():
  """
  Expect to filter cards by unit.
  """
  assert False


@xfail
def test_card_require():
  """
  Expect to filter cards by requires.
  """
  assert False


@xfail
def test_card_required_by():
  """
  Expect to filter cards by required by.
  """
  assert False


@xfail
def test_card_kind():
  """
  Expect to filter cards by kind.
  """
  assert False


@xfail
def test_card_tag():
  """
  Expect to filter cards by tag.
  """
  assert False


@xfail
def test_unit():
  """
  Expect to filter to units.
  """
  assert False


@xfail
def test_unit_name():
  """
  Expect to search units by name and body.
  """
  assert False


@xfail
def test_unit_subject():
  """
  Expect to filter units by subjects.
  """
  assert False


@xfail
def test_unit_requires():
  """
  Expect to filter units by requires.
  """
  assert False


@xfail
def test_unit_required_by():
  """
  Expect to filter units by required by.
  """
  assert False


@xfail
def test_unit_tag():
  """
  Expect to filter units by tag.
  """
  assert False


@xfail
def test_unit_learners():
  """
  Expect to sort units by number of learners.
  """
  assert False


@xfail
def test_subject():
  """
  Expect to filter to subjects.
  """
  assert False


@xfail
def test_subject_name():
  """
  Expect to search subjects by name and body.
  """
  assert False


@xfail
def test_subject_containing():
  """
  Expect to filter subjects by unit containing.
  """
  assert False


@xfail
def test_subject_tag():
  """
  Expect to filter subjects by tag.
  """
  assert False


@xfail
def test_subject_learners():
  """
  Expect to sort subjects by number of learners.
  """
  assert False
