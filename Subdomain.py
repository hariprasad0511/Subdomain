import os,socket,sys,argparse,itertools,time

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--domain', help="Domain to search. Example: -d google.com", action='store', dest='domain')
parser.add_argument('-w', '--wordlist', help="Wordlist based subdomain enumeration", action='store_true', dest='wordlist')
parser.add_argument('-b', '--bruteforce', help="Bruteforce based subdomain enumeration", action='store_true', dest='bruteforce')
parser.add_argument('-t', '--tld', help="TLD domain discovery", action='store_true', dest='tld')

args = parser.parse_args()

print "\n - Created by H4ck3rCame -\n"
print " If not you, who? If not now, when?"
print "  _   _            _      ____             _    _ "
print " | | | | __ _  ___| | __ | __ )  __ _  ___| | _| |"
print " | |_| |/ _` |/ __| |/ / |  _ \ / _` |/ __| |/ / |"
print " |  _  | (_| | (__|   <  | |_) | (_| | (__|   <|_|"
print " |_| |_|\__,_|\___|_|\_\ |____/ \__,_|\___|_|\_(_)"

domain = args.domain
if (type(domain) != str):
	print "[!] Domain not defined"
	sys.exit(1)
elif (args.wordlist == False and args.bruteforce == False and args.tld == False):
	print "[!] No parameters defined"
	sys.exit(1)

print "\n[*] Checking if domain exists..."
try:
	get = socket.gethostbyname(domain.strip())
	print '[%s] Domain %s is valid - %s' % (time.strftime("%H:%M:%S"),domain.strip(), get)
	r = True
except socket.gaierror, e:
	print "[%s] Unable to resolve: %s" % (time.strftime("%H:%M:%S"), domain.strip())
	print "[*] Retrying by adding www at the beginning..."
	rdomain = "www."+domain.strip()
	try:
		get = socket.gethostbyname(rdomain.strip())
		print '[%s] Domain %s is valid - %s' % (time.strftime("%H:%M:%S"), rdomain.strip(), get)
		r = True
	except socket.gaierror, e:
		print "[%s] Unable to resolve: %s" % (time.strftime("%H:%M:%S"), rdomain.strip())
		r = False

if (r):
	if (args.wordlist):
		subdomain_dict = dict()
		ip_list_w = []
		subdomain_list_w = []
		print "\n[WORDLIST] Searching for subdomains..."
		f = open("hosts.txt", "r")
		for line in f:
			line = line.strip('\n')
			subdomain = str(line)+"."+str(domain)
			print '{0}\r'.format(subdomain),
			try:
				get = socket.gethostbyname(subdomain.strip())
				print "["+time.strftime('%H:%M:%S')+"] Subdomain found: "+str(subdomain)+" - "+get
				if (get in subdomain_dict):
					subdomain_dict[get].append(str(subdomain))
				else:
					subdomain_dict[get] = [str(subdomain)]
				if subdomain in subdomain_list_w:
					pass
				else:
					subdomain_list_w.append(subdomain)
				if get in ip_list_w:
					pass
				else:
					ip_list_w.append(get)
			except socket.gaierror, e:
				pass
			except KeyboardInterrupt:
				print "You pressed Ctrl+C"
				print "[*] Stopping..."
				sys.exit()
		f.close()
		print "\t\t\t\t\t\t\t\t\r"
		print "%s subdomains found!" % (str(len(subdomain_list_w)))
		print "%s IPs found!" % (str(len(ip_list_w)))
		for ip in subdomain_dict:
			espais = 21-len(ip)
			print ip, "-"*espais, subdomain_dict[ip][0]
			if len(subdomain_dict) > 1:
				length = len(subdomain_dict[ip])
				for sub in range(1, length):
					print " "*15, " |----", subdomain_dict[ip][sub]

	if (args.tld):
		domain_tld_list = []
		ip_tld_list = []
		print "\n[WORDLIST] Searching for other TLDs..."
		domain = domain.split(".")[0]
		f = open("tlds.txt", "r")
		for line in f:
			line = line.strip('\n')
			line = line.lower()
			domain_tld = str(domain)+"."+str(line)
			print '{0}\r'.format(domain_tld),
			try:
				get = socket.gethostbyname(domain_tld.strip())
				print "["+time.strftime('%H:%M:%S')+"] Subdomain found: "+str(domain_tld)+" - "+get
				if domain_tld in domain_tld_list:
					pass
				else:
					domain_tld_list.append(domain_tld)
				if get in ip_tld_list:
					pass
				else:
					ip_tld_list.append(get)
			except socket.gaierror, e:
				pass
			except KeyboardInterrupt:
				print "You pressed Ctrl+C"
				print "[*] Stopping..."
				sys.exit()
		f.close()
		print "\t\t\t\t\t\t\t\t\r"
		print "%s domains found!" % (str(len(domain_tld_list)))
		print "%s IPs found!" % (str(len(ip_tld_list)))

	if (args.bruteforce):
		ip_list_b = []
		subdomain_list_b = []
		print "\n[BRUTEFORCE] Searching for subdomains..."
		minim = 1
		maxim = 66 - len(domain)
		alfabet = "abcdefghijklmnopqrstuvwxyz0123456789"
		while minim <= maxim:
			for i in itertools.combinations_with_replacement(alfabet, minim):
					i = ''.join(i)
					subdomain = str(i)+"."+str(domain)
					print '{0}\r'.format(subdomain),
					try:
						get = socket.gethostbyname(subdomain.strip())
						print "["+time.strftime('%H:%M:%S')+"] Subdomain found: "+str(subdomain)+" - "+get
						if subdomain in subdomain_list_b:
							pass
						else:
							subdomain_list_b.append(subdomain)
						if get in ip_list_b:
							pass
						else:
							ip_list_b.append(get)
					except socket.gaierror, e:
						pass
					except KeyboardInterrupt:
						print "You pressed Ctrl+C"
						print "[*] Stopping..."
						sys.exit()
			minim = minim+1

	print "\n[*] Finished!"
else:
	print "\n[!] Enter another domain"