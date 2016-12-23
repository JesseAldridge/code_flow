import os, glob

import l1_file_to_dot


def dir_to_call_graph(dir_path):
    # Generate call graph for each source file in directory.

    call_graph = {}
    file_paths = glob.glob(os.path.join(dir_path, '*.py'))
    print 'file_paths:', file_paths
    module_names = [
        os.path.basename(path).rsplit('.', 1)[0] for path in file_paths]
    global_root = l1_file_to_dot.TextNode('<top-level>', '')
    global_root.func_name = '<top-level>'
    for file_path in file_paths:
        file_root = l1_file_to_dot.file_to_nodes(file_path)
        global_root.children.extend(file_root.children)


        # for node_name in file_graph:
        #     new_name = node_name
        #     if('.' not in node_name or
        #        node_name.split('.', 1)[0] not in module_names):
        #         new_name = module_name + '.' + node_name
        #     call_graph[new_name] = file_graph[node_name]
        # for node_name, node in renamed_nodes.iteritems():
        #     call_graph[node_name] = node


    l1_file_to_dot.node_to_dot(global_root)


if __name__ == '__main__':
    dir_to_call_graph(os.path.dirname(__file__))
