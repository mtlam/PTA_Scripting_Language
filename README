#README

Each line of the script is read in order. All options are listed with their default values unless otherwise specified.

##Pulsar Options

To create a pulsar:
```
PULSAR X Y Z P
```
where X,Y,Z are the coordinates of the center and P is the period. Other options that can be provided include:
```
timestep=0.0
rotaxis=(0,0,0)
beamZ=BEAMZ
xrot=0.0
yrot=0.0
zrot=0.0
pulsephase = 0.2
```
These arguments are separated by commas, so an example would be:
```
PULSAR 0 -30 0 0.1 timestep=0.01 rotaxis=(-20,-40,-40) xrot=-40 yrot=-80 zrot=40
```
##Color Options

These options require three numbers (R,G,B) on a scale from 0.0 to 1.0. 

```
COLOR_PULSAR 0.0 0.0 1.0
COLOR_BEAM 1.0 1.0 0.0
COLOR_PULSE 0.0 1.0 0.0
COLOR_EARTH 0.0 0.0 1.0
COLOR_STAR 1.0 1.0 1.0
BGCOLOR 0.0 0.0 0.0
FGCOLOR 0.0 0.0 0.0
```

##Geometric Options

These options require one number.

```
BEAMZ 2
BEAMN 20
BEAMR 1
RADIUS_EARTH 1.5
RADIUS_PULSAR 0.3
```

##Image Options
```
N_FRAMES 1
SIZE 600 400
CAMERA ZOOM 3
CAMERA AZIMUTH 0
CAMERA ELEVATION 90
CAMERA ROTATE AZIMUTH 0
CAMERA ROTATE ELEVATION 0
```
##User Variables

This section is not quite complete and only works within the PULSAR DEFINITION. Example:

XROT 40
PULSAR 0 0 0 0.1 xrot=XROT


##Other Options
```
UNITS RADIANS
RANDOM_SEED 1
N_STARS 100
SKYBOX 100
SPHERE RESOLUTION 101j
PULSE RESOLUTION 500
```


##To do:

-The output filename format is currently frame%04d.png and is should be modifiable.
-Should be able to choose what configuration file to read in.
-Modify the Earth (continents on/off)
-No stars as default?
-Turn off pulses, Earth