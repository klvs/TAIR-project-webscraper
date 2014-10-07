#! /usr/bin/python
##################################################
# TAIR SCRAPER v1.0 Author: Kvls (Alex@allexr.com)
# scrapes:
# 	publications (not hyperlinked)
# 	"other names"
# 	Annotations (relatioships ect.)
# given a locus
################################################

from bs4 import BeautifulSoup
import re
import requests
import urlparse
import time
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
	# remove "scrape.py"
	sys.argv.pop(0)

	# File to output to
	if(len(sys.argv) == 1):
		inputFile = sys.argv[0]
	else:
		inputFile = 'atgs.txt'

	# specify input and output	
	if(len(sys.argv) == 2):
		inputFile = sys.argv[0]
		out = sys.argv[1]
	else:
		out = 'tair.txt'
		inputFile = 'atgs.txt'


	inp = open(inputFile)
	atgs = inp.readline().split(',')
	# print atgs
	i = 0
	length = len(atgs)
	for atg in atgs:
		i += 1
		print atg + ': #' + str(i) + '/' + str(length)
		tairReq(atg, out)
		# time delay: Let's go easy on these guys. 
		time.sleep(2)

	print 'Done' 



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
		print "ERROR: Multiple or no links retrived. Should be 1"
		sys.exit(1)
	else:
		targetLink = targetLink[0]

	# open targeted link
	url = BASE_URL + targetLink
	req = requests.get(url)
	print "Tair " + locus + " page success"

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
				output.write('More than 15 publications. See webpage.')
	print "publications parsed"
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
	output.write("\n\n\n") 
	output.close()

main()
