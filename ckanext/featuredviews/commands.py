import ckan.plugins as p
import paste.script
import db
import logging

from ckan.lib.cli import CkanCommand

from ckan import model

log = logging.getLogger(__name__)

class FeaturedCommands(CkanCommand):
    """
    ckanext-featuredviews commands:

    Usage::

        paster featuredviews migrate
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__

    parser = paste.script.command.Command.standard_parser(verbose=True)
    parser.add_option('-c', '--config', dest='config',
        default='development.ini', help='Config file to use.')

    def command(self):
        if not len(self.args):
            print self.__doc__
            return

        cmd = self.args[0]
        self._load_config()

        if cmd == 'migrate':
            self._migrate()
        else:
            print self.__doc__

    def _migrate(self):
        if not db.civicdata_featured_table.exists():
            db.civicdata_featured_table.create()
            log.info('Civicdata_Featured Views table created')
        else:
            log.warning('Civicdata_Features Views table already exists')
            print 'Civicdata_Featured Views table already exists'
