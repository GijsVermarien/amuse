"""
MESA chooser
"""
import_successful = {"2208": False, "15140": False}
try:
    from amuse.community.mesa_r15140.interface import \
    MESAInterface as MESAInterface_15140
    from amuse.community.mesa_r15140.interface import MESA as MESA_15140
    import_successful["15140"] = True
except ModuleNotFoundError as exception:
    import_successful["15140"] = exception.args[0]

try:
    from amuse.community.mesa_r2208.interface import \
        MESAInterface as MESAInterface_2208
    from amuse.community.mesa_r2208.interface import MESA as MESA_2208
    import_successful["2208"] = True
except ModuleNotFoundError as exception:
    import_successful["2208"] = exception.args[0]

def check_if_mesa_imported(version):
    # First check if the version is supported in AMUSE
    if not str(version) in import_successful.keys():
        raise AttributeError(
            f"MESA version {version} is not supported by AMUSE"
        )
    # Then check if the correct version was imported succesfully
    if not (import_successful[str(version)] == True):
        raise (
            f"MESA version {version} could not be loaded. Orginal error: {import_successful[str(version)]}"
)

def MESAInterface(version="15140", **options):
    check_if_mesa_imported(version)    
    if str(version) == "2208":
        return MESAInterface_2208(**options)
    if str(version) == "15140":
        return MESAInterface_15140(**options)
    raise AttributeError(
            f"MESA version {version} is not supported by AMUSE"
        )


def MESA(version="15140", **options):
    check_if_mesa_imported(version)    
    if str(version) == "2208":
        return MESA_2208(**options)
    if str(version) == "15140":
        return MESA_15140(**options)
    raise AttributeError(
            f"MESA version {version} is not supported by AMUSE"
        )


Mesa = MESA
