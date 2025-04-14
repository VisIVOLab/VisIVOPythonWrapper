# VisIVOPythonWrapper Code
import subprocess
import logging

def set_logging(show_debug=False):
    if show_debug not in (True, False, 0, 1):
        raise ValueError("show_debug must be True, False, 0, or 1")
    show_debug = bool(show_debug)
    print(f"Debug: {show_debug}")
    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        level=logging.DEBUG if show_debug else logging.INFO
    )
    if show_debug:
        logging.debug("Debug logging is enabled.")

def corefunction(comm, input_file, *flags, mpi=False, options=None):
    command = [comm]
    logging.debug("Initialize command as a list")
    
    tasks = options.pop("tasks", 1)
    logging.debug(f"Retrieves the number of processors (n) from options, defaulting to 1 if not provided.")
    logging.debug(f"The pop() method removes 'tasks' from options to prevent further conflicts.")
    logging.debug(f"Extract number of tasks: {tasks}")


    worked_options = {}
    if options:
        for key, (val, expected_type) in options.items():
            if val is not None:
                if not isinstance(val, expected_type):
                    raise TypeError(f"'{key}' must be of type {expected_type.__name__}")
                if expected_type is bool:
                    if val:  # add only if True
                        worked_options[key] = val
                else:
                    worked_options[key] = val

    for flag in flags:
        command.append(f"--{flag}") # Ensure flags are added properly


    for option, value in worked_options.items():
        if isinstance(value, (list, tuple)):
            command.append(f"--{option}")
            command.extend(map(str, value))
        elif value and type(value) != bool:
            command.append(f"--{option}")
            command.append(str(value))
        else:
            if value != False:
                command.append(f"--{option}")

    
    command.append(input_file)
    logging.debug(f"Final Command: {' '.join(command)}")


    if mpi:
        mpi_command = ["mpirun", "-n", str(tasks), "--oversubscribe", "--mca", "opal_warn_on_missing_libcuda", "0"] + command
        logging.debug(f"Running MPI command: {mpi_command}")
        result = subprocess.run(mpi_command, capture_output=True, text=True)
    else:
        logging.debug(f"Running command: {command}")
        result = subprocess.run(command, capture_output=True, text=True)

    

    if result.stderr.strip():
        logging.info(f"STDOUT: {result.stdout.strip() or 'Error Found'}")
        logging.error(f"STDERR: {result.stderr.strip()}")
    else:
        logging.info(f"STDOUT: {result.stdout.strip() or 'Output Successfully Generated'}")
        logging.error("STDERR: No Error Found")

def importer(input_file, *flags, mpi=False, fformat=None, out=None, volume=None, compx=None, compy=None, compz=None, sizex=None, sizey=None, sizez=None, userpwd=None, binaryheader=None, missingvalue=None,textvalue=None, bigendian=False, double=False, npoints=None, history=True, historyfile=None): 
    
    options = {
        "fformat": (fformat, str),
        "out": (out, str),
        "volume": (volume, str),
        "compx": (compx, float),
        "compy": (compy, float),
        "compz": (compz, float),
        "sizex": (sizex, float),
        "sizey": (sizey, float),
        "sizez": (sizez, float),
        "userpwd": (userpwd, str),
        "binaryheader": (binaryheader, str),
        "missingvalue": (missingvalue, float),
        "textvalue": (textvalue, float),
        "npoints": (npoints, int),
        "historyfile": (historyfile, str),
        "bigendian": (bigendian, bool),
        "double": (double, bool),
        "history": (history, bool),
    }

    

    logging.info(f"Executing VisIVOImporter with file: {input_file}")
    command = "VisIVOImporter"

    corefunction(command, input_file, *flags, mpi=mpi, options=options)


