#from mpl_toolkits.mplot3d import Axes3D
#import mpl_toolkits.mplot3d.art3d as art3d
#from mpl_toolkits.mplot3d.art3d import Poly3DCollection
#from matplotlib.pyplot import *
#from matplotlib.patches import Polygon,Circle

'''
12/21/2014

Speed up: make beam/cap there own classes and store x,y,z point matrices




'''

import numpy as np
import subprocess
from mayavi import mlab
from mayavi.sources.builtin_surface import BuiltinSurface
import time


# Remove vtk warnings
# https://github.com/enthought/mayavi/issues/3
try:
    __IPYTHON__
    ipython = True
except NameError:
    ipython = False
    ### THIS CAUSES ERRORS IN IPYTHON
    import vtk
    output=vtk.vtkFileOutputWindow()
    output.SetFileName("log.txt")
    vtk.vtkOutputWindow().SetInstance(output)



from configuration import *





sin = lambda x: np.sin(unitfunc(x))
cos = lambda x: np.cos(unitfunc(x))



def gaussian(x,a,b,c):
    return a*np.exp(-0.5*((x-b)/c)**2)




class Pulsar:
    def __init__(self,xp,yp,zp,period,timestep=0.0,rotaxis=(0,0,0),beamZ=BEAMZ,xrot=0.0,yrot=0.0,zrot=0.0,pulsephase = 0.2):
        # Pulsar characteristics
        self.xp = xp
        self.yp = yp
        self.zp = zp
        self.period = period
        self.xrotaxis,self.yrotaxis,self.zrotaxis = rotaxis #could go to a two coordinate system?

        self.phase = 0
        # Initial conditions
        self.xrot = xrot
        self.yrot = yrot
        self.zrot = zrot
        self.pulsephase = pulsephase #more to do here, the initial pulse phase

        # Generation
        #self.beam1,self.cap1 = self.plot_beam(beamZ,xrot,yrot,zrot)
        #self.beam2,self.cap2 = self.plot_beam(-1*beamZ,xrot,yrot,zrot)
        #self.beam1 = self.plot_beam(beamZ,xrot,yrot,zrot)
        #self.beam2 = self.plot_beam(-1*beamZ,xrot,yrot,zrot)
        self.beams = self.plot_beam2(beamZ,xrot,yrot,zrot)
        self.sphere = self.plot_sphere()
        if EARTH_ON and PULSE_ON:
            self.pulsetrain = self.plot_pulsetrain()

        # Animation 
        self.timestep = timestep
        self.Rmatrix = self.build_Rmatrix()

    def plot_beam2(self,Z=1,xrot=None,yrot=None,zrot=None): #modified from
        n = BEAMN
        t = np.linspace(-np.pi, np.pi, n)
        z = np.exp(1j * t)
        x = z.real.copy()*BEAMR
        y = z.imag.copy()*BEAMR
        z = np.zeros_like(x)

        triangles = [(0, i, i + 1) for i in range(1, n)]
        triangles.extend([((n+1), (n+1)+i, (n+1)+i +1) for i in range(1, n)])
        triangles.extend([(2*(n+1), 2*(n+1)+i, 2*(n+1)+i+1) for i in range(1, n)])
        triangles.extend([(3*(n+1), 3*(n+1)+i, 3*(n+1)+i + 1) for i in range(1, n)])

        x = np.r_[0, x]
        y = np.r_[0, y]
        z = np.r_[Z, z] - Z
        zneg = -1*z#np.r_[-1*Z, z] + Z
        xcap = np.copy(x)
        ycap = np.copy(y)
        zcap = np.zeros_like(x)-Z
        zcapneg = np.zeros_like(x)+Z
        #t = np.r_[0, t]
   

        x = np.r_[x,xcap]
        y = np.r_[y,ycap]
        zneg = np.r_[-1*z,-1*zcap]
        z = np.r_[z,zcap]
        x = np.r_[x,x]
        y = np.r_[y,y]
        z = np.r_[z,zneg]




        if xrot != 0.0 or yrot != 0.0 or zrot != 0.0:
            pts = np.matrix(np.vstack((x,y,z)))
            R = np.identity(3)
            if xrot != 0.0:
                c = cos(xrot)
                s = sin(xrot)
                R = np.matrix([[1,0,0],[0,c,-s],[0,s,c]])*R
            if yrot != 0.0:
                c = cos(yrot)
                s = sin(yrot)
                R = np.matrix([[c,0,s],[0,1,0],[-s,0,c]])*R
            if zrot != 0.0:
                c = cos(zrot)
                s = sin(zrot)
                R = np.matrix([[c,-s,0],[s,c,0],[0,0,1]])*R
            



            for i in range(len(x)):
                x[i],y[i],z[i] = R*pts[:,i]

            #ptscap = np.matrix(np.vstack((xcap,ycap,zcap)))
            #for i in range(len(x)):
            #    xcap[i],ycap[i],zcap[i] = R*ptscap[:,i]




            
        return mlab.triangular_mesh(x+self.xp, y+self.yp, z+self.zp, triangles,color=COLOR_BEAM)
        beam = mlab.triangular_mesh(x+self.xp, y+self.yp, z+self.zp, triangles,color=COLOR_BEAM)
        #Plot cap
        cap = mlab.triangular_mesh(xcap+self.xp,ycap+self.yp,zcap+self.zp,triangles,color=COLOR_BEAM)
        return beam,cap


    def plot_beam(self,Z=1,xrot=None,yrot=None,zrot=None): #modified from
        n = BEAMN
        t = np.linspace(-np.pi, np.pi, n)
        z = np.exp(1j * t)
        x = z.real.copy()*BEAMR
        y = z.imag.copy()*BEAMR
        z = np.zeros_like(x)

        triangles = [(0, i, i + 1) for i in range(1, n)]
        x = np.r_[0, x]
        y = np.r_[0, y]
        z = np.r_[Z, z] - Z
        xcap = np.copy(x)
        ycap = np.copy(y)
        zcap = np.zeros_like(x)-Z
        t = np.r_[0, t]

        if xrot != 0.0 or yrot != 0.0 or zrot != 0.0:
            pts = np.matrix(np.vstack((x,y,z)))
            R = np.identity(3)
            if xrot != 0.0:
                c = cos(xrot)
                s = sin(xrot)
                R = np.matrix([[1,0,0],[0,c,-s],[0,s,c]])*R
            if yrot != 0.0:
                c = cos(yrot)
                s = sin(yrot)
                R = np.matrix([[c,0,s],[0,1,0],[-s,0,c]])*R
            if zrot != 0.0:
                c = cos(zrot)
                s = sin(zrot)
                R = np.matrix([[c,-s,0],[s,c,0],[0,0,1]])*R
            



            for i in range(len(x)):
                x[i],y[i],z[i] = R*pts[:,i]
            #x,y,z = R*pts
            #x = np.array(x).flatten()
            #y = np.array(y).flatten()
            #z = np.array(z).flatten()
            #print R*pts
            #print np.shape(np.array(x).flatten()),y,z
            #raise SystemExit
            ptscap = np.matrix(np.vstack((xcap,ycap,zcap)))
            for i in range(len(x)):
                xcap[i],ycap[i],zcap[i] = R*ptscap[:,i]
            #xcap,ycap,zcap = R*ptscap
            #xcap = np.array(xcap).flatten()
            #ycap = np.array(ycap).flatten()
            #zcap = np.array(zcap).flatten()
        

        beam = mlab.triangular_mesh(x+self.xp, y+self.yp, z+self.zp, triangles,color=COLOR_BEAM)
        cap = mlab.triangular_mesh(xcap+self.xp, ycap+self.yp, zcap+self.zp, triangles,color=COLOR_BEAM)
        return beam,cap


    def plot_sphere(self):
        # Create a sphere for the pulsar
        phi, theta = np.mgrid[0:np.pi:SPHERE_RESOLUTION, 0:2 * np.pi:SPHERE_RESOLUTION]
       
        x = RADIUS_PULSAR * np.sin(phi) * np.cos(theta)
        y = RADIUS_PULSAR * np.sin(phi) * np.sin(theta)
        z = RADIUS_PULSAR * np.cos(phi)
        sphere = mlab.mesh(x+self.xp , y+self.yp, z+self.zp,color=COLOR_PULSAR)
        return sphere

    def plot_pulsetrain(self):
        self.pulsex = np.linspace(self.xp,0,PULSE_RESOLUTION) #these do not change
        self.pulsey = np.linspace(self.yp,0,PULSE_RESOLUTION)
        self.pulsez = np.linspace(self.zp,0,PULSE_RESOLUTION)  
        self.pulser = np.sqrt(self.pulsex**2 + self.pulsey**2 + self.pulsez**2)
        self.Npulses = int(np.ceil(np.max(self.pulser)/(2*np.pi)))+1 #+1 for loop, move this there?
        zpulse = np.zeros_like(self.pulsez)

        for n in range(self.Npulses):
            zpulse += gaussian(self.pulser,3.0,n*2*np.pi,0.3) #change pulse width        

        pulsetrain = mlab.plot3d(self.pulsex,self.pulsey,self.pulsez+zpulse,color=COLOR_PULSE,tube_radius=0.15)#),line_width=1036.0)
        return pulsetrain


    def get_components(self):
        return self.sphere,self.beams
        #return self.sphere,self.beam1,self.cap1,self.beam2,self.cap2

    def build_Rmatrix(self):
        self.rotation = self.timestep * (2*np.pi/self.period)


        R = np.matrix([[np.cos(self.rotation),-np.sin(self.rotation),0],[np.sin(self.rotation),np.cos(self.rotation),0],[0,0,1]]) #SHOULD THIS JUST BE COS AND SIN?
            
        RXneg = np.matrix([[1,0,0],[0,cos(-self.xrotaxis),-sin(-self.xrotaxis)],[0,sin(-self.xrotaxis),cos(-self.xrotaxis)]])
        RXpos = np.matrix([[1,0,0],[0,cos(self.xrotaxis),-sin(self.xrotaxis)],[0,sin(self.xrotaxis),cos(self.xrotaxis)]])
            
        RYneg = np.matrix([[cos(-self.yrotaxis),0,sin(-self.yrotaxis)],[0,1,0],[-sin(-self.yrotaxis),0,cos(-self.yrotaxis)]])
        RYpos = np.matrix([[cos(self.yrotaxis),0,sin(self.yrotaxis)],[0,1,0],[-sin(self.yrotaxis),0,cos(self.yrotaxis)]])

        RZneg = np.matrix([[cos(-self.zrotaxis),-sin(-self.zrotaxis),0],[sin(-self.zrotaxis),cos(-self.zrotaxis),0],[0,0,1]])
        RZpos = np.matrix([[cos(self.zrotaxis),-sin(self.zrotaxis),0],[sin(self.zrotaxis),cos(self.zrotaxis),0],[0,0,1]])


        R = RZpos*RYpos*RXpos*R*RXneg*RYneg*RZneg
        return R

    def rotate(self):
        items = self.get_components()[1:]
        
        #print self.phase
        for item in items:
            x,y,z = item.mlab_source.x-self.xp,item.mlab_source.y-self.yp,item.mlab_source.z-self.zp
            #a = time.time()
            pts = np.matrix(np.vstack((x,y,z)))
            #b = time.time()
            x,y,z = self.Rmatrix*pts
            x = np.array(x).flatten()
            y = np.array(y).flatten()
            z = np.array(z).flatten()
            #for i in range(len(x)):
            #    x[i],y[i],z[i] = self.Rmatrix*pts[:,i]
            #c = time.time()
            item.mlab_source.set(x=x+self.xp,y=y+self.yp,z=z+self.zp)
            #d = time.time()
            #print b-a,d-c
    def propagate(self):
        zpulse = np.zeros_like(self.pulsez)

        self.phase += np.abs(self.rotation/(2*np.pi))
        if self.phase >= 1.0:
            self.phase = self.phase % 1


        for n in range(self.Npulses):
            zpulse += gaussian(self.pulser,3.0,(n-self.phase)*2*np.pi,0.3) #change pulse width
        
        self.pulsetrain.mlab_source.set(z=self.pulsez+zpulse)
            
    def animate(self):
        self.rotate()
        if EARTH_ON and PULSE_ON:
            self.propagate()
    


