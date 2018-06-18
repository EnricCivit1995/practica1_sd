#!/usr/bin/python
import sys, os,re,time
import requests


def wordCount(texto):
	t1=time.time()
	wordcount={}
	for word in texto:
		word = word.encode('utf-8')	
		word = word.translate(None,'!-.";:?,')
    		if word not in wordcount:
        		wordcount[word] = 1
    		else:
        		wordcount[word] += 1
	print ("WordCount: El temps en sequencial es de "+str(time.time()-t1))
	return wordcount

def countwords(texto):
	result=0
	t1=time.time()
	for word in texto:
		result+=1

	print ("CountWords: El temps en sequencial es de: "+str(time.time()-t1))


if __name__ == "__main__":
	
	file=open(sys.argv[1],'r')
	texto = re.sub('[^ a-zA-Z0-9]',' ', file.read()).split()	
	wordCount(texto)
	countwords(texto)