def filter(input_file, *flags, mpi=False,
           op=None, perc=None, field=None, iseed=None, out=None, outcol=None, start=None, append=False,
           filelist=None,
           newnames=None, limits=None, operator=None, threshold=None, skip=None, listfile=None,
           geometry=None, background=None, center=None, radius=None, multilist=None, binaryint=False,
           asciilist=False, numberlists=None, listelements=None, onelist=False,
           startingcell=None, resolution=None, pos=None, points=None,
           constant=None, density=False, avg=False, tsc=False, ngp=False, volume=None, box=None, gridOrigin=None,
           gridSpacing=None, periodic=False, outvalue=None, invalue=None, expression=None, compute=None, size=None,
           dimvox=None, trackplanedist=None, innerdist=None, outpoints=None, outvol=None, pad=None, nodensity=False, delete=False, numcells=None, nsigma=None, override=False,
           infiles=None, numbin=None, interval=None, exclude=False, allcolumns=False,
           numrows=None, rangerows=None, width=None, precision=None,
           hugesplit=False, numoftables=None, maxsizetable=None, volumesplit=None,
           histogram=None, rangee=None, force=False, format=None, outlist=None,
           memsizelimit=None, history=False, historyfile=None):

    options = {
        # Global
        "op": (op, str),
        "history": (history, bool),
        "historyfile": (historyfile, str),
        "memsizelimit": (memsizelimit, float),

        # Basic
        "perc": (perc, float),
        "field": (field, str),
        "iseed": (iseed, int),
        "out": (out, str),
        "outcol": (outcol, str),
        "start": (start, int),
        "append": (append, bool),
        "filelist": (filelist, str),
        "newnames": (newnames, str),

        # Cut / Select Fields
        "limits": (limits, str),
        "operator": (operator, str),
        "threshold": (threshold, float),

        # Decimator
        "skip": (skip, int),
        "list": (listfile, str), # we cant take list, because list is a keyword

        # Extraction
        "geometry": (geometry, str),
        "background": (background, float),

        # Include
        "center": (center, str),
        "radius": (radius, float),

        # Extract List
        "multilist": (multilist, str),
        "binaryint": (binaryint, bool),
        "asciilist": (asciilist, bool),
        "numberlists": (numberlists, int),
        "listelements": (listelements, int),
        "onelist": (onelist, bool),

        # Subvolume
        "startingcell": (startingcell, str),
        "resolution": (resolution, str),

        # Multi Resolution / Point Distribute / Point Property
        "pos": (pos, str),
        "points": (points, str),
        "constant": (constant, float),
        "density": (density, bool),
        "avg": (avg, bool),

        # Distribution algorithms
        "tsc": (tsc, bool),
        "ngp": (ngp, bool),
        "volume": (volume, str),

        # Grid options
        "box": (box, float),
        "gridOrigin": (gridOrigin, str),
        "gridSpacing": (gridSpacing, str),
        "periodic": (periodic, bool),
        "invalue": (invalue, float),
        "outvalue": (outvalue, float),
        
        # Math Operation
        "expression": (expression, str),
        "compute": (compute, str),

        # Visual
        "size": (size, str),
        "pad": (pad, float),

        # POCA
        "dimvox": (dimvox, int),
        "trackplanedist": (trackplanedist, float),
        "innerdist": (innerdist, float),
        "outpoints": (outpoints, str),
        "outvol": (outvol, str),

        # Interpolate
        "infiles": (infiles, str),
        "numbin": (numbin, int),
        "interval": (interval, str),
        "nodensity": (nodensity, bool),

        # Sigma Contours
        "exclude": (exclude, bool),
        "allcolumns": (allcolumns, bool),
        
        # Show Table
        "numrows": (numrows, int),
        "rangerows": (rangerows, str),
        "width": (width, int),
        "precision": (precision, int),
        "delete": (delete, bool),
        "numcells": (numcells, int),
        "nsigma": (nsigma, float),
        "override": (override, bool),

        # Split
        "hugesplit": (hugesplit, bool),
        "numoftables": (numoftables, int),
        "maxsizetable": (maxsizetable, int),
        "volumesplit": (volumesplit, int),

        # Statistic
        "histogram": (histogram, int),
        "range": (rangee, str), # range is a keyword so we use rangee

        # VOTable
        "force": (force, bool),

        # Extract List output
        "format": (format, str),
        "outlist": (outlist, str)
    }

    logging.info(f"Executing VisIVOFilter with file: {input_file}")

    command = "VisIVOFilter"
    corefunction(command, input_file, *flags, mpi=mpi, options=options)