#mlab.options.offscreen = True
#mayavi.engine.current_scene.scene.off_screen_rendering = True
mlab.figure(1, bgcolor=BGCOLOR, fgcolor=FGCOLOR, size=SIZE)

#Make Earth
'''
phi, theta = np.mgrid[0:np.pi:SPHERE_RESOLUTION, 0:2 * np.pi:SPHERE_RESOLUTION]
x = RADIUS_EARTH * np.sin(phi) * np.cos(theta)
y = RADIUS_EARTH * np.sin(phi) * np.sin(theta)
z = RADIUS_EARTH * np.cos(phi)
earth = mlab.mesh(x, y, z,color=COLOR_EARTH)
'''
if EARTH_ON:
    continents_src = BuiltinSurface(source='earth',name='Continents')
    continents_src.data_source.on_ratio = 2
    continents_src.data_source.radius = 2.5
    continents = mlab.pipeline.surface(continents_src,color=(0,0,0))
    sphere = mlab.points3d(0,0,0,scale_mode='none',scale_factor=5,color=COLOR_EARTH,resolution=50)#,opacity=05,name='Earth')

#Star field
if STARS_ON:
    np.random.seed(RANDOM_SEED) #is this needed elsewhere?
    x = np.random.uniform(-SKYBOX,SKYBOX,N_STARS)
    y = np.random.uniform(-SKYBOX,SKYBOX,N_STARS)
    z = np.random.uniform(-SKYBOX,SKYBOX,N_STARS)
    mlab.points3d(x,y,z,color=COLOR_STAR,scale_factor=0.5) 



