# -*- coding: utf-8 -*-

class SyntaxElement(object):

    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return "{0}({1})".format(type(self).__name__, str(self.elements))

    def __repr__(self):
        return self.__str__()

    def code(self):
        return " ".join([tok.value for tok in self.search('Token')])

    def search(self, type_name):
        found_elements = []
        SyntaxElement.find(self, type_name, found_elements)
        return found_elements

    @staticmethod
    def find(syntax_element, type_name, result):
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
