'''
Simple parser for PTASL

The use of globals causes a segmentation fault if running twice in iPython
'''
import re
#import numpy as np

# Defaults
CONFIG_FILE = "single_pulsar_config.dat"

PI = 3.14159265359
UNITS = "RADIANS"
unitfunc = lambda x: x
cameraunitfunc = lambda x: x*180/PI
COLOR_PULSAR = (0.0, 0.0, 1.0)
COLOR_BEAM = (1.0, 1.0, 0.0)
COLOR_PULSE = (0.0, 1.0, 0.0)
COLOR_EARTH = (0.0, 0.0, 1.0)
COLOR_STAR = (1.0, 1.0, 1.0)
BEAMZ = 2
BEAMN = 20
BEAMR = 1
RADIUS_EARTH = 1.5
RADIUS_PULSAR = 0.3

BGCOLOR = (0.0, 0.0, 0.0)
FGCOLOR = (0.0, 0.0, 0.0)
N_FRAMES = 1
RANDOM_SEED = 1
N_STARS = 100
SKYBOX = 100
SPHERE_RESOLUTION = 101j
PULSE_RESOLUTION = 500
SIZE = (600, 400)

CAMERA_ZOOM = 3
CAMERA_AZIMUTH = 0
CAMERA_ELEVATION = 90
CAMERA_ROTATE_AZIMUTH = 0
CAMERA_ROTATE_ELEVATION = 0

#To add to parser:
OUTPUT_FILENAME_FORMAT = "frame%04d.png" #how to add this in?
#Flag to see if you want to animate? = number of frames?



PULSARS = []


FILE = open(CONFIG_FILE,'r')
lines = map(lambda x: x.strip(),FILE.readlines())
FILE.close()


for line in lines:    
    if len(line) == 0 or line[0] == '#':
        continue

    m = re.match("PULSAR",line)
    if m != None:
        #Need to do things here
        PULSARS.append(",".join(line.split()[1:]))

        
    
    

    else:
        m = re.match(r"([a-zA-Z]+)\s([a-zA-Z]+)\s([a-zA-Z]+)",line)
        if m == None:
            m = re.match(r"([a-zA-Z]+)\s([a-zA-Z]+)",line)
            if m == None:
                m = re.match(r"([a-zA-Z]+)",line)
                if m.group(1).upper()[0:4] == "BEAM": #BEAMZ, BEAMN, BEAMR
                    L = m.group(1).upper()[4]
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require %s as one value"%L)
                    exec("BEAM%s = float(value.group(0))"%L)
                elif m.group(1).upper() == "FRAMES":
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require one integer value")
                    exec("N_FRAMES = int(value.group(0))")
                elif m.group(1).upper() == "SEED":
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require one integer value")
                    exec("RANDOM_SEED = int(value.group(0))")
                elif m.group(1).upper() == "STARS":
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require one integer value")
                    exec("N_STARS = int(value.group(0))")
                elif m.group(1).upper() == "SKYBOX":
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require one integer value")
                    exec("SKYBOX = int(value.group(0))")
                elif m.group(1).upper()[1:7] == "GCOLOR":
                    rgb = re.findall("[0-9.]*[0-9]+",line)
                    if len(rgb) != 3:
                        raise IndexError("Require RGB as three values")
                    rgb = tuple(map(float,rgb))
                    exec("%sGCOLOR = %s"%(m.group(1).upper()[0],str(rgb)))
                elif m.group(1).upper() == "SPHEREPTS":
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require one integer value")
                    SPHERE_RESOLUTION = int(value.group(0))*1j
                elif m.group(1).upper() == "PULSEPTS":
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require one integer value")
                    PULSE_RESOLUTION = int(value.group(0))
                elif m.group(1).upper() == "SIZE":
                    xy = re.findall("[0-9.]*[0-9]+",line)
                    if len(xy) != 2:
                        raise IndexError("Require XY as two values")
                    xy = tuple(map(float,xy))
                    SIZE = xy




                else: #Arbitrarily define variables
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        continue
                    exec("%s = float(value.group(0))"%m.group(1)) #use eval?


            else:
                if m.group(1).upper() == "COLOR":
                    rgb = re.findall("[0-9.]*[0-9]+",line)
                    if len(rgb) != 3:
                        raise IndexError("Require RGB as three values")
                    rgb = tuple(map(float,rgb))
                    if m.group(2).upper() == "PULSAR":
                        COLOR_PULSAR = rgb
                    elif m.group(2).upper() == "BEAM":
                        COLOR_BEAM = rgb
                    elif m.group(2).upper() == "PULSE":
                        COLOR_PULSE = rgb
                    elif m.group(2).upper() == "EARTH":
                        COLOR_EARTH = rgb
                    elif m.group(2).upper() == "STAR":
                        COLOR_STAR = rgb
                elif m.group(1).upper() == "RADIUS":
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require one numerical value")
                    if m.group(2).upper() == "EARTH":
                        RADIUS_EARTH = float(value)
                    elif m.group(2).upper() == "PULSAR":
                        RADIUS_PULSAR = float(value)

                elif m.group(1).upper() == "CAMERA":
                    value = re.search("[0-9.]*[0-9]+",line)
                    if value == None:
                        raise IndexError("Require one numerical value")
                    if m.group(2).upper() == "ZOOM":
                        CAMERA_ZOOM = float(value.group(0))
                    elif m.group(2).upper() == "AZIMUTH":
                        CAMERA_AZIMUTH = cameraunitfunc(float(value.group(0)))
                    elif m.group(2).upper() == "ELEVATION":
                        CAMERA_ELEVATION = cameraunitfunc(float(value.group(0)))
                    


                elif m.group(1).upper() == "UNITS":
                    if m.group(2).upper() == "DEGREES":
                        UNITS = "DEGREES"
                        unitfunc = lambda x: x*PI/180
                        cameraunitfunc = lambda x: x
                    elif m.group(2).upper() == "RADIANS":
                        UNITS = "RADIANS"
                        unitfunc = lambda x: x
                        cameraunitfunc = lambda x: x*180/PI
        else:
            if m.group(1).upper() == "CAMERA":
                value = re.search("[0-9.]*[0-9]+",line)
                if value == None:
                    raise IndexError("Require one numerical value")
            
                if m.group(2).upper() == "ROTATE" and m.group(3).upper() == "AZIMUTH":
                    CAMERA_ROTATE_AZIMUTH = cameraunitfunc(float(value.group(0)))
                elif m.group(2).upper() == "ROTATE" and m.group(3).upper() == "ELEVATION":
                    CAMERA_ROTATE_ELEVATION = cameraunitfunc(float(value.group(0)))
