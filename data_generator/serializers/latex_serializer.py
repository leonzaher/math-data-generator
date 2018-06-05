from pytexit import py2tex
from sympy import preview


def generate_latex(expression: str):
    return py2tex(expression)


def generate_lates_image(expression: str, path: str):
    tex = generate_latex(expression)

    preview(tex, viewer='file', output='png', filename=path)