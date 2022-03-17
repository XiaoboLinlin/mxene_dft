import inspect
import os
import mbuild as mb
import pathlib
from pkg_resources import resource_filename

# def GetSolv(solv_name):
#     cache_dir = '/Users/xiaobolin/signac/acetone_li_xiaobo/src/util/lib/mol2/'
#     filename = '{}.mol2'.format(solv_name)
#     if any(file == filename for file in os.listdir(cache_dir)):
#         solv = mb.load(os.path.join(cache_dir, filename))
#         solv.name = solv_name
#     return solv

# def GetIL(il_name):
#     cache_dir = '/Users/xiaobolin/signac/acetone_li_xiaobo/src/util/lib/mol2/'
#     filename = '{}.mol2'.format(il_name)
#     if any(file == filename for file in os.listdir(cache_dir)):
#         il = mb.load(os.path.join(cache_dir, filename))
#         il.name = il_name

#     return il


# def Get_ff_path(ff_name):
#     """Get the path to a force field xml file """
#     """in a directory of the same name."""
#     cache_dir = '/Users/xiaobolin/signac/acetone_li_xiaobo/src/util/lib/'
#     ff_path = os.path.join(cache_dir, ff_name + '.xml')
#     return ff_path

import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

def GetSolv(solv_name):
    cache_dir = '{}/forcefield/mol2'.format(dir_path)
    filename = '{}.mol2'.format(solv_name)
    if any(file == filename for file in os.listdir(cache_dir)):
        solv = mb.load(os.path.join(cache_dir, filename))
        solv.name = solv_name
    return solv

def GetIL(il_name):
    cache_dir = '{}/forcefield/mol2'.format(dir_path)
    filename = '{}.mol2'.format(il_name)
    if any(file == filename for file in os.listdir(cache_dir)):
        il = mb.load(os.path.join(cache_dir, filename))
        il.name = il_name

    return il


def Get_ff_path(ff_name):
    """Get the path to a force field xml file """
    """in a directory of the same name."""
    cache_dir = '{}/forcefield'.format(dir_path)
    ff_path = os.path.join(cache_dir, ff_name + '.xml')
    return ff_path