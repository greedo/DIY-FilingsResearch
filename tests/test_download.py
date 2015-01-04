#! /usr/bin/env python
# encoding: utf-8

from ingestor import Ingestor, Edgar, Sedar, IngestorException
import os
import shutil
import sys
sys.path.insert(0, os.path.abspath('./'))
import pytest

from ingestor import Ingestor, Edgar, Sedar

docs_directory = "test"

ping = pytest.mark.skipif(os.system("ping -c 1 " + Edgar().org_root.replace("http://", "")) != 0,
                          reason="could not reach Edgar")

def setup_module():
    """ create folder for downloading docs """

    if not os.path.exists(docs_directory):
        os.mkdir(docs_directory)

@ping
def test_edgar_download_html():
    
    ingestor = Ingestor()
    edgar = Edgar("html", "2013-01-01")
    ingestor.file_downloader(edgar.ingest_stock("AAPL"), docs_directory)

    assert os.path.exists(docs_directory+"/a2124888z10-k.htm") == True

@ping
def test_edgar_download_xbrl():

    ingestor = Ingestor()
    edgar = Edgar("xbrl", "2014-01-01")
    ingestor.file_downloader(edgar.ingest_stock("AAPL"), docs_directory)

    assert os.path.exists(docs_directory+"/aapl-20130928.xml") == True

def test_sedar_create_html():
    ingestor = Ingestor()
    assert Sedar("html", "2010-01-01", "2014-01-01")

def test_sedar_create_xbrl():
    ingestor = Ingestor()
    assert Sedar("xbrl", "2010-01-01", "2014-01-01")

def test_sedar_exception():
    ingestor = Ingestor()
    with pytest.raises(IngestorException):
        sedar = Sedar("xbrl", "1995-01-01")

def teardown_module():
    """ remove the folder for downloading docs """

    if os.path.exists(docs_directory):
        shutil.rmtree(docs_directory)
