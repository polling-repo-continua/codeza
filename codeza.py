def logo():

	print ('\033[94m' + """
 ___________________________________________________________________
|                                                                   |
|          /|                                                       |
|         / |                             This Is my first tool :)  |
|   _____|  |_____                                                  |
|  /_____   _____/                                                  |
|        |  | _      ____   ____   ____   _____  _____      _       |
|        |  || |    |####| |####| |####  |##### |#####     /#\      |
|        |  || |   |#      #    # |#   # |#|__     /#     /# #\     |
|        |  || |   |#      #    # |#   # |####    /#     /#/_\#\    |
|        |  ||/    |#____  #____# |#___# |#|___  /#___  /#/   \#\   |
|        | /        |####| |####| |####  |##### /##### /#/     \#\  |
|        |/                                                         |
|                    # Coded By Raunak Parmar - @trouble1_raunak    |
|___________________________________________________________________|
	""" + '\033[00m')

import requests
import os
import sys
import time
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Back, Style
import re
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


if len(sys.argv) != 4:
	print "(+) usage: %s <file> <Min_Length> <Folder_name_to_create>" % sys.argv[0]
	print "(+) eg: %s alive.txt 500 ford" % sys.argv[0]
	print "(+) Note: List should contain http:// or https://"
	sys.exit(-1)

# Arguments
file = sys.argv[1]
length = sys.argv[2]
foldername = sys.argv[3]
logo()
m  = 0
f = open(file)

def contactMe():
	print
	print ('\033[96m' + "(+) Result will be saved in folder name " + foldername + "/ " + '\033[00m')
	print ('\033[96m' + "(+) Contact me on twitter for any suggestion or help- @trouble1_raunak" + '\033[00m')
	print ""
	
def createFolders():
	os.system("mkdir " + foldername)
	os.system('mkdir '+ foldername+'/status/')
	os.system("mkdir " + foldername + "/error/")

# Is there a directory?
isdir = os.path.isdir(foldername)

# Validating base folder
if isdir == True:
	time.sleep(0.3)
	print(('\033[91m' + "[!] " + '\033[00m') + ('\x1b[6;29;41m' + foldername + "/"+ '\x1b[0m') + " folder already exits")
	time.sleep(0.5)
	
	# everything in this IF statement logic depends on user input
	input = raw_input(('\033[93m' + "[!] " + '\033[00m') + "Delete current folder? (y/n): ")
	if input == "y":
		os.system("rm -r " + foldername +"/")
		createFolders()
		print ('\033[92m' + "[!] " + '\033[00m') + foldername +"/" + " Deleted, creating a new one"
		contactMe()
		
	elif input == "n":
		input = raw_input(('\033[93m' + "[!] " + '\033[00m') + "Overwrite on current folder? (y/n): ")
		if input == "y":
			print ('\033[92m' + "[!] " + '\033[00m') + "Okk fine, Overwriting in " + foldername +"/"
			contactMe()
		elif input == "n":
			foldername = raw_input(('\033[92m' + "[!] " + '\033[00m') + "Type the name of the new folder: ")
			isdir = os.path.isdir(foldername)
			if isdir == True:
				print('\033[91m' + "[!] " + '\033[00m') + "Please provide new folder name :|"
				time.sleep(0.4)
				print ('\033[91m' + "[!] " + '\033[00m') +("Bye :)")
				sys.exit()
			else:
				createFolders()
				contactMe()
	else:
		print ('\033[91m' + "[!] " + '\033[00m') + "Wrong input :("
		sys.exit()
	
else:
	createFolders()
	
print ""

