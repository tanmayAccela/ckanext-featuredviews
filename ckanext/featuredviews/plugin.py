import db
import actions
import ckan.model as model
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.dictization.model_dictize as md
from ckan.common import c, g

from ckan.lib.dictization import table_dictize

class FeaturedviewsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IConfigurable, inherit=True)
    
    # IConfigurable
    def configure(self, config):
        if not db.featured_table.exists():
            db.featured_table.create()

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'featured')

    def get_actions(self):
        actions_dict = {
            'featured_create': actions.featured_create,
            'featured_show': actions.featured_show,
            'featured_upsert': actions.featured_upsert
        }
        return actions_dict

    def get_helpers(self):
        helpers = {
            'get_featured_view': _get_featured_view,
            'get_canonical_resource_view': _get_canonical_view,
            'get_homepage_resource_views': _get_homepage_views
        }
        return helpers

def _get_featured_view(resource_view_id):
    if not resource_view_id:
        return None

    featured = db.Featured.get(resource_view_id=resource_view_id)

    return featured

def _get_canonical_view(package_id):
    canonical = db.Featured.find(package_id=package_id, canonical=True).first()

    if not canonical:
        return None

    resource_view = md.resource_view_dictize(
        model.ResourceView.get(canonical.resource_view_id), {'model': model}
    )
    resource = md.resource_dictize(
        model.Resource.get(resource_view['resource_id']), {'model': model}
    )

    return {'resource': resource, 'resource_view': resource_view}

def _get_homepage_views():
    print str(c)
    print str(g)
    homepage_view_ids = [
        view.resource_view_id for view in db.Featured.find(homepage=True).all()
    ]

    resource_views = model.Session.query(model.ResourceView).filter(
        model.ResourceView.id.in_(homepage_view_ids)
    ).all()

    homepage_views = []
    for view in resource_views:
        resource_view = md.resource_view_dictize(view, {'model': model})
        resource_obj = model.Resource.get(resource_view['resource_id'])
        resource = md.resource_dictize(resource_obj, {'model': model})

        homepage_views.append({
            'resource_view': resource_view,
            'resource': resource,
            'package': md.package_dictize(resource_obj.package, {'model':model})
        })

    return homepage_views

"""
def _get_organizationpage_views():
    organizationpage_view_ids = [
        view.resource_view_id for view in db.Featured.find(organizationpage=True).all()
    ]

    resource_views = model.Session.query(model.ResourceView).filter(
        model.ResourceView.id.in_(organizationpage_view_ids)
    ).all()

    organizationpage_views = []
    for view in resource_views:
        resource_view = md.resource_view_dictize(view, {'model': model})
        resource_obj = model.Resource.get(resource_view['resource_id'])
        resource = md.resource_dictize(resource_obj, {'model': model})

        organizationpage_views.append({
            'resource_view': resource_view,
            'resource': resource,
            'package': md.package_dictize(resource_obj.package, {'model':model})
        })

    return organizationpage_views
"""