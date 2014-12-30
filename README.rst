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

- Python >= 2.6 or >= 3.3

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
