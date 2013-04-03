from utils import *


class Browser(object):
    """ ABSTRACT class, implements cmd-type operations like ls, cd etc."""

    ls_config = {
        'ls_filt': {}, # dispslay filters
        'location': '', # current location, like 'metadata/section/293847/'
        'default_ls_mode': 'metadata', # browsing by metadata is default
        'ls_modes': ['data', 'metadata'] # could browse in data mode too
    }

    def ls(self, location=None, filt={}):
        """ cmd-type ls function """
        out = '' # output
        params = dict( self.ls_config['ls_filt'].items() + filt.items() )

        if not location: # if not given use the current one
            location = self.ls_config['location']

        if location:
            out += 'location %s:\n' % location
            app, cls, lid = self._parse_location( location )

            for child in self._meta.app_definitions[ cls ]['children']:

                parent_name = cls
                # FIXME dirty fix!! stupid data model inconsistency
                if (cls == 'section' and child == 'section') or \
                    (cls == 'property' and child == 'value'):
                    parent_name = 'parent_' + parent_name

                params[ parent_name + '__id' ] = lid
                objs = self.list(child, params=params)

                out = self._render( objs, out )
                params.pop( parent_name + '__id' )

            # FIXME exception case for Block -> Section
            if cls == 'section':
                params[ 'section__id' ] = lid
                objs = self.list('block', params=params)
                if objs:
                    out += '\nDATA:\n'
                    out = self._render( objs, out )

        else:
            if self.ls_config['default_ls_mode'] == 'data':
                objs = self.list('block', params=params)

            else: # metadata mode otherwise
                params['parent_section__isnull'] = 1
                objs = self.list('section', params=params)

            out = self._render( objs, out )

        print_status( out )

    def cd(self, location=''):
        """ changes the current location within the data structure """
        if location == '':
            self.ls_config['location'] = ''
            print 'back to root'

        else:
            # 1. compile url
            url = str( location )
            if is_permalink( location ):
                url = url.replace(self._meta.host, '')

            # 2. get the object at the location
            obj = self.pull(url, cascade=False, data_load=False)

            self.ls_config['location'] = url
            print "entered %s" % url


    def _render(self, objs, out):
        """ renders a list of objects for a *nice* output """
        for obj in objs:

            # object location
            location = obj._gnode['permalink'].replace(self._meta.host, '')
            out += self._strip_location(location) + '\t'

            # safety level
            out += str(obj._gnode['safety_level']) + ' '

            # object owner
            out += obj._gnode['owner'].replace(self._meta.host, '') + '\t'

            # object __repr__
            out += obj.__repr__()[ : self._meta.max_line_out ] + '\n'

        return out

