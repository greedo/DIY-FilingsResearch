#! /usr/bin/env python
# encoding: utf-8

import urllib2

def download_file(url):

        local_filename = url.split('/')[-1]
        
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        with open(local_filename, 'w') as f:
                f.write(response.read())
        return local_filename

def get_tickers(local_filename):
        
        writer = open('tickers.txt','w')
        with open(local_filename, 'r') as reader:
                for line in reader:
                        if line.split('|')[0] != "Symbol" and "File Creation Time" not in line.split('|')[0]:
                                writer.write(line.split('|')[0]+"\n")
        writer.close()

if __name__ == '__main__':
        get_tickers(download_file('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'))
