from ..server.model.db_methods import get_all, get_one, delete, update
from ..server.info_server import set_up
from pecan import expose, abort

class MachineController(object):

    def __init__(self, ip):
        self.ip = ip

    @property
    def machines(self):
        return self.ip

    @expose(generic=True, template='json')
    def index(self):
        machine = get_one(self.ip)
        if len(machine) == 0:
            abort(404)
        return machine

    @index.when(method='DELETE', template='json')
    def index_DELETE(self):
        return delete(self.ip)
    
    @index.when(method='PUT', template='json')
    def index_PUT(self, **data):
        return update(data, self.ip)

class RootController(object):

    @expose()
    def _lookup(self, ip, *remainder):
        return MachineController(ip), remainder

    @expose(generic=True, template='json')
    def index(self):
        return get_all()

    @index.when(method='POST', template='json')
    def index_POST(self, **data):
        set_up(data)
        return dict()
