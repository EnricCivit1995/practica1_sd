from pyactor.context import set_context, create_host, sleep, shutdown, serve_forever
from operator import add
from collections import Counter
import requests,sys,time


class Reducer(object):
    _tell = ['reduceWordCount','reduceCountingWords','setN']

    def __init__(self,registry):
        self.dictionaries=[]
        self.numMappers=0
        self.reduct=None
	self.cont=0
        self.registry=registry
	self.master=None
        self.t=0


    def reduceWordCount(self,dic):
        self.dictionaries.append(dic)
	self.numMappers=self.numMappers-1
	if self.numMappers==0:
		ti=time.time()
		self.reduct=dict(reduce(add, (Counter(dict(x)) for x in self.dictionaries)))
		tt=time.time()-self.t
                print self.reduct
		print "TEMPS TOTAL WORDCOUNT: " +str(tt)
		print ("El Reducer ha tardat: "+str(time.time()-ti))
		self.master.showResult(self.reduct)
		self.dictionaries=[]

    def reduceCountingWords(self,cont):
	ti=time.time()
	self.cont=self.cont+cont
	self.numMappers=self.numMappers-1
	if self.numMappers==0:
		tt=time.time()-self.t
		print "Num paraules "+str(self.cont)
		print "TEMPS TOTAL COUNTINGWORDS: " +str(tt)
		print ("El Reducer ha tardat: "+str(time.time()-ti))
		self.master.showResult(self.cont)


    def setN(self,numMappers):
        self.numMappers=numMappers
	master_host=self.registry.lookup('master')
	master=master_host.lookup('master')
	self.master=master
        self.t=time.time()


#reducer: ip_reducer	port_reducer	ip_registry	port_registry
if __name__ == "__main__":
	print 'reducer'
	set_context()
	host = create_host('http://'+sys.argv[1]+':'+sys.argv[2])
	registry = host.lookup_url('http://'+sys.argv[3]+':'+sys.argv[4]+'/registre', 'Registry','registry')
	registry.bind('reducer',host)
	reducer=host.spawn('reducer','reducer/Reducer',registry)

	serve_forever()
