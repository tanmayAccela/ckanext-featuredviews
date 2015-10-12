import ckan.model as model

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from ckan.model.meta import metadata,  mapper, Session
from ckan.model.types import make_uuid

civicdata_featured_table = Table('civicdata_featured', metadata,
    Column('resource_view_id', types.UnicodeText, primary_key=True),
    Column('package_id', types.UnicodeText),
    Column('canonical', types.Boolean),
    Column('organizationpage', types.Boolean)
)

class Civicdata_Featured(model.DomainObject):
    @classmethod
    def get(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).first()

    @classmethod
    def find(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw)

model.meta.mapper(Civicdata_Featured, civicdata_featured_table)
