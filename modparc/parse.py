# -*- coding: utf-8 -*-

"""
parse
----------------------------------

High-level helper functions for the package
"""

from modparc.syntax.stored_definition import stored_definition


def parse(source_code):
    """
    Parse Modelica source code and return the parsed structure

    :param source_code: code lines to be parsed
    :return: an instance of StoredDefinition
    """
    return stored_definition.parse(source_code)
