#!/usr/bin/python
from pyactor.context import set_context, create_host, sleep, shutdown, serve_forever
import sys, os,re
import requests


def separate(input_file,num_mappers,folder):
	with open(input_file) as f:
		for i, l in enumerate(f):
			pass
	lines=i+1
	lin_map=(lines/num_mappers)
	fileToCount=open(input_file,'r')
	m=0
	while(m<num_mappers):
		mapperFile=open(folder+'/Mapper'+str(m)+'.txt','w')
		print('Creat arxiu: Mapper'+str(m))
		j=0
		while(j<lin_map):
			line=fileToCount.readline()
			mapperFile.write(line)
			j+=1
		mapperFile.close()
		m+=1

	mapperFile=open(folder+'/Mapper'+str(m-1)+'.txt','a')
	j=0
	while True:
		line=fileToCount.readline()
		if not line: break
		mapperFile.write(line)

	mapperFile.close()

	fileToCount.close()


class Master(object):
	_tell = ['showResult']

	def showResult(self,result):
		print 'Resultat final '+str(result)

#master: ip_master	port_master	carpeta_server	port_server	mapperFile.txt	num_mappers	ip_registry	port_registry	accio ('wordCount' o 'CountingWords')
if __name__ == "__main__":

	num_map=int(sys.argv[6])
	separate(sys.argv[5],num_map,sys.argv[3])
 	set_context()
	host = create_host('http://'+sys.argv[1]+':'+sys.argv[2])
	registry = host.lookup_url('http://'+sys.argv[7]+':'+sys.argv[8]+'/registre', 'Registry','registry')
	registry.bind('master',host)
	master=host.spawn('master', 'master/Master')
	reducer_host=registry.lookup('reducer')
	reducer=reducer_host.lookup('reducer')
	mappers=[]
	textToCount=[]
	
	for i in range(0,num_map):
		print sys.argv[3]+"/Mapper"+str(i)+".txt"
		mapper_host=registry.lookup('mapper'+str(i))
		mappers.append(mapper_host.lookup('mapper'+str(i)))
		textToCount.append(open(sys.argv[3]+"/Mapper"+str(i)+".txt", 'r').read())

	reducer.setN(num_map)
	for i in range(0,num_map):
		if(sys.argv[9]=='wordCount'):
			mappers[i].wordCount(textToCount[i])
		elif(sys.argv[9]=='countingWords'):
			mappers[i].countingWords(textToCount[i])
		else: print ('Accio no disponible per als mappers')

	serve_forever()
	shutdown()
