#! /usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, print_function

import xml.etree.ElementTree as ET
from lxml import etree
import concurrent.futures
import requests
import re
import datetime

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class Ingestor():

    def file_downloader(self, urls, directory):
        """
        file_downloader asynchronously downloads all required documents using threads.
        By default the max number of threads running asynchronously is 5, but you can
        adjust this for your own system.
        """

        if urls is None or len(urls) == 0:
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
    """
    SEDAR is document filing and retrieval system used by the CSA (Canada)
    """

    def __init__(self, start_date=None, end_date=None):
        self.org_root = "http://www.sedar.com"

        if start_date is None:
            self.start_date = datetime.datetime(1970, 1, 1, 0, 0)
        else:
            self.start_date = datetime.strptime(self.start_date, "%y-%d-%m")

        self.start_month = self.start_date.month
        self.start_day = self.start_date.day
        self.start_year = self.start_date.year

        if end_date is None:
            self.end_date = datetime.datetime.now().date()
        else:
            self.end_date = datetime.strptime(self.end_date, "%y-%d-%m")

        self.end_month = self.end_date.month
        self.end_day = self.end_date.day
        self.end_year = self.end_date.year

    def ingest_stock(self, ticker):
        """
        ingest_stock essentially scrapes the site for the actual documents we need to download.
        It uses a ticker or keyword.
        """

        to_parse = []

        headers = {
            'User-Agent': 'DIY-FilingsResearch 0.1'
        }

        feed = requests.get(self.org_root+'/FindCompanyDocuments.do', params={'lang': 'EN', 'page_no': '1', 'company_search': ticker, 'document_selection': 5, 'industry_group': 'A', 'FromMonth': str(self.start_month), 'FromDate': str(self.start_day), 'FromYear':  str(self.start_year), 'ToMonth': str(self.end_month), 'ToDate': str(self.end_day), 'ToYear': str(self.end_year), 'Variable': 'Issuer', 'Search': 'Search'}, headers=headers)

        # utf-8
        processed = feed.text.encode('utf-8')
        try:
            root = ET.fromstring(processed)
        except ET.ParseError:
            return
        print(root)


class Edgar():
    """
    EDGAR is document filing and retrieval system used by the SEC (US)
    """

    filing_types = ['10-K', '10-Q']
    doc_types = {
        'html': ["Document Format Files", ".htm", filing_types],
        'xbrl': ["Data Files", ".xml", "XBRL INSTANCE DOCUMENT"]
        }

    def __init__(self, doc_type=None, start_date=None, end_date=None):
        self.org_root = "http://www.sec.gov"

        if start_date is None:
            self.start_date = datetime.datetime(1970, 1, 1, 0, 0)
        else:
            self.start_date = datetime.datetime.strptime(start_date, "%Y-%d-%m")

        if end_date is None:
            self.end_date = datetime.datetime.now().date()
        else:
            self.end_date = datetime.datetime.strptime(end_date, "%Y-%d-%m")

        if doc_type == "html":
            self.doc_type = Edgar.doc_types['html']
        else:
            self.doc_type = Edgar.doc_types['xbrl']

    def page_search(self, tree, types):
        """
        page_search finds the document url in the document listing file links.
        """

        grab_next = False
        tables = list(tree.iter("table"))

        try:
            for table in tables:
                if table.attrib['summary'] == self.doc_type[0]:
                    for row in table.findall('tr'):
                        for column in row.findall('td'):
                            if grab_next:
                                links = list(column.iter("a"))
                                for link in links:
                                    return link.attrib['href']
                                    break
                                grab_next = False
                            if column.text in self.doc_type[2]:
                                grab_next = True
        except UnicodeEncodeError:
            pass

    def ingest_stock(self, ticker):
        """
        ingest_stock essentially scrapes the site for the actual documents we need to download.
        It uses a ticker or keyword.
        """

        to_parse = []

        for types in self.doc_type[2]:
            feed = requests.get(self.org_root+'/cgi-bin/browse-edgar', params={'action': 'getcompany', 'CIK': ticker, 'type': types, 'dateb': str(self.start_date.strftime("%Y-%d-%m")), 'count': 200, 'output': 'atom'})

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
        
                output = self.page_search(tree, types)
                if output and self.doc_type[1] in output:
                    to_parse.append(self.org_root+output)

        return to_parse
