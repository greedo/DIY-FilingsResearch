|Travis-CI|

**DIY-FilingsResearch** is a library for analyzing complex company financial documents from the comfort of your own computer.

Installation
---------------

You will need to install the required libraries using the python package manager pip. If you do not have pip installed you can follow the directions `here <http://pip.readthedocs.org/en/latest/installing.html>`__

::

     pip install -r requirements.txt

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

.. |Travis-CI| image:: https://travis-ci.org/greedo/DIY-FilingsResearch.png?branch=master
   :target: https://travis-ci.org/greedo/DIY-FilingsResearch
