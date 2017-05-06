import pytest

xfail = pytest.mark.xfail


@xfail
def test_search(db_conn):
    """
    Expect to search by query.
    """
    assert False


@xfail
def test_search_sort(db_conn, users_table, topics_table,
                     posts_table):
    """
    Expect to sort in search.
    """
    assert False


@xfail
def test_search_paginate(db_conn, users_table, topics_table,
                         posts_table):
    """
    Expect to paginate in search.
    """
    assert False


@xfail
def test_search_blank(db_conn, users_table, topics_table,
                      posts_table):
    """
    Expect a blank search result.
    """
    assert False


@xfail
def test_sort_created(app):
    """
    Expect to sort results by created at time.
    """
    assert False


@xfail
def test_sort_modified(app):
    """
    Expect to sort results by modified time.
    """
    assert False


@xfail
def test_sort_language(app):
    """
    Expect to filter results by language.
    """
    assert False


@xfail
def test_users(app):
    """
    Expect to filter results to users.
    """
    assert False


@xfail
def test_user_name(app):
    """
    Expect to search users by name.
    """
    assert False


@xfail
def test_topic(app):
    """
    Expect to filter results to topics.
    """
    assert False


@xfail
def test_topic_name(app):
    """
    Expect to search topics by name.
    """
    assert False


@xfail
def test_topic_entity(app):
    """
    Expect to filter topics by entity.
    """
    assert False


@xfail
def test_topic_entity_kind(app):
    """
    Expect to filter topics by entity kind.
    """
    assert False


@xfail
def test_topisession(app):
    """
    Expect to filter topics by user.
    """
    assert False


@xfail
def test_topic_posts(app):
    """
    Expect to sort topics by number of posts.
    """
    assert False


@xfail
def test_post(app):
    """
    Expect to filter results to posts (all kinds).
    """
    assert False


@xfail
def test_post_body(app):
    """
    Expect to search posts by body.
    """
    assert False


@xfail
def test_post_topic(app):
    """
    Expect to filter posts by topic.
    """
    assert False


@xfail
def test_post_entity(app):
    """
    Expect to filter posts by entity.
    """
    assert False


@xfail
def test_post_entity_kind(app):
    """
    Expect to filter posts by entity kind.
    """
    assert False


@xfail
def test_post_user(app):
    """
    Expect to filter posts by user.
    """
    assert False


@xfail
def test_proposal(app):
    """
    Expect to filter to proposals.
    """
    assert False


@xfail
def test_proposal_status(app):
    """
    Expect to filter proposals by status.
    """
    assert False


@xfail
def test_proposal_action(app):
    """
    Expect to filter proposals by action.
    """
    assert False


@xfail
def test_vote(app):
    """
    Expect to filter to votes.
    """
    assert False


@xfail
def test_vote_response(app):
    """
    Expect to filter votes by response.
    """
    assert False


@xfail
def test_card(app):
    """
    Expect to filter to cards.
    """
    assert False


@xfail
def test_card_name(app):
    """
    Expect to search cards by name and contents.
    """
    assert False


@xfail
def test_card_unit(app):
    """
    Expect to filter cards by unit.
    """
    assert False


@xfail
def test_card_require(app):
    """
    Expect to filter cards by requires.
    """
    assert False


@xfail
def test_card_required_by(app):
    """
    Expect to filter cards by required by.
    """
    assert False


@xfail
def test_card_kind(app):
    """
    Expect to filter cards by kind.
    """
    assert False


@xfail
def test_card_tag(app):
    """
    Expect to filter cards by tag.
    """
    assert False


@xfail
def test_unit(app):
    """
    Expect to filter to units.
    """
    assert False


@xfail
def test_unit_name(app):
    """
    Expect to search units by name and body.
    """
    assert False


@xfail
def test_unit_subject(app):
    """
    Expect to filter units by subjects.
    """
    assert False


@xfail
def test_unit_requires(app):
    """
    Expect to filter units by requires.
    """
    assert False


@xfail
def test_unit_required_by(app):
    """
    Expect to filter units by required by.
    """
    assert False


@xfail
def test_unit_tag(app):
    """
    Expect to filter units by tag.
    """
    assert False


@xfail
def test_unit_learners(app):
    """
    Expect to sort units by number of learners.
    """
    assert False


@xfail
def test_subject(app):
    """
    Expect to filter to subjects.
    """
    assert False


@xfail
def test_subject_name(app):
    """
    Expect to search subjects by name and body.
    """
    assert False


@xfail
def test_subject_containing(app):
    """
    Expect to filter subjects by unit containing.
    """
    assert False


@xfail
def test_subject_tag(app):
    """
    Expect to filter subjects by tag.
    """
    assert False


@xfail
def test_subject_learners(app):
    """
    Expect to sort subjects by number of learners.
    """
    assert False
