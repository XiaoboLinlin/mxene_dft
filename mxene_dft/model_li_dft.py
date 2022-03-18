import mbuild as mb
import numpy as np
from foyer import Forcefield
from mxene_dft.get_sol_il_xml import GetSolv, GetIL, Get_ff_path
# import environment_for_nersc
# import environment_for_rahman
# from mxenes.utils.utils import get_fn, parse_nonbond_txt, collapse_atomtypes
from mxenes.structures import build_structure
from mxenes.lattices import Ti3C2Offset
from mxenes.structures import change_charge
import parmed as pm
from mbuild.formats import lammpsdata

def make_mxene_dft(length_abovetop = 4, d_spacing = 2, for_md=False, if_save = False, x_repeat = 2, y_repeat = 2):
    """make mxene with li ions above it
    Args:
        length_abovetop (int, optional): 
            The distance of Li ions above the outmost layer of MXene. Defaults to 4 (angstrom).
        d_spacing (int, optional):
            the d-spacing for mxene. Defaults to 2 (nm).
        for_md (boolen):
            If generate parmed structure for MD, large structure than dft. Default to False.
        if_save (boolen):
            If save the structure to .gro and .top and .data
    Returns:
        Parmed structure
    """
    print(d_spacing)

    displacements = d_spacing - 1.95462 / 2
    composition = {"O": 0, "OH": 1, "F": 0}
    ti3c2 = build_structure(
        lattice=Ti3C2Offset,
        periods=[x_repeat, y_repeat, 1],
        displacement = displacements,
        composition=composition,
        lateral_shift=True,
        atomtype=True,
    )

    #####
    del ti3c2.bonds[:]
    del ti3c2.angles[:]
    #####

    def find_center(coord):
        max_value = np.amax(coord)
        min_value = np.amin(coord)
        length = max_value - min_value
        center = min_value + length/2
        return center

    def center_coord(coord):
        center = np.array([find_center(coord[:,0]), 
                        find_center(coord[:,1]), 
                        find_center(coord[:,2])])
        return center

    coord = ti3c2.coordinates
    center = center_coord(coord)

    def delete_top_atom(ti3c2):
        i = 1
        while(i!=0):
            i = 0
            for atom in ti3c2.atoms:
                if atom.xz>center[2]:
                    del ti3c2.atoms[atom.idx]
    #                 print(atom.xz)
                    i = i +1
        return ti3c2

    ti3c2 = delete_top_atom(ti3c2)
    ti3c2 = change_charge(ti3c2, -9, atom_type='mxene_001')

    cation = GetIL("li")
    cation.name = "li"

    opls_li = Get_ff_path('opls_ions')
    opls_li = Forcefield(opls_li)
    liPM = opls_li.apply(cation, residues = 'li')

    for atom in liPM:
        atom.xx = center[0]
        atom.xy = center[1]
        atom.xz = np.amax(ti3c2.coordinates[:,2]) + length_abovetop
        
    structure_sub = ti3c2 + liPM
    # structure_sub = ti3c2
    
    if for_md:
        ### set 3*3 replicate for MD
        structure = pm.structure.Structure()
        series = [0,1,2]
        for y in series:
            for x in series:
                structure_sub_copy = structure_sub.__copy__()
                for atom in structure_sub_copy.atoms:
                    atom.xx = atom.xx + x * ti3c2.box[0]
                    atom.xy = atom.xy + y * ti3c2.box[1]
                structure = structure + structure_sub_copy 
        structure.box = [ti3c2.box[0]*3, ti3c2.box[1] * 3, ti3c2.box[2], 90, 90, 90]
    else:
        structure = structure_sub

    if if_save:
        structure.save(
                    "system.top",
                    combine='all',
                    overwrite=True
                    )
        structure.save(
                    "system.gro",
                    combine='all',
                    overwrite=True
                        )

        lammpsdata.write_lammpsdata(structure,
                                    filename = "model_data")

        # from mbuild.formats import vasp
        # structure_vasp = mb.conversion.from_parmed(structure)
        # structure_vasp._box._vectors = structure_vasp.box.vectors * 10
        # vasp.write_poscar(structure_vasp, 'POSCAR')

        structure_vasp = mb.load(structure)
        from mxene_dft import vasp_modify
        box = structure.get_box()[0]
        brav = [[box[0],0,0],[0, box[1],0],[0,0,box[2]]]
        vasp_modify.write_poscar(structure_vasp, "POSCAR_{}A".format(length_abovetop),lattice_constant=1.0, bravais=brav)

    return structure