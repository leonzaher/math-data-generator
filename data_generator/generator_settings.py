
class GeneratorSettings(object):
    """
    Class representing settings for data generator.
    """

    def __init__(self, operators, variables, functions, max_depth):
        self.operators: list = operators
        self.variables: list = variables
        self.functions: list = functions
        self.braces = ['(']

        self.max_depth = max_depth

        self.numberP = None
        self.variableP = None

        self.descentP = None
        self.expressionP = None
        self.closeP = None

    def set_generation_probability(self, descentP, expressionP, closeP):
        self.descentP = descentP
        self.expressionP = expressionP
        self.closeP = closeP

    def set_number_vs_variable_probability(self, numberP):
        self.numberP = numberP
        self.variableP = 1 - numberP
