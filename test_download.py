#! /usr/bin/env python
# encoding: utf-8

from ingestor import Ingestor, Edgar, Sedar
import os
import sys
sys.path.insert(0, os.path.abspath('python-xbrl'))
import pytest

from ingestor import Ingestor, Edgar, Sedar

docs_directory = "test"

if not os.path.exists(docs_directory):
    os.mkdir(docs_directory)

def test_download_html():
    
    ingestor = Ingestor()
    edgar = Edgar("html", "2014-03-20", "2014-05-20")
    ingestor.file_downloader(edgar.ingest_stock("AAPL"), docs_directory)

    assert os.path.exists(docs_directory+"/d694710d10q.htm")


def test_download_xbrl():

    ingestor = Ingestor()
    edgar = Edgar("xbrl", "2014-03-20", "2014-05-20")
    ingestor.file_downloader(edgar.ingest_stock("AAPL"), docs_directory)

    assert os.path.exists(docs_directory+"/aapl-20140329.xml")
