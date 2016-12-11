# -*- coding: utf-8 -*-
"""
syntax_element
----------------------------------

Each syntax element is defined as a class in the syntax_element module, to
enable basic formatting and query function for the parse tree.
"""


class SyntaxElement(object):
    """
    The class is a base implementation for all the syntax elements

    All the derived classes would inherit this syntax element, and they only
    differ in their names.

    The base implemenation provides possibility for inspection and querying
    the parsed syntax elements.
    """

    def __init__(self, elements):
        """
        Constructor used by `>>` operator after parsing

        This is a standard interface used in funcparserlib

        :param elements: the parsed subelements provided by parser
        """
        self.elements = elements

    def __str__(self):
        return "{0}({1})".format(type(self).__name__, str(self.elements))

    def __repr__(self):
        return self.__str__()

    def original_code(self):
        """
        Return the token arranged by original string with only space and
        newline, and leave out all trailing newline and spaces

        Intended for roundtripping

        :return: string contained in the instance
        """
        return SyntaxElement._create_string(self.search('Token'))

    def code(self):
        """
        Create a predefined representation of all the tokens in the instance

        :return: formatted tokens contained in the instance
        """
        ROW = 0
        COLUMN = 1

        tokens = self.search('Token')
        min_row_token = min(tokens, key=lambda t: t.start[ROW])
        min_row_position = min_row_token.start[ROW]
        min_column_token = min(tokens, key=lambda t: t.start[COLUMN])
        min_column_position = min_column_token.start[COLUMN]
        row_offset = 1 - min_row_position  # nominal start position is 1
        column_offset = 1 - min_column_position  # nominal start position is 1

        return SyntaxElement._create_string(tokens, row_offset, column_offset)

    @staticmethod
    def _create_string(tokens, row_offset=0, column_offset=0):
        """
        Return the token arranged by original string with only space and
        newline, and leave out all trailing newline and spaces with a
        predefined offset.

        :return: string created by the tokens and offset
        """
        def append_line(old_string, start_position, value):
            """
            :return: appended string at predefined positions
            """
            assert start_position >= len(old_string)
            no_of_missing_char = start_position - len(old_string) - 1
            old_string += ' ' * no_of_missing_char
            old_string += value
            return old_string
        ROW = 0
        COLUMN = 1
        return_results = []
        for token in tokens:
            token_row = token.start[ROW] + row_offset
            token_column = token.start[COLUMN] + column_offset
            if token_row > len(return_results):
                no_of_missing_lines = token_row - len(return_results)
                return_results.extend([''] * (no_of_missing_lines - 1))
                new_line = append_line('', token_column, token.value)
                return_results.append(new_line)
            else:
                old_line = return_results[token_row - 1]
                new_line = append_line(old_line, token_column, token.value)
                return_results[token_row - 1] = new_line

        return "\n".join(return_results)

    def search(self, type_name):
        """
        Create a predefined representation of all the tokens in the instance

        :param type_name: use the class name to find all matching subelements
        :return: list of found elements of the class type_name
        """
        found_elements = []
        SyntaxElement.find(self, type_name, found_elements)
        return found_elements

    @staticmethod
    def find(syntax_element, type_name, result):
        """
        Search the matching elements with pre-order tree trasversal

        :param syntax_element: the syntax element to be explored
        :param type_name: type name to be searched
        :param result: mutable list to store the results
        :return: no explicit return, communication through result variable
        """
        if type(syntax_element).__name__ == type_name:
            result.append(syntax_element)

        if hasattr(syntax_element, 'elements'):
            SyntaxElement.find(syntax_element.elements,
                               type_name, result)
        elif hasattr(syntax_element, '__getitem__'):
            for el in syntax_element:
                SyntaxElement.find(el, type_name, result)


class _Definition(SyntaxElement):
    """
    Base class for definition class, to support additional functionalities
    """

    def name(self):
        """
        :return: the name of the definition
        """
        token_name = self.search('ClassSpecifier')[0].elements[0]
        assert token_name.type == 'ident'

        return token_name.value

    def prefix(self):
        """
        :return: the prefix of the definition
        """
        class_prefix = self.search('ClassPrefixes')[0]

        return class_prefix.code()

    def class_type(self):
        """
        :return: the type of the definition
        """
        class_prefix = self.search('ClassPrefixes')[0]

        return class_prefix.elements[-1].value

classes = ['Expression', 'SimpleExpression', 'LogicalExpression',
           'LogicalTerm', 'LogicalFactor', 'Relation',
           'ArithmeticExpression', 'Term', 'Factor', 'Primary', 'RelOp',
           'MulOp', 'AddOp', 'Name', 'NamedArgument', 'NamedArguments',
           'FunctionArgument', 'FunctionArguments', 'FunctionCallArgs',
           'ExpressionList', 'OutputExpressionList', 'Subscript',
           'ArraySubscript', 'ComponentReference', 'StringComment',
           'Annotation', 'Comment', "LanguageSpecification", "BasePrefix",
           "ExternalFunctionCall", "Element", "ElementList",
           "Composition", "ClassSpecifier", "ClassPrefixes",
           "EnumerationLiteral", "EnumList", "ImportList", "ImportClause",
           "TypePrefix", "TypeSpecifier", "ConditionAttribute", "Declaration",
           "ComponentDeclaration", "ComponentList", "ComponentClause",
           "ForIndex", "ForIndices", "ConnectClause", "Equation", "IfEquation",
           "ForEquation", "WhileEquation", "WhenEquation", "Statement",
           "IfStatement", "ForStatement", "WhileStatement", "WhenStatement",
           "EquationSection", "AlgorithmSection", "ExtendsClause",
           "ConstrainingClause", "Modification", "ShortClassDefinition",
           "ComponentDeclaration1", "ComponentClause1", "ElementReplaceable",
           "ElementRedeclaration", "ElementModification",
           "ElementModificationOrReplaceable", "Argument", "ArgumentList",
           "ClassModification", "Assertion"]
definition_classes = ["ClassDefinition", "StoredDefinition"]

variables = globals()

for class_name in classes:
    variables[class_name] = type(class_name, (SyntaxElement,), {})

for class_name in definition_classes:
    variables[class_name] = type(class_name, (_Definition,), {})
