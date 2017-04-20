from ..webapp import database as db
from ..models.mixins import AnATTR
from sqlalchemy import Unicode, DateTime, Boolean, ForeignKey
from sqlalchemy_utils import UUIDType


class Group(AnATTR, db.Model):
    """
    Underly class for all objects in the store
    """
    # __tablename__ = 'item_attributes'

    """
    attribute = db.Column(Unicode(256))
    value = db.Column(Unicode(256))
    active = Column(Boolean, default=False)
    """
  
    parent_id = db.Column(UUIDType, ForeignKey('groups.id'))
    children = db.relationship("Group")
    group_maps = db.relationship("GroupMap")

    # submitted_date_time = db.Column(DateTime(timezone=True), nullable=False)
    # updated_date_time = db.Column(DateTime(timezone=True), nullable=False)

    @staticmethod
    def add(parent_id, attribute, value, active):
        return Group(parent_id=parent_id, attribute=attribute, value=value, active=active)

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