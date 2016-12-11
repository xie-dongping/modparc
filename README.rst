===============================
modparc
===============================


.. image:: https://img.shields.io/pypi/v/modparc.svg
        :target: https://pypi.python.org/pypi/modparc

.. image:: https://img.shields.io/travis/xie-dongping/modparc.svg
        :target: https://travis-ci.org/xie-dongping/modparc

.. image:: https://readthedocs.org/projects/modparc/badge/?version=latest
        :target: https://modparc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/xie-dongping/modparc/shield.svg
     :target: https://pyup.io/repos/github/xie-dongping/modparc/
     :alt: Updates


modparc is a Modelica parser in Python based on parser combinator.


* Free software: GNU General Public License v3
* Source code: https://github.com/xie-dongping/modparc.
* Documentation: https://modparc.readthedocs.io.

.. contents::

Quickstart
----------

Install the package from PyPI:

.. code-block:: bash

    $ pip install modparc


To parse a Modelica source file `"your_modelica_file.mo"`:

.. code-block:: python

    import modparc
    with open("your_modelica_file.mo", 'r') as f:
        modelica_source_code = f.read()
        model_definition = modparc.parse(modelica_source_code)

To use the `model_definition` instance:

.. code-block:: python

    all_equations = model_definition.search('Equation')
    for equation in all_equations:
        print(equation.code())  # The code of the equation as string

One could also parse a certain syntax element in Modelica:

.. code-block:: python

    import modparc
    from modparc.syntax import tokenize
    source_code = """
                  if init==InitializationOptions.FixedPopulation then
                    population = initial_population;
                  elseif init==InitializationOptions.SteadyState then
                    der(population) = 0;
                  else
                  end if
                  """
    tokens_list = tokenize(source_code)
    if_equation_element = modparc.syntax.equations.if_equation(tokens_list)
    sub_equations = if_equation_element.search('Equation')
    for equation in sub_equations:
        print(equation.code())  # The code of the equation as string



Features
--------

* Experimentally parses Modelica Standard Library 3.2.1
* Search element of a certain class

Known Issues
------------

* Handling tokenization of Q-IDENT and comments, which comes first?
* Assertion syntax not defined in Modelica specification
* Default recursion depth is not enough for long vector literals
* Cyclic import is neccessary for the Modelica syntax definition

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

