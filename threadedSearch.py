#! /usr/bin/env python
# encoding: utf-8

# Multithreading Searcher and Indexer.
# One Thread Indexes new documents in the background
# while thread in the foreground waits for new user queries
# This searcher and indexer works from the terminal, simply start it.
# It begins indexing files in the directory you point it to.

# import needed system modules
import os
import threading

# Import necessary Py-Lucene modules
import lucene
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.util import Version
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import IndexWriterConfig, DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.search.highlight import Highlighter, QueryScorer
from org.apache.lucene.search.highlight import SimpleFragmenter
from org.apache.lucene.search.highlight import NullFragmenter
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from java.io import File


class Indexer(threading.Thread):

    # set some initial values for the class, the root directory to
    # start indexing and pass in a writer instance
    def __init__(self, root, writer, directoryToWalk):
        threading.Thread.__init__(self)
        self.root = root
        self.writer = writer
        self.directory = directoryToWalk

    def run(self):
        env.attachCurrentThread()
        self.indexDocs()

    # start indexing beginning at the root directory
    def indexDocs(self):
        for self.root, dirnames, filenames in os.walk(self.directory):
            for filename in filenames:
                try:
                    path = os.path.join(self.root, filename)
                    file = open(path)
                    contents = unicode(file.read(), 'iso-8859-1')
                    file.close()
                    doc = Document()
                    doc.add(Field("name", filename, TextField.TYPE_STORED))
                    doc.add(Field("path", path, TextField.TYPE_STORED))

                    if len(contents) > 0:
                        doc.add(Field("contents", contents,
                            TextField.TYPE_STORED))
                    else:
                        print "warning: the file is empty %s" % filename
                    self.writer.addDocument(doc)
                    self.writer.commit()
                except Exception, e:
                    print "Failed in indexDocs:", e


class Queryer():

    def __init__(self, store_dir, hits_dir, frags_dir=None):

        # store_dir is the location of our generated lucene index
        # hits_dir is the location of the highlighted document hits
        # frags_dif is the location of the document hit fragments - optional
        self.store_dir = store_dir
        self.hits_dir = hits_dir
        self.frags_dir = frags_dir

        if not os.path.exists(self.store_dir):
            os.mkdir(self.store_dir)

        if not os.path.exists(self.hits_dir):
            os.mkdir(self.hits_dir)

        if self.frags_dir is not None and not os.path.exists(self.frags_dir):
            os.mkdir(self.frags_dir)

        self.directory = SimpleFSDirectory(File(self.store_dir))

        # For now I just use the StandardAnalyzer
        self.analyzer = StandardAnalyzer(Version.LUCENE_43)
        config = IndexWriterConfig(Version.LUCENE_43, self.analyzer)

        self.writer = IndexWriter(self.directory, config)

    def run(self, writer=None, analyzer=None):

        if writer is None:
            writer = self.writer

        if analyzer is None:
            analyzer = self.analyzer

        searcher = IndexSearcher(DirectoryReader.open(\
        SimpleFSDirectory.open(File(self.store_dir))))
        while True:
            print
            print "Hit enter with no input to quit."
            command = raw_input("Query:")
            if command == '':
                return

            print "Searching for:", command
            query = QueryParser(Version.LUCENE_43, "contents",
                analyzer).parse(command)

            # We'll just show the top 10 matching documents for now
            scoreDocs = searcher.search(query, 10).scoreDocs
            print "%s total matching documents." % len(scoreDocs)

            # Highlight the matching text in red
            highlighter = Highlighter(SimpleHTMLFormatter('<b><font color\
            ="red">', '</font></b>'), QueryScorer(query))

            # Using NullFragmenter since we still want to see
            # the whole document
            highlighter.setTextFragmenter(NullFragmenter())

            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                tokenStream = analyzer.tokenStream("contents",
                    StringReader(doc.get("contents")))

                # arg 3: the maximum number of fragments
                # arg 4: the separator used to intersperse the
                # document fragments (typically "...")
                # arg 3 and 4 don't really matter with NullFragmenter
                result = highlighter.getBestFragments(tokenStream,
                    doc.get("contents"), 2, "...")

                if len(result) > 10:
                    file_handler = open(self.hits_dir + '/' + doc.get("name"),
                        'w+')
                    file_handler.write(result)

            # create hit fragments, if we want to show them
            # arg 1: fragment size
            highlighter.setTextFragmenter(SimpleFragmenter(200))

            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                tokenStream = analyzer.tokenStream("contents",
                    StringReader(doc.get("contents")))

                result = highlighter.getBestFragments(tokenStream,
                    doc.get("contents"), 2, "...")

                if len(result) > 10:
                    file_handler = open(self.frags_dir + '/' + doc.get("name"),
                        'w+')
                    file_handler.write(result)
