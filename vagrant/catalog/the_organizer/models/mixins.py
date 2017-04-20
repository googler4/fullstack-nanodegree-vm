
from inflect import engine
from sqlalchemy import Boolean, Column, Unicode, UnicodeText
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates
from sqlalchemy_utils import EmailType, PasswordType, Timestamp, UUIDType
from uuid import uuid4

PASSWORD_ENCRYPTION_SCHEMES = ['bcrypt']

inflector = engine()


class BaseEntityMixin(Timestamp):
    """The base model for every modeled entity."""

    @declared_attr
    def __tablename__(cls):
        return inflector.plural(cls.__name__.lower())

    id = Column(UUIDType, default=uuid4, primary_key=True)

    def __repr__(self):
        return '<{entity_type}-{id}>'.format(
            entity_type=self.__class__, id=self.id)



class AnObject(BaseEntityMixin):
    """Anything with text and meta.

    Note: At the time, I'm not enforcing any authorship norms. Those
    are to be defined on their respective ORM classes.
    """
    title = Column(Unicode(100), nullable=False)
    headline = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)

    primary_key = Column(Unicode(256), nullable=False)
    url = Column(Unicode(2042), nullable=False)
    thumbnail = Column(Unicode(2042))

    active = Column(Boolean, default=False)

    @validates('title')
    def validate_title(self, key, title):
        """Keep titles from getting too long."""
        assert len(title) >= 4 or len(
            title) <= 256, 'Must be 4 to 256 characters long.'
        return title

class AnATTR(BaseEntityMixin):
    attribute = Column(Unicode(256))
    value = Column(UnicodeText)
    active = Column(Boolean, default=False)
