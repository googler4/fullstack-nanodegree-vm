from ..webapp import database as db
from ..models.mixins import BaseEntityMixin
from sqlalchemy import Unicode, DateTime, Boolean


class User(BaseEntityMixin, db.Model):
    """
    Underly model for all objects in the store
    """
    # __tablename__ = 'user'
    # __bind_key__ = Constants.HARRIER_BIND_KEY

    """

    username = Column(Unicode(100), nullable=False)
    headline = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)

    primary_key = db.Column(Unicode(256), nullable=False)
    url = db.Column(Unicode(2042), nullable=False)

    thumbnail = db.Column(Unicode(2042))

    active = Column(Boolean, default=False)
    """
    # price = db.Column(db.Integer, nullable=True)
    name = db.Column(Unicode(2042), nullable=False)
    image_url = db.Column(Unicode(256), nullable=True)
    email = db.Column(Unicode(256), nullable=True)
    token = db.Column(Unicode(256), nullable=True)
    authenticated = db.Column(Boolean, default=True)
    # images = db.relationship("ItemImage")
    

    # submitted_date_time = db.Column(DateTime(timezone=True), nullable=False)
    # updated_date_time = db.Column(DateTime(timezone=True), nullable=False)
    

    @staticmethod
    def add(name, image_url, email):
        return User(name=name, image_url=image_url, email=email)

    def insert(self):
        db.session.add(self)
        self.save()
        return self.id

    def save(self):
        db.session.commit()

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False