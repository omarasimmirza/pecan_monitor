from pecan import abort, expose

# Note: this is *not* thread-safe.  In real life, use a persistent data store.
BOOKS = {
    '0': 'The Last of the Mohicans',
    '1': 'Catch-22'
}


class BookController(object):

    def __init__(self, id_):
        self.id_ = id_
        assert self.book

    @property
    def book(self):
        if self.id_ in BOOKS:
            return dict(id=self.id_, name=BOOKS[self.id_])
        abort(404)

    # HTTP GET /<id>/
    @expose(generic=True, template='json')
    def index(self):
        return self.book

    # HTTP PUT /<id>/
    @index.when(method='PUT', template='json')
    def index_PUT(self, **kw):
        BOOKS[self.id_] = kw['name']
        return self.book

    # HTTP DELETE /<id>/
    @index.when(method='DELETE', template='json')
    def index_DELETE(self):
        del BOOKS[self.id_]
        return dict()


class RootController(object):

    @expose()
    def _lookup(self, id_, *remainder):
        return BookController(id_), remainder

    # HTTP GET /
    @expose(generic=True, template='json')
    def index(self):
        return [dict(id=k, name=v) for k, v in BOOKS.items()]

    # HTTP POST /
    @index.when(method='POST', template='json')
    def index_POST(self, **kw):
        id_ = str(len(BOOKS))
        BOOKS[id_] = kw['name']
        return dict(id=id_, name=kw['name'])
# from pecan import expose, redirect
# from webob.exc import status_map


# class RootController(object):

#     @expose(generic=True, template='index.html')
#     def index(self):
#         return dict()

#     @index.when(method='POST')
#     def index_post(self, q):
#         redirect('https://pecan.readthedocs.io/en/latest/search.html?q=%s' % q)

#     @expose('error.html')
#     def error(self, status):
#         try:
#             status = int(status)
#         except ValueError:  # pragma: no cover
#             status = 500
#         message = getattr(status_map.get(status), 'explanation', '')
#         return dict(status=status, message=message)
