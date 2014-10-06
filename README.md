TAIR-project-webscraper
=======================

Scrapes publications, annotations and other names for locus

I reccomend using their REST API instead of scraping. Had I known this existsed I'd have saved a lot of time.

Use https://www.arabidopsis.org/locus/<name> REST service instead and parse the JSON. I'll post a sample. 

If you want to use this, because it's up and running right now. You should adapt the loop in scrape.py main() to wait before 
forming another request because TAIR really can't handle people bombarding them w/ requests at 2/sec and WILL BLACKLIST YOU.

Please don't abuse TAIR and abide by their terms of use. And really, just use the REST service.

###########USAGE############
I use virtualenv so all dependencies are included. Just "bin/activate" and "python scrape.py" to start it. It reads line by line from the text file "atgs.txt" and writes to "Tair.txt". Obviously you can adapt this however you want.
