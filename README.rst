MMD - Overview
===============

The Metamorphic Malware Detection app built for the SJSU CMPE-287 Spring 2019 course.

Builds
------

+---------------------+------------------------------------------------------------------------------------------+
| ``master``          | .. image:: https://travis-ci.com/karthikramasamy/cmpe287.svg?branch=master              |
|                     |     :target: https://travis-ci.com/karthikramasamy/cmpe287                              |
+---------------------+------------------------------------------------------------------------------------------+
| ``dev``             | .. image:: https://travis-ci.com/karthikramasamy/cmpe287.svg?branch=dev                 |
|                     |     :target: https://travis-ci.com/karthikramasamy/cmpe287                              |
+---------------------+------------------------------------------------------------------------------------------+

Code Coverage
-------------

+---------------------+------------------------------------------------------------------------------------------+
| ``master``          | .. image:: https://codecov.io/gh/karthikramasamy/cmpe287/branch/master/graph/badge.svg  |
|                     |     :target: https://codecov.io/gh/karthikramasamy/cmpe287                              |
+---------------------+------------------------------------------------------------------------------------------+
| ``dev``             | .. image:: https://codecov.io/gh/karthikramasamy/cmpe287/branch/dev/graph/badge.svg     |
|                     |     :target: https://codecov.io/gh/karthikramasamy/cmpe287                              |
+---------------------+------------------------------------------------------------------------------------------+

Install
-------

Download the source code::

    # clone the repository
    $ git clone https://github.com/karthikramasamy/cmpe287
    $ cd cmpe287

Install the application::

    $ pip install -e .

Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
