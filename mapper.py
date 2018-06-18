from pyactor.context import set_context, create_host, sleep, shutdown, serve_forever
import sys, time, re

class Mapper(object):
    _tell = ['wordCount','countingWords']


    def __init__(self,reg,red):
        self.result=None
        self.registry=reg
	self.reducer=red

    def wordCount(self,text):
	wordsList=re.sub('[^ a-zA-Z0-9]',' ',text ).split()
	self.result={}
	t1=time.time()
	for paraula in wordsList:
		if paraula not in self.result:
			self.result[paraula] = 1
		else:
			self.result[paraula] += 1
	self.reducer.reduceWordCount(self.result)
        print self.result
	print ("El temps de Mapper"+sys.argv[3]+" es de: "+str(time.time()-t1))

    def countingWords(self,text):
        wordsList = re.sub('[^ a-zA-Z0-9]',' ',text ).split()
        self.result=0
        t1=time.time()
        for paraula in wordsList:
	        self.result+=1
        print self.result
	self.reducer.reduceCountingWords(self.result)
        print ("El temps de Mapper"+sys.argv[3]+" es de: "+str(time.time()-t1))


#mapper: ip_mapper	port_mapper	num_map		ip_registry	port_registry
if __name__ == "__main__":

	set_context()

	print 'Mapper' + str(sys.argv[3])

	host = create_host('http://'+sys.argv[1]+':'+sys.argv[2])

	registry = host.lookup_url('http://'+sys.argv[4]+':'+sys.argv[5]+'/registre', 'Registry','registry')

	registry.bind('mapper'+sys.argv[3],host)

	reducer_host=registry.lookup('reducer')
	reducer=reducer_host.lookup('reducer')

	mapper=host.spawn('mapper'+sys.argv[3], 'mapper/Mapper', registry, reducer)

	serve_forever()