ps = []
for PULSAR in PULSARS:
    ps.append(eval("Pulsar(%s)"%PULSAR))

mlab.view(CAMERA_AZIMUTH,CAMERA_ELEVATION)
f = mlab.gcf()
f.scene.camera.zoom(CAMERA_ZOOM)
f.scene.anti_aliasing_frames = ANTIALIASING



#mlab.show()
#raise SystemExit


@mlab.animate(delay=50,ui=False)
def anim():
    i=0
    while i < N_FRAMES:
        a = time.time()
        f.scene.camera.azimuth(CAMERA_ROTATE_AZIMUTH)
        f.scene.camera.elevation(CAMERA_ROTATE_ELEVATION)
        f.scene.disable_render= True
        for p in ps:
            p.animate()
        f.scene.disable_render = False
        f.scene.render()
        f.scene.save(OUTPUT_FILENAME_FORMAT%i)#,size=SIZE) #SIZE needed?
        i+=1
        b = time.time()
        print "(%i/%i)"%(i,N_FRAMES)
        print b-a
        yield
    print "Done"
    if not ipython:
        subprocess.call("rm log.txt",shell=True)
a = anim()

mlab.show()

#try:
#    subprocess.call("convert -delay 5 *png -loop 0 animated.gif",shel=True)


#convert -delay 5 *png -loop 0 animated.gif
