# usage

1. Crawl the website and generate the result to a csv file
	scrapy crawl Booking -o data.csv -t csv
2. Convert the csv to excel file and generate the histogram.
	python histogram.py