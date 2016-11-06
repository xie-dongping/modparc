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

    def code(self):
        """
        Create a predefined representation of all the tokens in the instance

        :return: formatted tokens contained in the instance
        """
        return " ".join([tok.value for tok in self.search('Token')])

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

classes = ['Expression', 'SimpleExpression', 'LogicalExpression',
           'LogicalTerm', 'LogicalFactor', 'Relation',
           'ArithmeticExpression', 'Term', 'Factor', 'Primary', 'RelOp',
           'MulOp', 'AddOp', 'Name', 'NamedArgument', 'NamedArguments',
           'FunctionArgument', 'FunctionArguments', 'FunctionCallArgs',
           'ExpressionList', 'OutputExpressionList', 'Subscript',
           'ArraySubscript', 'ComponentReference', 'StringComment',
           'Annotation', 'Comment', "LanguageSpecification", "BasePrefix",
           "ExternalFunctionCall", "ClassDefinition", "Element", "ElementList",
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
           "ClassModification", "StoredDefinition", "Assertion"]

variables = globals()

for class_name in classes:
    variables[class_name] = type(class_name, (SyntaxElement,), {})
