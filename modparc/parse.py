# -*- coding: utf-8 -*-

"""
parse
----------------------------------

High-level helper functions for the package
"""

from modparc.syntax.stored_definition import stored_definition
from modparc.syntax import tokenize


def parse(source_code):
    """
    Parse Modelica source code and return the parsed structure

    :param source_code: code lines to be parsed
    :return: an instance of StoredDefinition
    """
    tokens = tokenize(source_code)
    return stored_definition.parse(tokens)

def parse_file(source_file):
    """
    Parse Modelica source file and return the parsed structure

    :param source_file: Modelica source code file
    :return: an instance of StoredDefinition
    """
    with open(source_file, 'r') as file_object:
        mo_file_content = file_object.read()
        return parse(mo_file_content)
