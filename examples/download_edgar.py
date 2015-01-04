#! /usr/bin/env python
# encoding: utf-8

import os
from ingestor import Ingestor, IngestorException, Edgar

ingestor = Ingestor()

# xbrl or html?
edgar = Edgar("xbrl")

docs_directory = "test"

# if the directory we will download files does not exist, create it
if not os.path.exists(docs_directory):
    os.mkdir(docs_directory)

# for every ticker in our input file, download all the relevant documents
with open('edgar_tickers.txt', 'r') as reader:
    for line in reader:
        ingestor.file_downloader(edgar.ingest_stock(line.rstrip()), docs_directory)
