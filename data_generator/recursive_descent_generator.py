from .generator_settings import GeneratorSettings
from treelib import Tree, Node

from .serializers import string_serializer

import logging
import numpy as np
import math


class Generator(object):
    def generate_expression(self, length: int) -> str:
        self.state = State(target_len=length, root_node=Node(tag="root", identifier=0))

        logging.debug("Starting generation...")

        self.__choose_generation_type()

        self.__fix_length()

        logging.debug(string_serializer.debug_serialize(self.state.tree))

        logging.info("Result: {}".format(string_serializer.serialize(self.state.tree)))

        return string_serializer.serialize(self.state.tree)

    def __choose_generation_type(self):
        gen = self.generator_settings

        logging.debug("{}{}   {}".format("_" * self.state.tree.depth(self.state.current_node),
                                         str(self.state.current_node.data), self.state.current_len))

        while self.state.current_len < self.state.target_len:

            spaces_left = self.state.target_len - self.state.current_len

            # if we are at depth x and we can only fill x more spaces, we will exit, because there is no more space
            if spaces_left == self.state.tree.depth(self.state.current_node):
                return
            elif spaces_left < self.min_function_length + 2:
                # if we cannot fit a function, we won't
                self.generation_functions.get('expression')()
            else:
                # if we can fit anything, we will choose randomly
                choice = np.random.choice(
                    a=['descend', 'expression', 'close'],
                    p=[gen.descentP, gen.expressionP, gen.closeP]
                )

                self.generation_functions.get(choice)()

    def __append_operator_if_needed(self):
        if not self.state.current_node.is_leaf():
            operator = np.random.choice(self.generator_settings.operators)

            self.state.current_len += 1

            self.state.tree.create_node(tag="operator", identifier=self.__get_node_identifier(),
                                        parent=self.state.current_node, data=operator)

    def __descend(self):
        # since functions have certain length, we cannot descend further if they will surpass the set length
        if self.state.current_len + self.min_function_length + 2 >= self.state.target_len:
            return

        # if we reached max depth, we cannot descend further
        if self.state.tree.depth(self.state.current_node) == self.generator_settings.max_depth:
            return

        self.__append_operator_if_needed()

        expression = self.__choose_descent_function()

        current_node = self.state.tree.create_node(tag="function", identifier=self.__get_node_identifier(),
                                                   parent=self.state.current_node, data=expression)

        self.state.current_len += len(expression) + 2  # add 2 because we count opening and closing parentheses

        self.state.current_node = current_node

        self.__choose_generation_type()

    def __expression(self):
        self.__append_operator_if_needed()

        gen = self.generator_settings

        expr_len = np.random.randint(1, 5)
        expression = ""

        while len(expression) < expr_len:
            choice = np.random.choice(
                a=['num', 'var'],
                p=[gen.numberP, gen.variableP]
            )

            if expr_len - len(expression) == 2:
                # if 2 letters are missing until expression is complete, we can only fill it with number with length 2
                expression += str(number(2))
                break
            elif choice == 'num':
                num_len = np.random.randint(1, 10)

                # we must keep expression length in check
                if len(expression) + num_len > expr_len:
                    num_len = expr_len - len(expression)

                expression += str(number(num_len))
            elif choice == 'var':
                expression += np.random.choice(gen.variables)

            expression += np.random.choice(gen.operators)

        # remove last operator
        expression = str(expression[:-1])

        self.state.tree.create_node(tag="expression", identifier=self.__get_node_identifier(),
                                    parent=self.state.current_node, data=expression)

        self.state.current_len += len(expression)

    def __close(self):
        current_node = self.state.current_node

        # we cannot close the root node
        if current_node.tag == "root":
            return

        # function nodes need at least one child
        if current_node.tag == "function" and current_node.is_leaf():
            return

        self.state.current_node = self.state.tree.parent(current_node.identifier)

    def __fix_length(self):
        # delete or add additional data if needed

        length_diff = self.state.current_len - self.state.target_len

        if length_diff == 0:
            return

        while length_diff > 0:
            # we need to delete some data
            for node in self.state.tree.all_nodes_itr():
                if node.tag == "expression" and len(node.data) > 1:
                    data_len = len(node.data)
                    node.data = node.data[0:1]
                    length_diff -= data_len - 1
                    break

        while length_diff < 0:
            # we need to add some data
            for node in self.state.tree.all_nodes_itr():
                if node.tag == "expression":
                    node.data += str(number(-length_diff))
                    length_diff = 0
                    break

    def __choose_descent_function(self):
        return str(np.random.choice(a=self.generator_settings.functions))

    def __get_node_identifier(self) -> int:
        current_id = self.state.node_count

        self.state.node_count += 1

        return current_id

    def __init__(self, generator_settings: GeneratorSettings):
        self.generator_settings: GeneratorSettings = generator_settings

        self.state: State = None

        self.generation_functions = {
            "descend": self.__descend,
            "expression": self.__expression,
            "close": self.__close
        }

        self.min_function_length = len(min(generator_settings.functions, key=len))  # get shortest function length


class State(object):
    def __init__(self, target_len, root_node):
        self.target_len: int = target_len
        self.current_len: int = 0

        self.current_node = root_node
        self.node_count: int = 1

        self.tree: Tree = Tree()
        self.tree.add_node(root_node)


def number(len: int):
    """
    Generate number whose string representation is of length size. In other words, following stands:
       len(str(num)) == size
    """
    return np.random.randint(
        int(math.pow(10, len - 1)),
        int(math.pow(10, len) - 1))
