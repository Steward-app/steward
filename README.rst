Steward.app
=============

|docs| |ci| |coverage|

Lightweight maintenance DB. Still heavily in development.

.. contents:: :local:

Installation
------------

Python3.5 is the current minimum supported version of Python.

.. code:: console

       make dependencies # python requirements
       make proto # proto client libraries
       make app # frontend resources
       make run_backend -j 10 # run backend services with defaults
       make run_frontend # run frontend service with defaults


.. |docs| image:: https://readthedocs.org/projects/steward-app/badge/?version=latest
  :target: http://steward-app.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. |ci| image:: https://travis-ci.org/Steward-app/steward.svg?branch=master
  :target: https://travis-ci.org/Steward-app/steward
  :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/Steward-app/steward/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Steward-app/steward
  :alt: Coverage Status
