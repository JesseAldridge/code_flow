import re

import graphviz

import l0_get_func_call

'''
def foo():
    bar()

def bar():
    baz()
'''

class TextNode:
    def __init__(self, line):
        self.line = line
        self.parent = None
        self.children = []
        self.func_name = None

        if line:
            m = re.match('(def) ([a-zA-Z0-9_]+)\(.*?', line.strip())
            if m and m.group(2) != '__init__':
                self.func_name = m.group(2)
        self.func_call = l0_get_func_call.get_func_call(line)

def file_to_nodes(path):
    # Create a node for each line in the file.

    path = re.sub('.pyc$', '.py', path)
    with open(path) as f:
        text = f.read()
    text_root = curr_parent = TextNode('<top-level>')
    text_root.func_name = '<top-level>'
    text_root.num_spaces = -1
    for line in text.splitlines():
        curr_parent = line_to_node(curr_parent, line)
    return text_root

def line_to_node(curr_parent, line):
    # Create a new node and append to curr_parent.  Hierarchy defined by indentation.

    if line.strip() and not line.strip().startswith('#'):
        while len(line) - len(line.lstrip()) <= curr_parent.num_spaces:
            curr_parent = curr_parent.parent
        text_node = TextNode(line)
        text_node.parent = curr_parent
        curr_parent.children.append(text_node)
        if text_node.func_name:
            text_node.num_spaces = len(line) - len(line.lstrip())
            curr_parent = text_node
    return curr_parent


def each_node(root, funcs, depth):
    for func in funcs:
        func(root, depth)
    for child in root.children:
        each_node(child, funcs, depth + 1)

def print_tree(root, depth):
    print 'root: {} {:<10} | {:<10} | {}'.format(
        depth,
        root.func_name[:10] if root.func_name else '',
        root.func_call[:10] if root.func_call else '',
        root.line)

def build_call_graph():
    call_graph = {}

    def add_to_graph(node, depth):
        if node.func_name:
            call_graph.setdefault(node.func_name, [])
        if node.func_call:
            call_graph[node.parent.func_name].append(node.func_call)

    return call_graph, add_to_graph

if __name__ == '__main__':
    root_node = file_to_nodes(__file__)
    call_graph, add_to_graph = build_call_graph()
    each_node(root_node, [print_tree, add_to_graph], 0)

    dot = graphviz.Digraph()
    for caller, callees in call_graph.iteritems():
        dot.node(caller)
        for callee in callees:
            dot.edge(caller, callee)
    dot.render('out.dot')

