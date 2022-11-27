import trimesh
import numpy as np
import os 

STL_PATH = os.getcwd() + "tmp/stl_files/"

def generate_mesh(
    f_min,
    f_max,
    port,
    pml_n,
    step_file,
    stl="model.stl",
    factor=30,
    factor_space=15,
    fraction=500,
    res_fraction=[6,6,6],
    cell_ratio=2,
    n=[3, 3, 3],
):

    # Generate mesh
    unit = 1000  # 1000 = mm
    c = 299792458
    lambda_min = unit * c / f_max

    max_cell = lambda_min / factor
    max_cell_space = lambda_min / factor_space
    min_cell = lambda_min / fraction

    # Fetch node coordinates
    vertices = trimesh.load(STL_PATH + stl).vertices

    nodes = len(vertices)
    #print(nodes)

    # Generate tetrahedral mesh (for large models)
    if False and nodes > 1000:
        os.system("gmsh -2 data/" + step_file + " -o data/tmp/" + stl)

        # Re-fetch node coordinates (coarser model)
        vertices = trimesh.load("data/tmp/" + stl).vertices

    vertices = [vertices[:, 0], vertices[:, 1], vertices[:, 2]]

    # Refine port
    vertices[0] = np.append(vertices[0], [port[0][0], port[1][0]])
    vertices[1] = np.append(vertices[1], [port[0][1], port[1][1]])
    vertices[2] = np.append(vertices[2], [port[0][2], port[1][2]])

    # Clear duplicate axis entries
    vertices[0] = np.unique(vertices[0])
    vertices[1] = np.unique(vertices[1])
    vertices[2] = np.unique(vertices[2])

    # Sort original vertices
    vertices[0] = np.sort(vertices[0])
    vertices[1] = np.sort(vertices[1])
    vertices[2] = np.sort(vertices[2])

    # Sample thin traces
    for i, axis in enumerate(vertices):
        for j, line in enumerate(axis):
            if j < len(axis)-1 and abs(axis[j+1] - axis[j]) < min_cell and axis[j+1] != axis[j]:
                axis[j] = (axis[j] + axis[j+1])/2
                axis[j+1] = axis[j]
        vertices[i] = np.sort(np.unique(axis))


    #vertices = [vertices[0],vertices[1],vertices[2]]
    x = vertices[0]
    y = vertices[1]
    z = vertices[2]

    mesh = [x, y, z]

    if nodes > 1000:
        x = [x[0], x[-1]]
        y = [y[0], y[-1]]
        z = [z[0], z[-1]]

    # Apply edge refinement
    res = [max_cell/res_fraction[0], max_cell/res_fraction[1], max_cell/res_fraction[2]]

    for i, axis in enumerate([x, y, z]):
        fine = np.array([])
        edge_refinements = np.array([-np.inf])
        for line in axis:
            edge_refinement = np.array([])
            for m in range(-n[i], n[i] + 1):
                edge_refinement = np.concatenate((np.array([line + m * res[i]]), edge_refinement))
            edge_refinement = np.sort(edge_refinement) ### PROBABLY not needed
            for edge in edge_refinement:
                if edge > np.max(edge_refinements)+min_cell or edge in axis:
                    fine = np.append(fine, edge)
                    
                #####edge_refinements = np.append(edge_refinements, edge)

        mesh[i] = np.sort(fine)

    # Add lambda/4 + PML padding cells for bounding box
    f_center = (f_min + f_max)/2
    lambda_center = unit * c / f_center
    padding = lambda_center / 8 + pml_n * max_cell_space

    mesh[0] = np.append([x[0] - padding], mesh[0])
    mesh[0] = np.append(mesh[0], x[-1] + padding)
    mesh[1] = np.append([y[0] - padding], mesh[1])
    mesh[1] = np.append(mesh[1], y[-1] + padding)
    mesh[2] = np.append([z[0] - padding], mesh[2])
    mesh[2] = np.append(mesh[2], z[-1] + padding)

    # Global refinement
    for i, axis in enumerate(mesh):
        # Add line to every vertex
        axis = np.unique(np.concatenate((np.unique(vertices[i]), axis)))
 
        to_delete = np.argwhere(np.ediff1d(axis) < min_cell) + 1
        q = 1
        axis_tmp = axis #.copy()
        to_delete_tmp = np.array([])
        while (np.argwhere(np.ediff1d(axis_tmp) < min_cell) + 1).size > 1:
            to_delete_tmp = np.delete(to_delete, np.arange(0, to_delete.size, q))
            axis_tmp = np.delete(axis, to_delete_tmp)
            q += 1
 
        if to_delete_tmp.size != 0:
            axis = np.delete(axis, to_delete_tmp)

        # Interior & exterior refinement
        j_tot = (np.argwhere(np.abs(np.ediff1d(axis)) >= max_cell) + 1).size
        for count, j in enumerate(
            (np.argwhere(np.abs(np.ediff1d(axis)) >= max_cell) + 1)
        ):
            if count != 0 and count != j_tot - 1: # Interior
                n = int(np.abs((axis[j - 1] - axis[j]) / max_cell) + 1)
            else: # Exterior
                n = int(np.abs((axis[j - 1] - axis[j]) / max_cell_space) + 1)
            delta = np.abs(axis[j - 1] - axis[j]) / n
            for k in range(n):
                axis = np.append(axis, axis[j - 1] + k * delta)
    
        # Assert no cell exceeds minimum cell size (e.g. 35 um trace thickness)
        axis = np.delete(axis, np.argwhere(np.ediff1d(axis) <= min_cell) + 1)

        axis = np.unique(axis)
        axis = np.sort(axis)
        axis = np.round(axis, 3)
        
        ###### add 35 micrometer traces
        #axis = np.unique(np.concatenate((np.unique(vertices[:,i]), axis)))
        axis = np.append(axis, [port[0][i], port[1][i]])

        mesh[i] = np.sort(np.unique(axis))



    return mesh
