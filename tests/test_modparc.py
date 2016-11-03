#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_modparc
----------------------------------

Tests for `modparc` module.
"""

# import pytest

from modparc.syntax import tokenize
from modparc import expressions
from modparc import equations


# @pytest.fixture
# def response():
#     """Sample pytest fixture.
#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
#
#
# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument.
#     """
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string



def test_expression_simple1():
    string = r'x*(alpha-beta*y)'
    expression = expressions.expression.parse(tokenize(string))
    result = ['x * ( alpha - beta * y )', 'alpha - beta * y']
    assert len(expression.search('Expression')) == len(result)
    for (i, parsed_expression) in enumerate(expression.search('Expression')):
        assert parsed_expression.code() == result[i]


def test_expression_simple2():
    string = r'k1*(phi2-phi1)+d1*der(phi2-phi1)'
    expression = expressions.expression.parse(tokenize(string))
    result = ['k1 * ( phi2 - phi1 ) + d1 * der ( phi2 - phi1 )',
              'phi2 - phi1', 'phi2 - phi1']
    assert len(expression.search('Expression')) == len(result)
    for (i, parsed_expression) in enumerate(expression.search('Expression')):
        assert parsed_expression.code() == result[i]

def test_expression_if1():
    string = r'if done then 0 else -9.81'
    expression = expressions.expression.parse(tokenize(string))
    result = ['if done then 0 else - 9.81', 'done', '0', '- 9.81']
    assert len(expression.search('Expression')) == len(result)
    for (i, parsed_expression) in enumerate(expression.search('Expression')):
        assert parsed_expression.code() == result[i]


def test_expression_if2():
    string = r'reinit(v, -e*(if h<-eps then 0 else pre(v)))'
    expression = expressions.expression.parse(tokenize(string))
    result = ['reinit ( v , - e * ( if h < - eps then 0 else pre ( v ) ) )',
              'v', '- e * ( if h < - eps then 0 else pre ( v ) )',
              'if h < - eps then 0 else pre ( v )', 'h < - eps',
              '0', 'pre ( v )', 'v']
    assert len(expression.search('Expression')) == len(result)
    for (i, parsed_expression) in enumerate(expression.search('Expression')):
        assert parsed_expression.code() == result[i]


def test_simple_equation():
    string = r'der(v) = if done then 0 else -9.81'
    equation = equations.equation.parse(tokenize(string))
    result = ['v', 'if done then 0 else - 9.81', 'done', '0', '- 9.81', ]
    assert len(equation.search('Expression')) == len(result)
    for (i, parsed_expression) in enumerate(equation.search('Expression')):
        assert parsed_expression.code() == result[i]


def test_if_equation():
    string = """
             if init==InitializationOptions.FixedPopulation then
               population = initial_population;
             elseif init==InitializationOptions.SteadyState then
               der(population) = 0;
             else
             end if;
             """
    if_equation = equations.if_equation.parse(tokenize(string))
    result = ['population = initial_population', 'der ( population ) = 0']
    assert len(if_equation.search('Equation')) == len(r esult)
    for (i, parsed_expression) in enumerate(if_equation.search('Equation')):
        assert parsed_expression.code() == result[i]
