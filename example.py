from data_generator.generator_settings import GeneratorSettings
from data_generator.recursive_descent_generator import Generator
from data_generator.serializers.latex_serializer import *

import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def run_generator():
    generator_settings = GeneratorSettings(
        ['+', '-', '*', '/'],
        ['x', 'y', 'z'],
        ['sin', 'cos'],
        max_depth=4
    )

    generator_settings.set_number_vs_variable_probability(numberP=0.7)
    generator_settings.set_generation_probability(descentP=0.3, expressionP=0.4, closeP=0.3)

    gen = Generator(generator_settings)

    expression = gen.generate_expression(100)


if __name__ == '__main__':
    run_generator()
