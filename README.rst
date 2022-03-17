Sphinx-rstprog
======================================================================

Document simple programs with rst syntax and generate sphinx documentation.

Usage
----------------------------------------------------------------------

Add and configure in ``conf.py``::

  extensions += ['sphinxcontrib.rstprog']

  rstprog = [
    # ( extension, begin rstcomment, end rstcomment ),
    ('.gp', '/**', '**/' ),
    ('.c', '/**', '**/' ),
    ]

Installation
----------------------------------------------------------------------

In this repository

::
  
  pip3 install .

Tips
----------------------------------------------------------------------

If you do not want all files to be processed by sphinx, use
``exclude_patterns`` to restrict the paths. Example, to
process only files having extension ``.pub.c``

::

  exclude_patterns = ['*/*[!pub].c']

How does it work
----------------------------------------------------------------------

This extensions registers a new source parser to sphinx
(thanks to ``add_source_parser`` and ``add_source_suffix`` methods).

The parser adds to the usual rst parser a initial step which turns
rst comment segments inside program into code segments inside rst.
That is, a python file::

  /** first litt. prog. comment **/
  def foobar():
      pass
  /** second comment **/
  foobor()

is converted into the following rst::

  first litt. prog. comment

  .. code::
    
    def foobar():
      pass

  second comment

  .. code::

    foobor()

Future work
----------------------------------------------------------------------

- The parser could be improved (currently absolutely minimal and non robust).
- Special markers in the comments could by used to change the
  sphinx directive used, or pass options.
