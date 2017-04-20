from ..webapp import database as db
from ..models.mixins import AnObject
from sqlalchemy import Unicode, DateTime, Boolean


class Item(AnObject, db.Model):
    """
    Underly model for all objects in the store
    """
    # __tablename__ = 'item'
    # __bind_key__ = Constants.HARRIER_BIND_KEY

    """
    title = Column(Unicode(100), nullable=False)
    headline = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)

    primary_key = db.Column(Unicode(256), nullable=False)
    url = db.Column(Unicode(2042), nullable=False)

    thumbnail = db.Column(Unicode(2042))

    active = Column(Boolean, default=False)
    """
    # price = db.Column(db.Integer, nullable=True)
    amazon_url = db.Column(Unicode(2042), nullable=True)
    attributes = db.relationship("ItemAttribute")
    group_maps = db.relationship("GroupMap")

    images = db.relationship("ItemImage")
    

    # submitted_date_time = db.Column(DateTime(timezone=True), nullable=False)
    # updated_date_time = db.Column(DateTime(timezone=True), nullable=False)

    @staticmethod
    def add(title, headline, description, primary_key, url, amazon_url,thumbnail):
        return Item(title=title, headline=headline, description=description, primary_key=primary_key, url=url, amazon_url=amazon_url, thumbnail=thumbnail)

    def insert(self):
        db.session.add(self)
        self.save()
        return self.id

    def save(self):
        db.session.commit()