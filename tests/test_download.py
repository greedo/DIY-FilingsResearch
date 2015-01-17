#! /usr/bin/env python
# encoding: utf-8

from ingestor import Ingestor, Edgar, Sedar, IngestorException
import requests
import requests.utils
import os
import shutil
import sys
sys.path.insert(0, os.path.abspath('./'))
import pytest

docs_directory = "test"

ping_edgar = pytest.mark.skipif(os.system("ping -c 1 \
    " + Edgar().org_root.replace("http://", "")) != 0,
    reason="could not reach Edgar")


def setup_module():
    """ create folder for downloading docs """

    if not os.path.exists(docs_directory):
        os.mkdir(docs_directory)


@ping_edgar
def test_edgar_download_html():

    ingestor = Ingestor()
    edgar = Edgar("html", "2013-01-01")
    ingestor.file_downloader(edgar.ingest_stock("AAPL"), docs_directory)

    assert os.path.exists(docs_directory + "/a2124888z10-k.htm") is True


@ping_edgar
def test_edgar_download_xbrl():

    ingestor = Ingestor()
    edgar = Edgar("xbrl", "2014-01-01")
    ingestor.file_downloader(edgar.ingest_stock("AAPL"), docs_directory)

    assert os.path.exists(docs_directory + "/aapl-20130928.xml") is True


def test_sedar_create_html():
    ingestor = Ingestor()
    assert Sedar("html", "2010-01-01", "2014-01-01")


def test_sedar_create_xbrl():
    ingestor = Ingestor()
    assert Sedar("xbrl", "2010-01-01", "2014-01-01")


def test_sedar_ingest_xbrl():
    ingestor = Ingestor()
    sedar = Sedar("xbrl", "2010-01-01", "2014-01-01")

    headers = {
        'User-Agent': 'DIY-FilingsResearch 0.1'
    }

    initial_params = {
        'lang': 'EN',
        'page_no': 1,
        'company_search': 'blackberry',
        'document_selection': 26,
        'industry_group': 'A',
        'FromMonth': 1,
        'FromDate': 1,
        'FromYear': 2010,
        'ToMonth': 1,
        'ToDate': 1,
        'ToYear': 2014,
        'Variable': 'Issuer',
        'Search': 'Search'
    }

    session = requests.session()
    initial_request = session.post(Sedar().org_root + "/F\
     indCompanyDocuments.do", params=initial_params)
    processed = initial_request.text.encode('utf-8')
    cookies = requests.utils.dict_from_cookiejar(initial_request.cookies)

    assert cookies['BIGipServerP_R1_sedar_80'] is not None


def test_sedar_exception():
    ingestor = Ingestor()
    with pytest.raises(IngestorException):
        sedar = Sedar("xbrl", "1995-01-01")


def teardown_module():
    """ remove the folder for downloading docs """

    if os.path.exists(docs_directory):
        shutil.rmtree(docs_directory)
