# from modules.model import Model
# from datetime import datetime


# notifications_categories = db.Table(
#     'notifications_categories',
#     db.Column(
#         'notification_id',
#         db.String(64),
#         db.ForeignKey('notifications.id'),
#     ),
#     db.Column(
#         'category_id',
#         db.String(64),
#         db.ForeignKey('categories.id'),
#     ),
# )


# class Notification(db.Model):
#     __tablename__ = 'notifications'

#     id = db.Column(db.String(64), primary_key=True)
#     created = db.Column(db.DateTime, default=datetime.utcnow())
#     user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
#     name = db.Column(db.String(256))
#     body = db.Column(db.Text)
#     read = db.Column(db.Boolean, default=False)

#     categories = db.relationship(
#         'Category',
#         secondary=notifications_categories,
#         lazy='joined'
#     )

#     @staticmethod
#     def get_user_notifications(**kwargs):
#         """
#         Takes a set of kwargs.
#         user_id: ID of the user.
#         limit: Number of notifications per page.
#         offset: Where to start the number of notifications.
#         TODO: categories: Limit to the categories selected.

#         Returns a matching list of notifications.
#         """

#         assert kwargs.get('user_id'), {
#             "name": "user_id",
#             "message": "You must be logged in to read notifications.",
#         }

#         query = Notification.query.filter_by(user_id=kwargs.get('user_id'))

#         if kwargs.get('read') is not None:
#             query.filter_by(read=kwargs.get('read'))

#         if kwargs.get('categories'):
#             # http://stackoverflow.com/a/6543089
#             query.join(Notification.categories)
#             query.filter(Category.name.in_(kwargs.get('categories')))

#         if kwargs.get('limit'):
#             query.limit(kwargs.get('limit'))

#         if kwargs.get('offset'):
#             query.offset(kwargs.get('offset'))

#         return query.all()

#     @staticmethod
#     def get_by_id(id):
#         """
#         Takes an ID and returns a notification.
#         """

#         # TODO: Redis cache
#         return Notification.query.filter_by(id=id).one()

#     def mark_as_read(self):
#         """
#         Marks the notification as read
#         """

#         self.read = True
#         self.commit()
#         return self

#     def commit(self):
#         """
#         Commits notification to the database.
#         """

#         # TODO: Clear Redis caches

#         try:
#             db.session.add(self)
#             db.session.commit()
#             return self
#         except:
#             db.session.rollback()
#             return False
