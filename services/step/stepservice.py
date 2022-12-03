from collections.abc import Iterable
from io import StringIO
import os
import cadquery as cq
from services.common.zipping.zipperhelper import zipfiles
from services.common.diroperations.dirservice import create_user_directory


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

    HARDCODED_USER_ID = 'user2'

    user_id = HARDCODED_USER_ID

    _dir = create_user_directory(HARDCODED_USER_ID)
    #Write STEP contents into tmp file
    with open(_dir + "/patch.step", "w", newline='') as stream:
        stream.write(step_file)
        stream.close()

    model = cq.importers.importStep(_dir + "/patch.step")

    compounds = model.objects
    shapes = dfs(compounds, compounds[0], set())

    sorted_by_mass = []
    sorted_by_name = []
    for i, shape in enumerate(shapes):
        sorted_by_mass.append(str(shape.centerOfMass(shape)))
        sorted_by_name.append(shape)

    sorted_by_mass, sorted_by_name = zip(*sorted(zip(sorted_by_mass, sorted_by_name)))

    file_names = []
    for i, obj in enumerate(sorted_by_name):
        file_name = _dir+"/obj_"+str(i)+".stl"
        file_names.append(file_name)
        obj.exportStl(file_name)
    
    return zipfiles(file_names, user_id)

