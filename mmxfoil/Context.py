# Context.py


class Context(object):
    """manages data passed between commands"""

    model = "hodson-wart"
    airfoil = "simplex"  # default airfoil passed to XFoil
    propfile = "default_prop"  # default prop file in data dir
    motorfile = "default_motor"  # default motorfile in data dir
    data_dir = "data"  # directory holding data files
    airfoil_data = ()
    model_data = {}
    argcount = 0
    debug = False
    CL = []
    CD = []
    CM = []
