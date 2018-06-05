from treelib import Tree


def debug_serialize(tree: Tree):
    def recursive(node) -> str:
        result = ""

        for child in tree.children(node.identifier):
            result += "_" * tree.depth(node) + child.data + "\n"

            if child.tag == "function":
                result += recursive(child)

        return result

    return "Serialized tree view:\n" + recursive(tree.get_node(0))


def serialize(tree: Tree):
    def recursive(node) -> str:
        result = ""

        for child in tree.children(node.identifier):
            if child.tag == "operator" or child.tag == "expression":
                result += child.data
            elif child.tag == "function":
                result += "{}({})".format(child.data, recursive(child))

        return result
    return recursive(tree.get_node(0))
