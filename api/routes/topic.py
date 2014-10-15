from flask import Blueprint, jsonify, request
from models.topic import Topic
from models.post import Post
from flask.ext.login import current_user

topic = Blueprint('topic', __name__, url_prefix='/api/topics')


@topic.route('/', methods=['GET'])
def list_topics():
    """
    Search the topics.
    Takes query string, filters, sort.
    Paginates.
    """
    pass


@topic.route('/<topic_id>/', methods=['GET'])
def get_topic(topic_id):
    """
    Get topic information.
    """
    pass


@topic.route('/', methods=['POST'])
def create_topic():
    """
    Search the topics.
    Takes query string, filters, sort.
    Paginates.
    """
    pass


@topic.route('/<topic_id>/', methods=['PUT', 'PATCH'])
def update_topic(topic_id):
    """
    Update the topic. Only the name can be changed by original author.
    """
    pass


@topic.route('/<topic_id>/posts/', methods=['GET'])
def get_posts(topic_id):
    """
    Get a reverse chronological listing of posts for given topic.
    Paginates.
    """
    pass


@topic.route('/<topic_id>/posts/', methods=['POST'])
def create_post(topic_id):
    """
    Create a new post on a given topic.
    """
    pass


@topic.route('/<topic_id>/posts/<post_id>/', methods=['PUT', 'PATCH'])
def update_post(topic_id, post_id):
    """
    Update an existing post. Must be one's own post.
    """
    pass
