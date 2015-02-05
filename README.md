#README

Each line of the script is read in order. All options are listed with their default values unless otherwise specified.

To run:

python pta_animation.py [CONFIGURATION_FILE]

If no configuration file is given, the default will be config.dat. See below for scripting options.

##Pulsar Options

To create a pulsar:
```
PULSAR X Y Z P
```
where X,Y,Z are the coordinates of the center and P is the period. Other options that can be provided include:
```
timestep=0.0 #timestep of rotation
rotaxis=(0,0,0)
beamZ=BEAMZ #defined below
xrot=0.0
yrot=0.0
zrot=0.0
pulsephase = 0.2 #initial pulse phase, not used currently
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
BEAMZ 2 #Height of beam
BEAMN 20 #Number of panels in the conical beam
BEAMR 1 #Radius of beam cap
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
```
XROT 40
PULSAR 0 0 0 0.1 xrot=XROT
```

##Other Options
```
UNITS RADIANS
RANDOM_SEED 1 #Random number generator's start seed
N_STARS 100 #Number of stars in skybox
SKYBOX 100 #Size of the skybox
SPHERE RESOLUTION 101 #Number of points to render for spheres
PULSE RESOLUTION 500 #Number of points to render for pulses
EARTH ON #Typing ON or OFF switches Earth and pulse rendering state
STARS ON #Typing ON or OFF switches star rendering state
FILENAME frame%04d.png #Change the default filename output. Must contain an integer formatting argument.
```


##To do:

- Modify the Earth (continents on/off)
- No stars as default?