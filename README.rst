# Sphinx-rstprog

Document simple programs with rst syntax and generate sphinx documentation.

## Usage

Add and configure in ``conf.py``::

  extensions += ['sphinxcontrib.rstprog']

  rstprog = [
    # ( extension, begin rstcomment, end rstcomment ),
    ('.gp', '/**', '**/' ),
    ('.c', '/**', '**/' ),
    ]

## Installation

In this repository

::
  
  pip3 install .

## Tips

If you do not want all files to be processed by sphinx, use
``exclude_patterns`` to restrict the paths. Example, to
process only files having extension ``.pub.c``

::

  exclude_patterns = ['*/*[!pub].c']

