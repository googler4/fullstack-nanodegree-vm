from ..webapp import database as db
from ..models.mixins import AnATTR
from sqlalchemy import Unicode, DateTime, Boolean, ForeignKey
from sqlalchemy_utils import UUIDType


class ItemAttribute(AnATTR, db.Model):
    """
    A model for attr attached to objects
    """
    # __tablename__ = 'item_attributes'

    """
    attribute = db.Column(Unicode(256))
    attr_id = Column(UUIDType, default=uuid4)
    value = db.Column(Unicode(256))
    active = Column(Boolean, default=False)
    """

    item_id = db.Column(UUIDType, ForeignKey('items.id'))
    attr_id = db.Column(UUIDType, ForeignKey('attributemaps.id'))

    # submitted_date_time = db.Column(DateTime(timezone=True), nullable=False)
    # updated_date_time = db.Column(DateTime(timezone=True), nullable=False)

    @staticmethod
    def add(item_id, attr_id, attribute, value, active):
        return ItemAttribute(item_id=item_id, attribute=attribute, value=value, active=active, attr_id=attr_id)

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