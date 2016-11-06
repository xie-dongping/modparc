=====
Usage
=====

To use modparc in a project::

    import modparc
    with open("your_modelica_file.mo", 'r') as f:
        modelica_source_code = f.read()
        model_definition = modparc.parse(modelica_source_code)
