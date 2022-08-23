# from re import template
from ..server.model.db_methods import get_all
from ..server.info_server import set_up
from pecan import expose, redirect
from webob.exc import status_map

class RootController(object):

    @expose(generic=True, template='json')
    def index(self):
        machines_list = get_all()
        return machines_list

    @index.when(method='POST', template='json')
    def index_post(self, **data):
        set_up(data)
        return "done"

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
