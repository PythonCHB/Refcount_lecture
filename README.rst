================
Refcount_lecture
================

This repository holds the source and examples for a lecture about 
about Python reference counting issues, and some of the solutions.

The lecture slides were developed with the "hieroglyph" package, which leverages the Restructured Text (RST) and the Spinx document generation system to make nice HTML slides from an easy to use text markup language.

https://github.com/nyergler/hieroglyph

Building
=========

You can bulid the slides yourelf from the source, if you have installed hieroglyph::

  pip install hieroglyph

Then you should be able to buld the slides with::
  make slides
(run in the ``Refcount_lecture`` directory)

The RST source for the slides are in::

  source/index.rst

The generated html is in::
  
  build/slides/index.html

Code Samples
=============

Code samples refered to in the slides are in::
  code

For questions, comments, etc, send me a note at:

PythonCHB@gmail.com

