
from pyactor.context import set_context, create_host, serve_forever
import sys


class NotFound(Exception):
    pass


class Registry(object):
    _ask = ['bind', 'lookup']
    _ref = ['bind', 'lookup']

    def __init__(self):
        self.dictActors = {}

    def bind(self, name, actor):
        print "server registred ",name
        self.dictActors[name] = actor


    def lookup(self, name):
        if name in self.dictActors:
            return self.dictActors[name]
        else:
            return None


#registry: ip_registry	port_registry
if __name__ == "__main__":
    set_context()
    host = create_host('http://'+sys.argv[1]+':'+sys.argv[2]+'/')

    registry = host.spawn('registre', Registry)

    print 'host '+sys.argv[1]+'listening at port'+sys.argv[2]

    serve_forever()
