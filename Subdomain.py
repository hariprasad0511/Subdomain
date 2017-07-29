import os,socket,sys,itertools,time

domain = sys.argv[1]
print "\n - Created by H4ck3rCame -\n"
print " If not you, who? If not now, when?"
print "  _   _            _      ____             _    _ "
print " | | | | __ _  ___| | __ | __ )  __ _  ___| | _| |"
print " | |_| |/ _` |/ __| |/ / |  _ \ / _` |/ __| |/ / |"
print " |  _  | (_| | (__|   <  | |_) | (_| | (__|   <|_|"
print " |_| |_|\__,_|\___|_|\_\ |____/ \__,_|\___|_|\_(_)"

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

if r == True:
	ip_list = []
	subdomain_list = []
	print "\n[WORDLIST] Searching for subdomains..."
	f = open("hosts.txt", "r")
	for line in f:
		line = line.strip('\n')
		subdomain = str(line)+"."+str(domain)
		print '{0}\r'.format(subdomain),
		try:
			get = socket.gethostbyname(subdomain.strip())
			print "["+time.strftime('%H:%M:%S')+"] Subdomain found: "+str(subdomain)+" - "+get
			if subdomain in subdomain_list:
				pass
			else:
				subdomain_list.append(subdomain)
			if get in ip_list:
				pass
			else:
				ip_list.append(get)
		except socket.gaierror, e:
			pass
		except KeyboardInterrupt:
			print "You pressed Ctrl+C"
			print "[*] Stopping..."
			sys.exit()
	f.close()
	print "\t\t\t\t\t\t\t\t\r"
	print "%s subdomains found!" % (str(len(subdomain_list)))
	print "%s IPs found!" % (str(len(ip_list)))
	response = str(raw_input("["+time.strftime('%H:%M:%S')+"] Do you want to try with bruteforce? [y/N] "))
	if response == "Y" or response == "y":
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
						if subdomain in subdomain_list:
							pass
						else:
							subdomain_list.append(subdomain)
						if get in ip_list:
							pass
						else:
							ip_list.append(get)
					except socket.gaierror, e:
						pass
					except KeyboardInterrupt:
						print "You pressed Ctrl+C"
						print "[*] Stopping..."
						sys.exit()
			minim = minim+1
	else:
		print "\n[*] Skipping bruteforce"

	for s in subdomain_list:
		f = open("hosts.txt", "r")
		print "[%s] Scanning for subdomains in %s..." % (time.strftime("%H:%M:%S"), s)
		for line in f:
			line = line.strip('\n')
			subdomain1 = str(line)+"."+str(s)
			print '{0}\r'.format(subdomain1),
			try:
				get = socket.gethostbyname(subdomain1.strip())
				print "["+time.strftime('%H:%M:%S')+"] Subdomain found: "+str(subdomain1)+" - "+get
				if subdomain1 in subdomain_list:
					pass
				else:
					subdomain_list.append(subdomain1)
				if get in ip_list:
					pass
				else:
					ip_list.append(get)
			except socket.gaierror, e:
				pass
			except KeyboardInterrupt:
				print "You pressed Ctrl+C"
				print "[*] Stopping..."
				sys.exit()
		f.close()

	print "\n[*] Finished!"
else:
	print "\n[!] Enter another domain"