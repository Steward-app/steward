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
       make run_backend -j 10 # run backend microservices with defaults (set ARGS to override partially or BE_ARGS to completely)
       make run_frontend # run frontend service with defaults (set FE_PORT)


API exploration
---------------
.. code:: console
  make run_backend_monolithic & # defaults assume MongoDB running on localhost
  evans -r
  steward@127.0.0.1:50051> show service # list services and their RPCs and request types
  steward@127.0.0.1:50051> service UserService # select service
  steward.UserService@127.0.0.1:50051> call ListUsers # perform a call

.. |docs| image:: https://readthedocs.org/projects/steward-app/badge/?version=latest
  :target: http://steward-app.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. |ci| image:: https://travis-ci.org/Steward-app/steward.svg?branch=master
  :target: https://travis-ci.org/Steward-app/steward
  :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/Steward-app/steward/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Steward-app/steward
  :alt: Coverage Status
