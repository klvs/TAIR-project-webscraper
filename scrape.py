#! /usr/bin/python

from bs4 import BeautifulSoup
import re
import requests
import urlparse
import sys

# todo
# log failed urls instead of exiting
# threading for multiple request - examine speeds first
# add strip tags routine
# support for more than 15 publications

# features 
# start/stop w/o losing place
# command line

def main():
	# File to output to
	out = 'tair.txt'
	# inp = open('atgs.txt')
	atgs = (line.rstrip('\n') for line in open('atgs.txt'))
	# inp.readlines()
	# inp.close()

	i = 0
	for atg in atgs:
		i += 1
		print 'REQ #' + str(i)
		tairReq(atg, out)



## tair request ##
# writes publications, annotations,
# and other names along w/ locus to txt file
def tairReq(locus, outfile):
	BASE_URL = "http://www.arabidopsis.org"
	# locus = "AT1G51620"
	output = open(outfile, 'a')

	# write locus
	output.write(locus + '\n')

	# make request to TAIR
	req = requests.get("http://www.arabidopsis.org/servlets/Search?type=general&search_action=detail&method=1&show_obsolete=F&name=" +
	locus + "&sub_type=gene&SEARCH_EXACT=4&SEARCH_CONTAINS=1")
	
	print "Tair Search request: " + locus

	soup = BeautifulSoup(req.text)
	links = soup.findAll('a', href=True)

	# find target link on search page
	targetLink = []
	for tag in links:
		if(tag.getText() == locus):
			targetLink.append(tag['href']) 
	# list should be singular 
	if(len(targetLink) != 1):
		print "ERROR: Multiple or no links retrived"
		sys.exit(1)
	else:
		targetLink = targetLink[0]

	# open targeted link
	url = BASE_URL + targetLink
	req = requests.get(url)
	print "REQUESTING: " + locus

	soup = BeautifulSoup(req.text)

	# other names
	output.write("Other names: \n")
	field = re.compile('Other names')
	output.write(soup.find(text=field).parent.parent.findAll('td')[1].text.strip() + '\n')
	print "Names parsed"

	# publications 
	output.write("Publications: \n")
	field = re.compile('Publication')
	for tag in soup.find_all(text=field):
		if(tag.string == "Publication "):
			pub_len = len(tag.parent.parent.findAll('td')[1].findAll('tr'))
			# range starts at 1 to skip first tr containing only th
			try:
				for x in xrange(1,pub_len):
					output.write(tag.parent.parent.findAll('td')[1].findAll('tr')[x].findAll('td')[2].text + ': ') 
					output.write(tag.parent.parent.findAll('td')[1].findAll('tr')[x].findAll('td')[0].text + '\n') 
			except IndexError:
				print (locus + "more publications than supported")
	print "Publications parsed"
	output.write("\n")

	# annotations 
	output.write("Annotations: \n")
	field = re.compile('Annotations')
	for tag in soup.find_all(text=field):
		if(tag.string == "Annotations "):
			pub_len = len(tag.parent.parent.findAll('td')[1].findAll('tr'))
			# range starts at 1 to skip first tr containing only th
			# -1 to skip "annotation detail" link
			for x in xrange(1,pub_len -1):
				output.write(tag.parent.parent.findAll('td')[1].findAll('tr')[x].findAll('td')[0].text.strip() + ' ')
				output.write(tag.parent.parent.findAll('td')[1].findAll('tr')[x].findAll('td')[2].text.strip() + ' ') 
				output.write(tag.parent.parent.findAll('td')[1].findAll('tr')[x].findAll('td')[4].text.strip() + '\n') 

				# print tag.parent.parent.findAll('td')[1].findAll('tr')[x].findAll('td')[0].text + '\n' 
	print "Annotations parsed"
	output.write('\n\n')
	output.close()

main()
