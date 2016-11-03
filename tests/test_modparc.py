#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_modparc
----------------------------------

Tests for `modparc` module.
"""

from funcparserlib.parser import skip, finished

from modparc.syntax import tokenize
import modparc


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

def verify_parsed_result(source_code, parser,
                         subelement_type, subelement_code):
    """
    Verify the parsed result contain a predefined set of subelements

    :param source_code: code line to be parsed
    :param parser: parser to parse the code
    :param subelement_type: inspect all the subelement of this type
    :param subelement_code: reference result value for each subelement
    :return: returns nothing
    """
    tokens = tokenize(source_code)
    parsed_element = (parser + skip(finished)).parse(tokens)
    subelements = parsed_element.search(subelement_type)
    assert len(subelements) == len(subelement_code)
    for (i, parsed_subelements) in enumerate(subelements):
        assert parsed_subelements.code() == subelement_code[i]


def test_expression_simple1():
    source_code = r'x*(alpha-beta*y)'
    subelement_code = ['x * ( alpha - beta * y )', 'alpha - beta * y']
    subelement_type = 'Expression'
    verify_parsed_result(source_code, modparc.expressions.expression,
                         subelement_type, subelement_code)


def test_expression_simple2():
    source_code = r'k1*(phi2-phi1)+d1*der(phi2-phi1)'
    subelement_code = ['k1 * ( phi2 - phi1 ) + d1 * der ( phi2 - phi1 )',
                       'phi2 - phi1', 'phi2 - phi1']
    subelement_type = 'Expression'
    verify_parsed_result(source_code, modparc.expressions.expression,
                         subelement_type, subelement_code)



def test_expression_if1():
    source_code = r'if done then 0 else -9.81'
    subelement_code = ['if done then 0 else - 9.81', 'done', '0', '- 9.81']
    subelement_type = 'Expression'
    verify_parsed_result(source_code, modparc.expressions.expression,
                         subelement_type, subelement_code)


def test_expression_if2():
    source_code = r'reinit(v, -e*(if h<-eps then 0 else pre(v)))'
    subelement_code = ['reinit ( v , - e * ( if h < - eps '
                       + 'then 0 else pre ( v ) ) )',
                       'v', '- e * ( if h < - eps then 0 else pre ( v ) )',
                       'if h < - eps then 0 else pre ( v )', 'h < - eps',
                       '0', 'pre ( v )', 'v']
    subelement_type = 'Expression'
    verify_parsed_result(source_code, modparc.expressions.expression,
                         subelement_type, subelement_code)


def test_function_arguments():
    " Problem with the overloaded __or__ operator implementation bug "
    source_code = """
                  Text(
                    extent={{-100,-40},{100,-80}},
                    lineColor={0,0,0},
                    fillColor={255,255,255},
                    fillPattern=FillPattern.Solid,
                    textString="%name")
                  """
    subelement_code = ['extent = { { - 100 , - 40 } , { 100 , - 80 } }',
                       'lineColor = { 0 , 0 , 0 }',
                       'fillColor = { 255 , 255 , 255 }',
                       'fillPattern = FillPattern . Solid',
                       'textString = "%name"']
    subelement_type = 'NamedArgument'
    verify_parsed_result(source_code, modparc.expressions.function_arguments,
                         subelement_type, subelement_code)



def test_simple_equation():
    source_code =r'der(v) = if done then 0 else -9.81'
    subelement_code = ['v', 'if done then 0 else - 9.81', 'done',
                       '0', '- 9.81', ]
    subelement_type = 'Expression'
    verify_parsed_result(source_code, modparc.equations.equation,
                         subelement_type, subelement_code)


def test_if_equation():
    source_code = """
                  if init==InitializationOptions.FixedPopulation then
                    population = initial_population;
                  elseif init==InitializationOptions.SteadyState then
                    der(population) = 0;
                  else
                  end if
                  """
    subelement_code = ['population = initial_population',
                       'der ( population ) = 0']
    subelement_type = 'Equation'
    verify_parsed_result(source_code, modparc.equations.if_equation,
                         subelement_type, subelement_code)


