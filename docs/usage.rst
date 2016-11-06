=====
Usage
=====

To use modparc in a project:

.. code-block:: python
   :linenos:
   :emphasize-lines: 4

    import modparc
    with open("your_modelica_file.mo", 'r') as f:
        modelica_source_code = f.read()
        model_definition = modparc.parse(modelica_source_code)

To use the `model_definition` instance:

.. code-block:: python
   :emphasize-lines: 1,3
   :lineno-start: 5

    all_equations = model_definition.search('Equation')
    for equation in all_equations:
        print(equation.code())  # The code of the equation as string

One could also parse a certain syntax element in Modelica:

.. code-block:: python
   :linenos:
   :emphasize-lines: 11-13

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

