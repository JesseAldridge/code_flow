import re, os

import l0_get_func_call

'''
def foo():
    bar()

def bar():
    baz()
'''

class TextNode:
    def __init__(self, line, module_name):
        self.line = line
        self.parent = None
        self.children = []
        self.func_name = None

        if line:
            m = re.match('(def) ([a-zA-Z0-9_]+)\(.*?', line.strip())
            if m and m.group(2) != '__init__':
                self.func_name = m.group(2)
        self.func_call = l0_get_func_call.get_func_call(line)
        self.module_name = module_name

    def proper_func_name(self):
        return '{}.{}'.format(self.module_name, self.func_name) if self.func_name else None

    def proper_func_call(self):
        return '{}.{}'.format(self.module_name, self.func_call) if self.func_call else None

def file_to_nodes(path):
    # Create a node for each line in the file.

    module_name = os.path.splitext(os.path.basename(path))[0]

    def line_to_node(curr_parent, line):
        # Create a new node and append to curr_parent.  Hierarchy defined by indentation.

        if line.strip() and not line.strip().startswith('#'):
            while len(line) - len(line.lstrip()) <= curr_parent.num_spaces:
                curr_parent = curr_parent.parent
            text_node = TextNode(line, module_name)
            text_node.parent = curr_parent
            curr_parent.children.append(text_node)
            if text_node.func_name:
                text_node.num_spaces = len(line) - len(line.lstrip())
                curr_parent = text_node
        return curr_parent

    path = re.sub('.pyc$', '.py', path)
    with open(path) as f:
        text = f.read()
    text_root = curr_parent = TextNode('<top-level>', '')
    text_root.func_name = '<top-level>'
    text_root.num_spaces = -1
    for line in text.splitlines():
        curr_parent = line_to_node(curr_parent, line)
    return text_root


def each_node(root, funcs, depth):
    for func in funcs:
        func(root, depth)
    for child in root.children:
        each_node(child, funcs, depth + 1)

def print_tree(root, depth):
    print 'root: {} {:30} | {:<30} | {}'.format(
        depth,
        root.proper_func_name()[:30] if root.func_name else '',
        root.proper_func_call()[:30] if root.func_call else '',
        root.line[:60])

def build_add_to_graph():
    caller_to_callees = {}
    callee_to_callers = {}

    def add_to_graph(node, depth):
        name, call = node.proper_func_name(), node.proper_func_call()
        if name:
            caller_to_callees.setdefault(name, [])
        if call:
            parent_name = node.parent.proper_func_name()
            caller_to_callees[parent_name].append(call)
            callee_to_callers.setdefault(call, [])
            callee_to_callers[call].append(parent_name)

    return caller_to_callees, callee_to_callers, add_to_graph

def node_to_dot(root_node):
    caller_to_callees, callee_to_callers, add_to_graph = build_add_to_graph()
    # each_node(root_node, [print_tree, add_to_graph], 0)
    each_node(root_node, [add_to_graph], 0)
    roots = set(caller_to_callees.keys()) - set(callee_to_callers.keys())
    import pdb; pdb.set_trace()


    # def base_name(full_name):
    #     return full_name.split('.', 1)[1] if '.' in full_name else full_name




    # dot = graphviz.Digraph()
    # for caller_name, callee_names in call_graph.iteritems():
    #     dot.node(caller_name, base_name(caller_name))
    #     for callee_name in callee_names:
    #         dot.edge(caller_name, callee_name)
    # dot.render('out.dot')
    # return call_graph


if __name__ == '__main__':
    root_node = file_to_nodes(__file__)
    node_to_dot(root_node)