for line in f:
	try:
		m = m +1
		line = line.strip('\r\n')
		
		# Request made here
		req = requests.get(url = line, allow_redirects=True, verify=False )
		res = req.text
		forms = ["</form>", "password", "username", "methods="]
		forms_found = False
		
		# check for forms
		for item in forms:    
			if item in res:
				forms_found = True
				found = item
		# for Dom XSS
		if forms_found:
			os.system("echo '" + line + " --> contains: " + found +"' >> " + foldername +"/contains_form.txt")
		Dom_xss = ['document.URL', 'document.documentURI', 
					'location', 'location.href', 
					'location.search', 'location.hash', 
					'document.referrer', 'window.name', 
					'eval', 'setTimeout','setInterval', 
					'document.write', 'document.writeIn', 
					'innerHTML', 'outerHTML' ]
					
		Dom_xss_possible = False
		for item in Dom_xss:    
			if item in res:
				Dom_xss_possible = True
				found = item
		if Dom_xss_possible:
			os.system("echo '" + line + " --> contains: "+ found+ "' >> " + foldername + "/possible_Dom_XXS.txt" )
		status = req.status_code
		if(len(res) > int(length)):
			try:
				os.system('echo '+ line + ' >> '+ foldername +'/potential.txt')
				r1 = re.findall("<title>(.+?)</title>",res)
				
				if not r1:  
					title = ('\033[91m' + " No Title" + '\033[00m')

				else:
					title = r1[0]

				# result in with_titles.txt
				os.system("echo '" + line + " -->  " + title + "' >> " + foldername + "/with_titles.txt")
					
				result = " " + ('\033[92m' +line + '\033[00m')+ ('\033[93m' +" --> " + '\033[00m') + ('\x1b[6;29;43m ' + 'Len:' + '\x1b[0m') + " " + ('\033[92m' + str(len(res)) + '\033[00m') + ('\033[94m' +" --> " + '\033[00m') +('\x1b[6;29;44m ' + 'Title:' + '\x1b[0m') +" " + ('\033[92m' + title + '\033[00m')

				CSI = "\x1B["
				
				# full result
				full_result = (CSI+"29;45m" + "[ Line No: " + str(m) + " ]"+ CSI + "0m")+ result
				result1 = line + " --> " + "Len: " +str(len(res)) + " --> " + " Title: " + title
				
				# upadating result
				os.system("echo '" + result1 + "' >> " + foldername +"/potential_result.txt")
				print full_result
				
			# error while upadating with_title.txt file
			except UnicodeEncodeError as error:
					print ('\x1b[6;29;41m' + "[Error: Line no: "+ str(m)  + " Url: " + line + "]"+ '\x1b[0m')+ ('\033[91m' + " There was error while updating result in with_title.txt" + '\033[00m')
					print ""
					update = line + " [Error: Line no "+ str(m) + " ]"
					os.system("echo " + update + " >> " + foldername + "/error/title_error.txt")
					pass
		
		# urls with status code are been saved from here in status/ folder
		req_status = requests.get(url = line, allow_redirects=False, verify=False )
		status =  str(req_status.status_code)
		result2 = str(line )
		file_name = foldername + "/status/"+status + ".txt"
		os.system("echo '" + result2 + "' >> " + file_name)
	
	
	# List of Possible Exceptions begins from here
	  
	
	# error for connectionError
	except requests.exceptions.ConnectionError as e:
		print ('\x1b[6;29;41m' + "[Error: Line no: "+ str(m) + " Url: " + line + "]"+ '\x1b[0m') + ('\033[91m' + " Connection error" + '\033[00m')
		print ""
		update = line + " [Error: Line no "+ str(m) + " ]"
		os.system("echo " + update + " >> " + foldername + "/error/ConnectionError.txt")
		pass
		
	# error for tooManyRedirects
	except requests.exceptions.TooManyRedirects as e:
		print ('\x1b[6;29;41m' + "[Error: Line no: "+ str(m) + " Url: " + line + "]"+ '\x1b[0m') + ('\033[91m' + " Too many redirects" + '\033[00m')
		print ""
		update = line + " [Error: Line no "+ str(m) + " ]"
		os.system("echo " + update + " >> " + foldername + "/error/TooManyRedirects.txt")
		pass
		
	# error for invalid url	
	except requests.exceptions.MissingSchema as e:
		print ('\x1b[6;29;41m' + "[Error: Line no: "+ str(m) + " Invalid Url: " + line + "]"+ '\x1b[0m')+ ('\033[91m' + " Invalid URL " + '\033[00m')
		print ""
		update = line + " [Error: Line no "+ str(m) + " ]"
		os.system("echo " + update + " >> " + foldername + "/error/Invalid_Url.txt")
		pass
	
	# error for Chunked Encoding
	except requests.exceptions.ChunkedEncodingError as e:
		print ('\x1b[6;29;41m' + "[Error: Line no: "+ str(m) + " Url: " + line + "]"+ '\x1b[0m')+ ('\033[91m' + " ChunkedEncodingError" + '\033[00m')
		print ""
		update = line + " [Error: Line no "+ str(m) + " ]"
		os.system("echo " + update + " >> " + foldername + "/error/ChunkedEncodingError.txt")
		pass

	# error for InvalidSchema
	except requests.exceptions.InvalidSchema as e:
		print ('\x1b[6;29;41m' + "[Error: Line no: "+ str(m) + " Url: " + line + "]"+ '\x1b[0m')+ ('\033[91m' + " InvalidSchema" + '\033[00m')
		print ""
		update = line + " [Error: Line no "+ str(m) + " ]"
		os.system("echo " + update + " >> " + foldername + "/error/InvalidSchema.txt")
		pass

	# error for InvalidURL
	except requests.exceptions.InvalidURL as e:
		print ('\x1b[6;29;41m' + "[Error: Line no: "+ str(m) + " Url: " + line + "]"+ '\x1b[0m')+ ('\033[91m' + " InvalidURL" + '\033[00m')
		print ""
		update = line + " [Error: Line no "+ str(m) + " ]"
		os.system("echo " + update + " >> " + foldername + "/error/InvalidURL.txt")
		pass
		
	#except Exception as e:	
	#	pass
	
print "(+) Done :)"
