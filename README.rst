|PyPI version| |Travis-CI|

**DIY-FilingsResearch** is a library for analyzing complex company financial documents from the comfort of your own computer.

Installation
------------

The easiest way to install DIY-FilingsResearch is with pip

::

    sudo pip install DIY-FilingsResearch
    
Made sure your **sys.path** is correct. Note it is currently just a collection of scripts.

Requirements
------------

- Python >= 2.7 or >= 3.3

Initialization
--------------

To start using the library, first import ``Ingestor`` and ``Edgar``

::

    from ingestor import Ingestor, Edgar

``Edgar`` (US) and ``Sedar`` (Canada) are currently supported. Note however that the flows are a bit different.
See the note at the bottom about the ``Sedar`` flow.

Simple Download Workflow
-----------------------

First specific what kind of files using the new ``Edgar`` basic object

::

    ingestor = Ingestor()
    edgar = Edgar("xbrl")

``xbrl`` or ``html`` are currently supported

Then pass ``ingest_stock()`` with a stock ticker to ingest and a directory to store the downloaded docs into 
``file_downloader()``

::

    ingestor.file_downloader(edgar.ingest_stock("AAPL"), downloaded_docs_directory)

Sedar Download Workflow Note
-----------------------

The ``Sedar`` workflow is very similar to the ``Edgar`` workflow except that you will see a browser window 
launched. This is to capture cookies. Once the browser is launched you will need to click on a document link 
on the page. This will open up a CAPTCHA window. Solve the CAPTCHA and then close all the browser windows. 
The downloader should proceed normally assumed you solved the CAPTCHA correctly.

Testing
-------

To run the unit tests, you need pytest

::

    pip install pytest

Once you have that, ``cd`` into the root directory of this repo and

::

    py.test --tb=line -vs

License
-------

::

    Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the license.

.. |PyPI version| image:: https://badge.fury.io/py/DIY-FilingsResearch.png
   :target: http://badge.fury.io/py/DIY-FilingsResearch
.. |Travis-CI| image:: https://travis-ci.org/greedo/DIY-FilingsResearch.png?branch=master
   :target: https://travis-ci.org/greedo/DIY-FilingsResearch
