# -*- coding: utf-8 -*-

import funcparserlib
import funcparserlib.lexer
from re import MULTILINE
import pprint

def tokenize(string):
    token_specs = [
        ('string', (r'"([^\\"]|\\.|[\r\n])*?"', MULTILINE)),
        ('q-ident', (r"'" + r'([a-zA-Z_0-9' +
                     r'!#%&()*+,\-\./:;<>=?@\[\]\^{}|~ ' +
                     r'\"\?\\\a\b\f\n\r\t\v]|\\.)*' + r"'",)),
        ('comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),
        ('comment', (r'//.*',)),
        ('newline', (r'[\r\n]+',)),
        ('whitespace', (r'[ \t\r\n]+',)),
        ('keyword', (r'('
                     r'algorithm|' + r'and|' + r'annotation|' + r'assert|'
                     r'block|' + r'break|' + r'class|' + r'connect|'
                     r'connector|' + r'constant|' + r'constrainedby|' +
                     r'der|' + r'discrete|' + r'each|' + r'else|' +
                     r'elseif|' + r'elsewhen|' + r'encapsulated|' +
                     r'end|' + r'enumeration|' + r'equation|'
                     r'expandable|' + r'extends|' + r'external|'
                     r'false|' + r'final|' + r'flow|' + r'for|' +
                     r'function|' + r'if|' + r'import|' + r'impure|' + r'in|'
                     + r'initial|' + r'inner|' + r'input|' + r'loop|'
                     r'model|' + r'not|' + r'operator|' + r'or|' + r'outer|' +
                     r'output|' + r'package|' + r'parameter|' + r'partial|' +
                     r'protected|' + r'public|' + r'pure|' + r'record|' +
                     r'redeclare|' + r'replaceable|' + r'return|' +
                     r'stream|' + r'then|' + r'true|' + r'type|' + r'when|'
                     r'while|' + r'within' + r')',)),
        ('ident', (r'[a-zA-Z_][a-zA-Z_0-9]*',)),
        ('number', (r'[+-]?\d+(\.\d+)?([eE]\d+)?',)),
        ('rel_op', (r'(<>|<=|>=|==)',)),
        ('rel_op', (r'[<>]',)),
        ('add_op', (r'(\.\+|\.-)',)),
        ('add_op', (r'[+\-]',)),
        ('mul_op', (r'(\.\*|\./)',)),
        ('mul_op', (r'[*/]',)),
        ('op', (r'[\[\]\.(){}\^+\-*/=\,;:]',)),
    ]
    inner_tokenize = funcparserlib.lexer.make_tokenizer(token_specs)
    useless = ['comment', 'newline', 'whitespace']

    return [tok for tok in inner_tokenize(string) if tok.type not in useless]


def get_all_models(root_path):
    import os
    file_list = [os.path.join(path, fn)
                 for path, _, filenames in os.walk(root_path)
                 for fn in filenames
                 if fn.endswith('.mo')]
    return file_list


def print_file(file_name, function=tokenize):
    with open(file_name, 'r') as f:
        content = f.read()
        results = function(content)
        pprint.pprint(results)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run it on modelica files')
    parser.add_argument('root_path', type=str, nargs='?',
                        help='Root path for Modelica libraries')

    args = parser.parse_args().__dict__

    if args.get('root_path') is None:
        MODELICA_PATH = "***REMOVED***/workspace/modelica/"
        root_path = MODELICA_PATH
    else:
        root_path = args['root_path']

    file_list = get_all_models(root_path)

    for file_name in file_list:
        print("File name is {0}".format(file_name))
        print_file(file_name, function=tokenize)
