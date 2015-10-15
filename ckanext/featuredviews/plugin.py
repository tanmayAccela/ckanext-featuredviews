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
        if model.repo.are_tables_created()  and not db.civicdata_featured_table.exists():
            db.civicdata_featured_table.create()

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'civicdata_featured')

    def get_actions(self):
        actions_dict = {
            'civicdata_featured_create': actions.civicdata_featured_create,
            'civicdata_featured_show': actions.civicdata_featured_show,
            'civicdata_featured_upsert': actions.civicdata_featured_upsert
        }
        return actions_dict

    def get_helpers(self):
        helpers = {
            'get_civicdata_featured_view': _get_civicdata_featured_view,
            'get_canonical_resource_view': _get_canonical_view,
            'get_organizationpage_resource_views': _get_organizationpage_views
        }
        return helpers

def _get_civicdata_featured_view(resource_view_id):
    if not resource_view_id:
        return None

    civicdata_featured = db.Civicdata_Featured.get(resource_view_id=resource_view_id)

    return civicdata_featured

def _get_canonical_view(package_id):
    canonical = db.Civicdata_Featured.find(package_id=package_id, canonical=True).first()

    if not canonical:
        return None

    resource_view = md.resource_view_dictize(
        model.ResourceView.get(canonical.resource_view_id), {'model': model}
    )
    resource = md.resource_dictize(
        model.Resource.get(resource_view['resource_id']), {'model': model}
    )

    return {'resource': resource, 'resource_view': resource_view}

def _get_organizationpage_views():
    organizationpage_view_ids = []
    organizationpage_views = []
    # list out all the resource ID whose is featured with package IDs in the organization
    try:
        resp = c.page.items

        if len(resp)>0 and resp[0].has_key('id'):
            for items in resp:
                pkg_id = items['id']
                for view in db.Civicdata_Featured.find(organizationpage=True, package_id=pkg_id).all():
                    organizationpage_view_ids.append(view.resource_view_id)

            resource_views = model.Session.query(model.ResourceView).filter(model.ResourceView.id.in_(organizationpage_view_ids)).all()

            for view in resource_views:
                resource_view = md.resource_view_dictize(view, {'model': model})
                resource_obj = model.Resource.get(resource_view['resource_id'])
                resource = md.resource_dictize(resource_obj, {'model': model})

                organizationpage_views.append({
                    'resource_view': resource_view,
                    'resource': resource,
                    'package': md.package_dictize(resource_obj.package, {'model':model})
                })


    except Exception, ex:
        print '\nDEBUG: '+str(ex)

    return organizationpage_views
