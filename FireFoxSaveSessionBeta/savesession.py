import sys
import json
import os
import subprocess
import webbrowser
cwd=os.path.dirname(os.path.abspath(__file__))
print cwd

def usage():
	print 'Usage:'
	print '[save|open|show|delete]'

def delete_session(present):
	session_info = open(cwd + "/" + 'session_info', 'a+')
	sessions = session_info.readlines()
	alreadyexists = (present + '\n') in sessions
	if not alreadyexists:
		print "Session doesn't exist"
		print "Cannot be deleted"
		return
	sessions.remove(present + '\n')
	s = ''.join(sessions)
	write = open(cwd+'/session_info','w')
	write.write(s)
	os.remove(cwd + "/" + 'sessions' + "/" + present)
	print "Session "+present+ " deleted Successfully!"	

def main():
	if len(sys.argv)>3:
		usage()
		exit(-1)

	if sys.argv[1] not in ['save', 'open', 'show', 'delete']:
		usage()
		exit(-1)

	if sys.argv[1] == 'save':
		try:
			path = open(cwd + "/" + "path",'r')
			s = path.read()[:-1]
			fp = open(s + "/" + 'sessionstore.js','r')
			content=json.load(fp)
			present=sys.argv[2]
			session_info=open(cwd + "/" + 'session_info','a+')
			alreadyexists = (present+'\n') in session_info
			if alreadyexists:
				print "session with same name already exists"
				print "Choose Different session name"
			else:
				session_info.write(present+'\n')
				f=open(cwd + "/" + 'sessions' + "/" + sys.argv[2], 'w')
				windows=content['windows']
				for n, w in enumerate(windows, 1):
					tabs = w['tabs']
					for tab in tabs:
						e=tab['entries'][0]
						f.write('{}\n'.format(e['url']))
			print "Session " + present + " saved Successfully!"		
		except(IOError):
			print "Error"
	elif sys.argv[1] == 'open':
		session_info=open(cwd + "/" + 'session_info','r')
		present = sys.argv[2]
		alreadyexists = (present+'\n') in session_info
		if not alreadyexists:
			print "session doesn't exist"
			print "Cannot be Opened"		
		else:
			f = open(cwd + "/" + 'sessions' + "/" + sys.argv[2],'r')
			subprocess.call(["firefox"] + [url[:-1] for url in f])
	elif sys.argv[1] == 'show':
		session_info=open(cwd + "/" + 'session_info','r')
		print "Already existing sessions"
		print session_info.read()[:-1]
	elif sys.argv[1] == 'delete':
		present = sys.argv[2]
		delete_session(present)			

if __name__ == '__main__':
	main()
		
