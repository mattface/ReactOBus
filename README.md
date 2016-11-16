[![Build Status](https://travis-ci.org/ivoire/ReactOBus.svg?branch=master)](https://travis-ci.org/ivoire/ReactOBus) [![Coverage Status](https://coveralls.io/repos/github/ivoire/ReactOBus/badge.svg?branch=master)](https://coveralls.io/github/ivoire/ReactOBus?branch=master) [![Code Health](https://landscape.io/github/ivoire/ReactOBus/master/landscape.svg?style=flat)](https://landscape.io/github/ivoire/ReactOBus/master)

ReactOBus
========

ReactOBus is a message broker that helps to create software bus over the network
and to react to some messages.


Features
========

ReactOBus is able to:

* collect events (as network messages) from different sources
* publish the stream of events
* store the events in a database
* launch specific commands when an event match some conditions


In a near future, ReactOBus will be able to:

* filter-out some events
* modify on-the-fly event format
* ...


Using ReactOBus
===============

Requirements
------------

ReactOBus is known to work with Python3.4 and Python3.5 under Linux.

It depends on (see **requirements.txt**):

* pyzmq
* pyYAML
* SQLAlchemy (if you wish to store events in a database)
* setproctitle


Installing
----------

Executing ReactOBus directly from the sources:

    git clone https://github.com/ivoire/ReactOBus.git
    cd ReactOBus
    virtualenv -p python3.5 venv
    source venv/bin/activate
    pip install -r requirements.txt
    python reactobus.py --level DEBUG --conf share/examples/reactobus.yaml


Configuration
-------------

The configuration file is a YAML dictionnary with:

* *inputs*: a list of input streams
* *outputs*: a list of output streams
* *core*: configuration of the internal sockets
* *reactor*: the reacting part of ReactOBus
* *db*: the database configuration

All keys except *core* and *inputs* are optional. If the optional keys are not
found in the configuration, the corresponding modules won't be loaded.


Message format
--------------

For the moment, ReactOBus only accepts one type of messages. The messages
should be multipart ZMQ messages with the folowing meaning:

* **topic**
* **uuid** (as generated by uuid.uuid1() in Python)
* **datetime** when the message was generated (isoformat)
* **username** of the sending process or user
* **data** as JSON


Testing ReactOBus
=================

In order to run ReactOBus automatic tests, you will have to install *py.test*:

    pip install pytest

Then run the tests using:

    py.test tests -v
    [...]
    tests/test_core.py::test_core PASSED
    tests/test_db.py::test_run PASSED
    tests/test_db.py::test_errors PASSED
    [...]

On each push, the tests and the coverage are computed on:
* [Test results](https://travis-ci.org/ivoire/ReactOBus)
* [Coverage report](https://coveralls.io/github/ivoire/ReactOBus)