def viewer(input_file, *flags, mpi=False,
           out=None, nodefault=False, cycle=None, cycleoffset=None, cycle_skip_from=None, cycle_skip_to=None,
           camazim=None, camelev=None, zoom=None, camfov=None, campos=None, camfp=None, camroll=None,
           imagesize=None, backcolor=None, onecolor=None, color=False, colortable=None, colorrangefrom=None,
           colorrangeto=None, stereo=None, anaglyphsat=None, anaglyphmask=None,
           showlut=False, showbox=False, showaxes=False,
           cliplarge=False, cliprange=None, history=False, historyfile=None,
           x=None, y=None, z=None, scale=False, colorscalar=None, logscale=False, glyphs=None,
           radius=None, height=None, opacity=None, opacityTF=None, scaleglyphs=False, scenario=None,
           radiusscalar=None, heightscalar=None, 
           volume=False, vrendering=False, vrenderingfield=None, shadow=False, autorange=False,
           autorangemin=None, autorangemax=None, isosurface=False, isosurfacefield=None,
           isosurfacevalue=None, wireframe=False, isosmooth=None, 
           slice=False, slicefield=None, sliceplane=None, sliceposition=None, sliceplanepoint=None,
           sliceplanenormal=None, vector=False, vx=None, vy=None, vz=None, vectorline=False,
           vectorscalefactor=None, vectorscale=None):
    
    options = {
        # General
        "out": (out, str),
        "nodefault": (nodefault, bool),
        "cycle": (cycle, str),
        "cycleoffset": (cycleoffset, int),
        "cycle_skip_from": (cycle_skip_from, int),
        "cycle_skip_to": (cycle_skip_to, int),
        
        # Camera
        "camazim": (camazim, float),
        "camelev": (camelev, float),
        "zoom": (zoom, float),
        "camfov": (camfov, float),
        "campos": (campos, str),
        "camfp": (camfp, str),
        "camroll": (camroll, float),

        # Image & Color
        "imagesize": (imagesize, str),
        "backcolor": (backcolor, str),
        "onecolor": (onecolor, str),
        "color": (color, bool),
        "colortable": (colortable, str),
        "colorrangefrom": (colorrangefrom, float),
        "colorrangeto": (colorrangeto, float),

        # Stereo
        "stereo": (stereo, str),
        "anaglyphsat": (anaglyphsat, float),
        "anaglyphmask": (anaglyphmask, str),

        # Display
        "showlut": (showlut, bool),
        "showbox": (showbox, bool),
        "showaxes": (showaxes, bool),
        "cliplarge": (cliplarge, bool),
        "cliprange": (cliprange, str),
        "history": (history, bool),
        "historyfile": (historyfile, str),

        # Data Points
        "x": (x, str),
        "y": (y, str),
        "z": (z, str),
        "scale": (scale, bool),
        "colorscalar": (colorscalar, str),
        "logscale": (logscale, bool),
        "glyphs": (glyphs, str),
        "radius": (radius, float),
        "height": (height, float),
        "opacity": (opacity, float),
        "opacityTF": (opacityTF, str),
        "scaleglyphs": (scaleglyphs, bool),
        "scenario": (scenario, str),
        "radiusscalar": (radiusscalar, str),
        "heightscalar": (heightscalar, str),

        # Volumes
        "volume": (volume, bool),
        "vrendering": (vrendering, bool),
        "vrenderingfield": (vrenderingfield, str),
        "shadow": (shadow, bool),
        "autorange": (autorange, bool),
        "autorangemin": (autorangemin, float),
        "autorangemax": (autorangemax, float),

        # Isosurfaces
        "isosurface": (isosurface, bool),
        "isosurfacefield": (isosurfacefield, str),
        "isosurfacevalue": (isosurfacevalue, float),
        "wireframe": (wireframe, bool),
        "isosmooth": (isosmooth, str),

        # Slice
        "slice": (slice, bool),
        "slicefield": (slicefield, str),
        "sliceplane": (sliceplane, str),
        "sliceposition": (sliceposition, int),
        "sliceplanepoint": (sliceplanepoint, str),
        "sliceplanenormal": (sliceplanenormal, str),

        # Vector
        "vector": (vector, bool),
        "vx": (vx, str),
        "vy": (vy, str),
        "vz": (vz, str),
        "vectorline": (vectorline, bool),
        "vectorscalefactor": (vectorscalefactor, float),
        "vectorscale": (vectorscale, int),
    }

    logging.info(f"Executing VisIVOViewer with file: {input_file}")

    command = "VisIVOViewer"
    corefunction(command, input_file, *flags, mpi=False, options=options)


# sample commands for importer, filter and viewer
"""
if __name__ == "__main__":
    importer("clusterfields4.ascii", fformat="ascii", npoints=1000, double=True,missingvalue=0.0)
    filter("VisIVOServerBinary.bin", op="randomizer", perc=2.1, iseed=42, field="Y")
    filter("VisIVOServerBinary.bin", op="changecolname", field="X Y Z", newnames="A B C")
    viewer("VisIVOServerBinary.bin", x="X", y="Y", z="Z", color=True, colorscalar="scalar0", colortable="temperature", logscale=True)
"""

