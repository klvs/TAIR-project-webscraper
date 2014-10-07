TAIR-project-webscraper
=======================

Scrapes publications, annotations and other names for locus

I reccomend using their REST API instead of scraping. If you only need basic info.

REST service: https://www.arabidopsis.org/locus/<name> 

Time delay before each request is 2 seconds 

Please don't abuse TAIR and abide by their terms of use. And really, just use the REST service if you can.

USAGE
======================
I use virtualenv so all dependencies are included. Just "bin/activate" and "python scrape.py" to start it. It reads line by line from the text file "atgs.txt" and writes to "Tair.txt". Obviously you can adapt this however you want.

You can you with no arguments                       "python scrape.py"
				 specifying input                   "python scrape.py input.txt"
				 specifying input & output files    "python scrape.py input.txt output.txt"
