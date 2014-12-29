#! /usr/bin/env python
# encoding: utf-8

from threadedSearch import Queryer, Indexer
from ingestor import Ingestor, Edgar, Sedar
import signal
import lucene

# before we quit we always want to close the writer to prevent corruptions to the index
def quit_gracefully(*args):
    queryer.writer.close()
    print "Cleaning up and terminating"
    exit(0)

# always declare the signal handler first
signal.signal(signal.SIGINT, quit_gracefully)

env=lucene.initVM()
queryer = Queryer("index", "hits")
print 'Using Directory: ', queryer.store_dir

# directory for storing downloaded docs
directoryToWalk = "docs"

# and start the indexer
# note the indexer thread is set to daemon causing it to terminate on a SIGINT
indexer = Indexer(queryer.store_dir, queryer.writer, directoryToWalk)
ingestor = Ingestor()
#edgar = Edgar()
sedar = Sedar()

with open('data.txt', 'r') as reader:
    for line in reader:
        ingestor.file_downloader(sedar.ingest_stock(line.rstrip()), directoryToWalk)
        #indexer.indexDocs()

# start up the terminal query interface
#queryer.run(queryer.writer, queryer.analyzer)

# if return from Querying then call the signal handler to clean up the writer cleanly
#quit_gracefully()
