from ..webapp import database as db
from ..models.mixins import BaseEntityMixin
from sqlalchemy import Unicode, DateTime, Boolean, ForeignKey
from sqlalchemy_utils import UUIDType


class ItemImage(BaseEntityMixin, db.Model):
    """
    Underly class for all objects in the store
    """
    # __tablename__ = 'item_attributes'

    """
    attribute = db.Column(Unicode(256))
    attr_id = Column(UUIDType, default=uuid4)
    value = db.Column(Unicode(256))
    active = Column(Boolean, default=False)
    """
    url = db.Column(Unicode(2042))

    item_id = db.Column(UUIDType, ForeignKey('items.id'))
    # attr_id = db.Column(UUIDType, ForeignKey('attributemaps.id'))

    # submitted_date_time = db.Column(DateTime(timezone=True), nullable=False)
    # updated_date_time = db.Column(DateTime(timezone=True), nullable=False)

    @staticmethod
    def add(item_id, url):
        return ItemImage(item_id=item_id, url=url)

    def insert(self):
        db.session.add(self)
        self.save()
        return self.id

    def save(self):
        db.session.commit()


    # def add_item_attr_save(item_id, attribute, value, active):
    #     item_attrs = ItemAttribute(item_id=item_id, attribute=attribute, value=value, active=active)
    #     db.session.add(item_attrs)
    #     item_attrs.save()
    #     return item_attrs.id