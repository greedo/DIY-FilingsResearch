#! /usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

import xml.etree.ElementTree as ET
from lxml import etree
import concurrent.futures
import requests
import re
from datetime import datetime, date, time

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class Ingestor():

    def file_downloader(self, urls, directory):

        if len(urls) == 0:
            return

        def load_url(url, timeout):
            request = requests.get(url, stream=True, timeout=timeout)
            return request

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(load_url, url, 60): url for url in urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()

                    if data.status_code == requests.codes.ok:

                        local_filename = url.split('/')[-1]
                        with open(directory+"/"+local_filename, 'wb') as handle:
                            for block in data.iter_content(chunk_size=1024):
                                if not block:
                                    break
                                handle.write(block)
                            handle.close()

                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))


class Sedar():

    def __init__(self, start_date=None, end_date=None):
        self.org_root = "http://www.sedar.com"

        if start_date is None:
            self.start_date = date(1970, 01, 01)
        else:
            self.start_date = datetime.strptime(self.start_date, "%y-%d-%m")

        self.start_month = self.start_date.month
        self.start_day = self.start_date.day
        self.start_year = self.start_date.year

        if end_date is None:
            self.end_date = datetime.now().date()
        else:
            self.end_date = datetime.strptime(self.end_date, "%y-%d-%m")

        self.end_month = self.end_date.month
        self.end_day = self.end_date.day
        self.end_year = self.end_date.year

    def ingest_stock(self, ticker):

        to_parse = []

        feed = requests.get(self.org_root+'/FindCompanyDocuments.do', params={'lang': 'EN', 'page_no': '1', 'company_search': ticker, 'document_selection': 5, 'industry_group': 'A', 'FromMonth': str(self.start_month), 'FromDate': str(self.start_day), 'FromYear':  str(self.start_year), 'ToMonth': str(self.end_month), 'ToDate': str(self.end_day), 'ToYear': str(self.end_year), 'Variable': 'Issuer', 'Search': 'Search'})

        # iso-8859-1 -> utf-8
        processed = feed.text.decode('iso-8859-1').encode('utf8')

        root = ET.fromstring(processed)
        print root


class Edgar():

    def __init__(self, start_date=None, end_date=None):
        self.org_root = "http://www.sec.gov"

        if start_date is None:
            self.start_date = datetime.date(1970, 01, 01)
        else:
            self.start_date = start_date

        if end_date is None:
            self.end_date = datetime.datetime.now().date()
        else:
            self.end_date = end_date

    def html_search(self, tree, types):

        grab_next = False
        tables = list(tree.iter("table"))

        try:
            for table in tables:
                if table.attrib['summary'] == "Document Format Files":
                    for row in table.findall('tr'):
                        for column in row.findall('td'):
                            if grab_next:
                                links = list(column.iter("a"))
                                for link in links:
                                    return link.attrib['href']
                                    break
                                grab_next = False
                            if column.text == types:
                                grab_next = True
        except UnicodeEncodeError:
            pass

    def ingest_stock(self, ticker):

        doc_types = ['10-K', '10-Q']
        to_parse = []

        for types in doc_types:
            feed = requests.get(self.org_root+'/cgi-bin/browse-edgar', params={'action': 'getcompany', 'CIK': ticker, 'type': types, 'count': 200, 'output': 'atom'})

            # iso-8859-1 -> utf-8
            processed = feed.text.decode('iso-8859-1').encode('utf8')

            try:
                ticker_feed = ET.fromstring(processed)
            except Exception, e:
                break
            root = ticker_feed

            for item in ticker_feed.findall('{http://www.w3.org/2005/Atom}entry'):
                html_url = item[1].find('{http://www.w3.org/2005/Atom}filing-href').text.encode('ascii','ignore')

                output = StringIO.StringIO(requests.get(html_url).text.encode('ascii','ignore'))
                tree = etree.parse(output, etree.HTMLParser())
        
                output = self.html_search(tree, types)
                if output and ".htm" in output:
                    to_parse.append(self.org_root+output)

        return to_parse
