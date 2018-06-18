import requests,os,sys
#server: port_server carpeta_server

if __name__ == '__main__':
	os.system("mkdir -p "+sys.argv[2])
	os.chdir(sys.argv[2])
	os.system("python -m SimpleHTTPServer "+sys.argv[1])
