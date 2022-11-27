from collections.abc import Iterable
from io import StringIO
import os
import cadquery as cq

TMP_STEP_FILE_PATH = "/tmp/stl_files/"

"""
Switch to current tmp folder and return the path
"""
def switch_to_tmp():
    _dir = os.getcwd()
    os.chdir(_dir + TMP_STEP_FILE_PATH)
    return os.getcwd()


def dfs(graph, node, visited_leafs):
    """Depth-first search (DFS) algorithm"""
    if node not in visited_leafs:
        if isinstance(
            node,
            (
                cq.occ_impl.shapes.Solid,
                cq.occ_impl.shapes.Shell,
                cq.occ_impl.shapes.Face,
            ),
        ):
            visited_leafs.add(node)

        if isinstance(node, Iterable):
            for n in node:
                dfs(graph, n, visited_leafs)

    return visited_leafs


"""
Generates the stl file entities
"""
def step2tsl(step_file, clear=True) -> dict:


     #Decode from bytes to string
    _step_file = step_file.decode("utf8")

    _dir = switch_to_tmp()

    #Write STEP contents into tmp file
    with open(_dir + "/patch.step", "w", newline='') as stream:
        stream.write(_step_file)
        stream.close()

    model = cq.importers.importStep(_dir + "/patch.step")

    # Export full model as a single STL
    cq.exporters.export(model, _dir+"/model.stl")
    
    compounds = model.objects
    shapes = dfs(compounds, compounds[0], set())

    sorted_by_mass = []
    sorted_by_name = []
    for i, shape in enumerate(shapes):
        sorted_by_mass.append(str(shape.centerOfMass(shape)))
        sorted_by_name.append(shape)

    sorted_by_mass, sorted_by_name = zip(*sorted(zip(sorted_by_mass, sorted_by_name)))

    for i, obj in enumerate(sorted_by_name):
        file_name = _dir+"/obj_"+str(i)+".stl"
        obj.exportStl(file_name)

    return {}

