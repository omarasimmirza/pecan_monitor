# from re import template
from ..server.model.db_methods import get_all
from ..server.info_server import set_up
from pecan import expose

class RootController(object):

    @expose(generic=True, template='json')
    def index(self):
        return get_all()

    @index.when(method='POST', template='json')
    def index_post(self, **data):
        set_up(data)
        return "done"