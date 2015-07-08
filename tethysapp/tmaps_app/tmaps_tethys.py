#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This script is designed to produce time machine zoommable-interactive-
embeddable video products that users can embed in their websites or share
locally.The script was developed at Brigham Young Univeristy by Noah Taylor.
It was desgined to read and process the output of AD Hydro which is a finite
element hydrologic model that is being developed at the University of Wyoming
by Dr. Fred Ogden and CI-Water
'''


import netCDF4
try: paraview.simple
except: from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()
from PIL import Image, ImageChops
import PIL
import os
import sys
import numpy as np
from osgeo import ogr
from osgeo import osr
from owslib.wms import WebMapService
import shutil
import multiprocessing

class adhydro_render:
    
    def __init__(self, parameter, contour, opacityofmesh):
        """
        When the adhydro_render class object is called, it requires 3 parameters for input
        """
        self.input_dir = 'geometry.nc'
        self.parinput_dir = 'display.nc'
        self.parameter = parameter
        self.netcdfgeo = netCDF4.Dataset(self.input_dir)
        self.netcdfpar = netCDF4.Dataset(self.parinput_dir)


        self.ymin = self.netcdfgeo.variables['meshNodeY'][:].min()
        self.ymax = self.netcdfgeo.variables['meshNodeY'][:].max()
        self.ymid = (self.ymax + self.ymin)/2
        self.ydif = self.ymax - self.ymin
        
        self.xmin = self.netcdfgeo.variables['meshNodeX'][:].min()
        self.xmax = self.netcdfgeo.variables['meshNodeX'][:].max()
        self.xmid = (self.xmax + self.xmin)/2
        self.xdif = self.xmax - self.xmin
        
        self.zmin = self.netcdfgeo.variables['meshNodeZSurface'][:].min()
        self.zmax = self.netcdfgeo.variables['meshNodeZSurface'][:].max()
        self.zmid = (self.zmax + self.zmin)/2
        self.zdif = self.zmax - self.zmin
        self.zout = self.xdif + 2*self.ydif
        
        print self.ymin, self.ymax, self.xmin, self.xmax, self.zmin, self.zmax


        imagepath = './images'
        if not os.path.isdir(imagepath):
            os.makedirs(imagepath)
            
        self.contour = contour
        self.opacity = opacityofmesh
#        self.zeroopacity = turnon_zeroopacity
        
        if opacityofmesh > 1:
            sys.exit("Please choose an opacity value that is not greater than 1 nor less than 0")
        elif opacityofmesh < 0:
            sys.exit("Please choose an opacity value that is not greater than 1 nor less than 0")
        else:
            pass

        
    def renderpv(self):
        '''
        This method uses the paraview package to loop through the specified 
        parameter and output an image of each time step. The output 
        of this method can be found in the images folder in the relative 
        working directory.        
        '''

        contour = self.contour
        
        ##Here the code checks to see what parameter the user is wanting to render. It then sets the variable associated
        ##to the specified parameter    
        parameter = self.parameter       
        print parameter
        try:
            max_max = self.netcdfpar.variables[parameter][:].max()
            min_min = self.netcdfpar.variables[parameter][:].min()
            print max_max, min_min
            
        except Exception:
            sys.exit("Invalid parameter Inputted.")
        
        
        self.netcdfgeo.close()
        self.netcdfpar.close()        
        
        try:
            piecewise = CreatePiecewiseFunction( Points=[min_min, 1.0, 0.5, 0.0, max_max, 1.0, 0.5, 0.0] )
            #piecewise = CreatePiecewiseFunction( Points=[min_min, 1.0, 0.5, 0.0, (max_max+min_min)*0.001, 1.0, 0.5, 0.0, max_max, 0.6, 0.5, 0.0])
            #print (max_max+min_min)*0.001, min_min
            titletype = parameter
        except Exception:
            sys.exit("Invalid parameter inputted. Please input an existing variable.")        

        ## From the inputted contour arg, generate the pvlookup parameter that will be used as the contour reference
        if contour == 'cooltowarm':
            pvlookup = GetLookupTableForArray( parameter, 1, Discretize=1, RGBPoints=[min_min, 0.23, 0.299, 0.754, max_max, 0.706, 0.016, 0.15], UseLogScale=0, VectorComponent=0, NanColor=[0.25, 0.0, 0.0], NumberOfTableValues=256, EnableOpacityMapping=0, ColorSpace='Diverging', IndexedLookup=0, VectorMode='Magnitude', ScalarOpacityFunction=piecewise, HSVWrap=0, ScalarRangeInitialized=1.0, AllowDuplicateScalars=1, Annotations=[], LockScalarRange=0 )           
        elif contour == 'bluetocyan':
            pvlookup = GetLookupTableForArray(parameter, 1, Discretize=1, RGBPoints=[min_min, 0.0, 0.0, 0.0, ((max_max-min_min)/16*1+min_min), 0.0, 0.15294117647058825, 0.36470588235294116, ((max_max-min_min)/16*2+min_min), 0.0, 0.2549019607843137, 0.47058823529411764, ((max_max-min_min)/16*3+min_min), 0.0, 0.34901960784313724, 0.5725490196078431, ((max_max-min_min)/16*4+min_min), 0.0, 0.44313725490196076, 0.6705882352941176, ((max_max-min_min)/16*5+min_min), 0.0, 0.5372549019607843, 0.7725490196078432, ((max_max-min_min)/16*6+min_min), 0.0, 0.6274509803921569, 0.8705882352941177, ((max_max-min_min)/16*7+min_min), 0.0, 0.7176470588235294, 0.9647058823529412, ((max_max-min_min)/16*8+min_min), 0.0784313725490196, 0.7725490196078432, 1.0, ((max_max-min_min)/16*9+min_min), 0.20784313725490197, 0.8588235294117647, 1.0, ((max_max-min_min)/16*10+min_min), 0.3254901960784314, 0.9411764705882353, 1.0, ((max_max-min_min)/16*11+min_min), 0.45098039215686275, 1.0, 1.0, ((max_max-min_min)/16*12+min_min), 0.5607843137254902, 1.0, 1.0, ((max_max-min_min)/16*13+min_min), 0.6627450980392157, 1.0, 1.0, ((max_max-min_min)/16*14+min_min), 0.7607843137254902, 1.0, 1.0, ((max_max-min_min)/16*15+min_min), 0.8705882352941177, 1.0, 1.0, max_max, 1.0, 1.0, 1.0], UseLogScale=0, VectorComponent=0, NanColor=[0.4980392156862745, 0.0, 0.0], NumberOfTableValues=256, EnableOpacityMapping=0, ColorSpace='Lab', IndexedLookup=0, VectorMode='Magnitude', ScalarOpacityFunction=piecewise, HSVWrap=0, ScalarRangeInitialized=1.0, AllowDuplicateScalars=1, Annotations=[], LockScalarRange=0 )        
        elif contour == 'bluetored':
            pvlookup = GetLookupTableForArray( parameter, 1, Discretize=1, RGBPoints=[min_min, 0.0196078431372549, 0.18823529411764706, 0.3803921568627451, ((max_max-min_min)/16*1+min_min), 0.08850232700083925, 0.3211108567940795, 0.5649347676813916, ((max_max-min_min)/16*2+min_min), 0.1633936064698253, 0.444983596551461, 0.6975051499198901, ((max_max-min_min)/16*3+min_min), 0.24705882352941178, 0.5557030594338903, 0.7541008621347371, ((max_max-min_min)/16*4+min_min), 0.42069123369192035, 0.6764324406805524, 0.8186923018234531, ((max_max-min_min)/16*5+min_min), 0.6064545662623025, 0.7897764553292134, 0.8802777141985199, ((max_max-min_min)/16*6+min_min), 0.7614709697108415, 0.868513008316167, 0.9245593957427329, ((max_max-min_min)/16*7+min_min), 0.8780498970016022, 0.9257190814068819, 0.9519493400473029, ((max_max-min_min)/16*8+min_min), 0.969085221637293, 0.966475928892958, 0.9649347676813916, ((max_max-min_min)/16*9+min_min), 0.9838559548332951, 0.8975814450293736, 0.8468299382009613, ((max_max-min_min)/16*10+min_min), 0.9824673838406958, 0.8006866559853514, 0.706111238269627, ((max_max-min_min)/16*11+min_min), 0.9603265430685893, 0.6678263523308156, 0.5363393606469825, ((max_max-min_min)/16*12+min_min), 0.8945754177157245, 0.5038071259632257, 0.3997711146715496, ((max_max-min_min)/16*13+min_min), 0.8170748455024033, 0.3321736476691844, 0.2810406652933547, ((max_max-min_min)/16*14+min_min), 0.7284962233920805, 0.15501640344853895, 0.1973907072556649, ((max_max-min_min)/16*15+min_min), 0.576928358892195, 0.055359731441214616, 0.1492484931715877, max_max, 0.403921568627451, 0.0, 0.12156862745098039], UseLogScale=0, VectorComponent=0, NanColor=[0.4980392156862745, 0.0, 0.0], NumberOfTableValues=256, EnableOpacityMapping=0, ColorSpace='Lab', IndexedLookup=0, VectorMode='Magnitude', ScalarOpacityFunction=piecewise, HSVWrap=0, ScalarRangeInitialized=1.0, AllowDuplicateScalars=1, Annotations=[], LockScalarRange=0 )
        elif contour == 'blueyellowred':
            pvlookup = GetLookupTableForArray( parameter, 1, Discretize=1, RGBPoints=[min_min, 0.19121080338750285, 0.19121080338750285, 0.19121080338750285, ((max_max-min_min)/16*1+min_min), 0.23949034866865035, 0.005447470817120622, 0.6148165102616923, ((max_max-min_min)/16*2+min_min), 0.22059967956054016, 0.06175326161593042, 0.8635538261997406, ((max_max-min_min)/16*3+min_min), 0.17509727626459143, 0.2789806973373007, 0.9779354543373769, ((max_max-min_min)/16*4+min_min), 0.14352635996032653, 0.57607385366598, 0.9985503929198138, ((max_max-min_min)/16*5+min_min), 0.16646066987106126, 0.8718852521553369, 0.9659418631265736, ((max_max-min_min)/16*6+min_min), 0.3761959258411536, 0.9935606927595941, 0.9818265049210345, ((max_max-min_min)/16*7+min_min), 0.6820019836728466, 0.9913023575188831, 0.9992370489051652, ((max_max-min_min)/16*8+min_min), 0.9541771572442207, 0.9527275501640344, 0.9437399862668803, ((max_max-min_min)/16*9+min_min), 0.9997405966277562, 0.9930113679713131, 0.6628976882581826, ((max_max-min_min)/16*10+min_min), 0.9794003204394598, 0.9914702067597467, 0.35797665369649806, ((max_max-min_min)/16*11+min_min), 0.9687647821774624, 0.8549629968719005, 0.16266117341878386, ((max_max-min_min)/16*12+min_min), 0.9992523079270619, 0.5566948958571756, 0.14431982909895474, ((max_max-min_min)/16*13+min_min), 0.9739528496223392, 0.262226291294728, 0.17795071335927368, ((max_max-min_min)/16*14+min_min), 0.8523537041275654, 0.05267414358739605, 0.22298008697642482, ((max_max-min_min)/16*15+min_min), 0.5938963912413214, 0.00912489509422446, 0.2388494697489891, max_max, 0.19121080338750285, 0.19121080338750285, 0.19121080338750285], UseLogScale=0, VectorComponent=0, NanColor=[0.4980392156862745, 0.0, 0.0], NumberOfTableValues=256, EnableOpacityMapping=0, ColorSpace='Lab', IndexedLookup=0, VectorMode='Magnitude', ScalarOpacityFunction=piecewise, HSVWrap=0, ScalarRangeInitialized=1.0, AllowDuplicateScalars=1, Annotations=[], LockScalarRange=0 )
        elif contour == 'rainbowdesat':
            pvlookup = GetLookupTableForArray( parameter, 1, Discretize=1, RGBPoints=[min_min, 0.2784313725490196, 0.2784313725490196, 0.8588235294117647, ((max_max-min_min)/7*1+min_min), 0.0, 0.0, 0.3607843137254902, ((max_max-min_min)/7*2+min_min), 0.0, 1.0, 1.0, ((max_max-min_min)/7*3+min_min), 0.0, 0.5019607843137255, 0.0, ((max_max-min_min)/7*4+min_min), 1.0, 1.0, 0.0, ((max_max-min_min)/7*5+min_min), 1.0, 0.3803921568627451, 0.0, ((max_max-min_min)/7*6+min_min), 0.4196078431372549, 0.0, 0.0, max_max, 0.8784313725490196, 0.30196078431372547, 0.30196078431372547], UseLogScale=0, VectorComponent=0, NanColor=[1.0, 1.0, 0.0], NumberOfTableValues=256, EnableOpacityMapping=0, ColorSpace='RGB', IndexedLookup=0, VectorMode='Magnitude', ScalarOpacityFunction=piecewise, HSVWrap=0, ScalarRangeInitialized=1.0, AllowDuplicateScalars=1, Annotations=[], LockScalarRange=0 )
     
        else:
            sys.exit("Invalid contour inputted. Please input one of the following: 'cooltowarm', 'bluetocyan', 'bluetored', 'blueyellowred', 'rainbowdesat'") 
    
        ##This portion of the script will use the python paraview tools to 
        ##render and export the images from each time step of the data set
        ##There are piecewise functions to define what data set will be viewed
        ##out of the XDMF file and the max and min bounds for contour display
        ##Notice that the XDMFReader is being used to interpret the input files
        ##since this was developed to originally handl ADHydro ouput.

        
        mesh_display_xmf = XDMFReader( guiName="mesh_display.xmf", FileName='./mesh_display.xmf')
        ##Here it is being determined how many time steps there are in order to extract all these as images later
        tsteps = mesh_display_xmf.TimestepValues

        tstepstotext = [('"Output Time: '+str(i)+'",') for i in tsteps]
        np.savetxt('tstepstotext.txt',tstepstotext,delimiter=',', fmt="%s")        
        
        print("There are a total number of " + str(len(tsteps)) + " images that will be extracted")
        
        tstepsnum = len(tsteps)
        print tstepsnum
        
        ##THe following sets up the rendering options used to define the 
        ##extents, background color, and similar parameters for output
        RenderView1 = CreateRenderView()
        RenderView1.LightSpecularColor = [1.0, 1.0, 1.0]
        RenderView1.UseOutlineForLODRendering = 0
        RenderView1.KeyLightAzimuth = 10.0
        RenderView1.UseTexturedBackground = 0
        RenderView1.UseLight = 1
        RenderView1.CameraPosition = [self.xmid, self.ymid, self.zout]
        RenderView1.FillLightKFRatio = 3.0
        RenderView1.Background2 = [0.0, 0.0, 0.16470588235294117]
        RenderView1.FillLightAzimuth = -10.0
        RenderView1.LODResolution = 0.5
        RenderView1.BackgroundTexture = []
        RenderView1.InteractionMode = '3D'
        RenderView1.StencilCapable = 1
        RenderView1.LightIntensity = 1.0
        RenderView1.CameraFocalPoint = [self.xmid, self.ymid, self.zmid]
        RenderView1.ImageReductionFactor = 2
        RenderView1.CameraViewAngle = 30.0
        RenderView1.CameraParallelScale = 36120.14658587354
        RenderView1.EyeAngle = 2.0
        RenderView1.HeadLightKHRatio = 3.0
        RenderView1.StereoRender = 0
        RenderView1.KeyLightIntensity = 0.75
        RenderView1.BackLightAzimuth = 110.0
        RenderView1.OrientationAxesInteractivity = 0
        RenderView1.UseInteractiveRenderingForSceenshots = 0
        RenderView1.UseOffscreenRendering = 1
        RenderView1.Background = [0.9568627450980393, 0.6705882352941176, 0.0]
        RenderView1.UseOffscreenRenderingForScreenshots = 1
        RenderView1.NonInteractiveRenderDelay = 0.0
        RenderView1.CenterOfRotation = [self.xmid, self.ymid, self.zmid]
        RenderView1.CameraParallelProjection = 0
        RenderView1.CompressorConfig = 'vtkSquirtCompressor 0 3'
        RenderView1.HeadLightWarmth = 0.5
        RenderView1.MaximumNumberOfPeels = 4
        RenderView1.LightDiffuseColor = [1.0, 1.0, 1.0]
        RenderView1.StereoType = 'Red-Blue'
        RenderView1.DepthPeeling = 1
        RenderView1.BackLightKBRatio = 3.5
        RenderView1.StereoCapableWindow = 1
        RenderView1.CameraViewUp = [0.0, 1.0, 0.0]
        RenderView1.LightType = 'HeadLight'
        RenderView1.LightAmbientColor = [1.0, 1.0, 1.0]
        RenderView1.RemoteRenderThreshold = 20.0
        RenderView1.CacheKey = 120.423912
        RenderView1.UseCache = 0
        RenderView1.KeyLightElevation = 50.0
        RenderView1.CenterAxesVisibility = 0
        RenderView1.MaintainLuminance = 0
        RenderView1.StillRenderImageReductionFactor = 1
        RenderView1.BackLightWarmth = 0.5
        RenderView1.FillLightElevation = -75.0
        RenderView1.MultiSamples = 0
        RenderView1.FillLightWarmth = 0.4
        RenderView1.AlphaBitPlanes = 1
        RenderView1.LightSwitch = 0
        RenderView1.OrientationAxesVisibility = 0
        RenderView1.BackLightElevation = 0.0
        RenderView1.ViewTime = 120.423912
        RenderView1.OrientationAxesOutlineColor = [1.0, 1.0, 1.0]
        RenderView1.LODThreshold = 5.0
        RenderView1.CollectGeometryThreshold = 100.0
        RenderView1.UseGradientBackground = 0
        RenderView1.KeyLightWarmth = 0.6
        RenderView1.OrientationAxesLabelColor = [1.0, 1.0, 1.0]
        
        DataRepresentation1 = Show()
        DataRepresentation1.CubeAxesZAxisVisibility = 1
        DataRepresentation1.SelectionPointLabelColor = [0.5, 0.5, 0.5]
        DataRepresentation1.SelectionPointFieldDataArrayName = 'vtkOriginalPointIds'
        DataRepresentation1.SuppressLOD = 0
        DataRepresentation1.CubeAxesXGridLines = 0
        DataRepresentation1.BlockVisibility = []
        DataRepresentation1.CubeAxesYAxisTickVisibility = 1
        DataRepresentation1.Position = [0.0, 0.0, 0.0]
        DataRepresentation1.BackfaceRepresentation = 'Follow Frontface'
        DataRepresentation1.SelectionOpacity = 1.0
        DataRepresentation1.SelectionPointLabelShadow = 0
        DataRepresentation1.CubeAxesYGridLines = 0
        DataRepresentation1.CubeAxesZAxisTickVisibility = 1
        DataRepresentation1.OrientationMode = 'Direction'
        DataRepresentation1.ScaleMode = 'No Data Scaling Off'
        DataRepresentation1.Diffuse = 1.0
        DataRepresentation1.SelectionUseOutline = 1
        DataRepresentation1.SelectionPointLabelFormat = ''
        DataRepresentation1.CubeAxesZTitle = 'Z-Axis'
        DataRepresentation1.Specular = 0.1
        DataRepresentation1.SelectionVisibility = 1
        DataRepresentation1.InterpolateScalarsBeforeMapping = 1
        DataRepresentation1.CustomRangeActive = [0, 0, 0]
        DataRepresentation1.Origin = [0.0, 0.0, 0.0]
        DataRepresentation1.CubeAxesVisibility = 0
        DataRepresentation1.Scale = [1.0, 1.0, 1.0]
        DataRepresentation1.SelectionCellLabelJustification = 'Left'
        DataRepresentation1.DiffuseColor = [1.0, 1.0, 1.0]
        DataRepresentation1.SelectionCellLabelOpacity = 1.0
        DataRepresentation1.CubeAxesInertia = 1
        DataRepresentation1.Source = []
        DataRepresentation1.Masking = 0
        DataRepresentation1.Opacity = 1.0
        DataRepresentation1.LineWidth = 1.0
        DataRepresentation1.MeshVisibility = 0
        DataRepresentation1.Visibility = 1
        DataRepresentation1.SelectionCellLabelFontSize = 18
        DataRepresentation1.CubeAxesCornerOffset = 0.0
        DataRepresentation1.SelectionPointLabelJustification = 'Left'
        DataRepresentation1.OriginalBoundsRangeActive = [0, 0, 0]
        DataRepresentation1.SelectionPointLabelVisibility = 0
        DataRepresentation1.SelectOrientationVectors = ''
        DataRepresentation1.CubeAxesTickLocation = 'Inside'
        DataRepresentation1.BackfaceDiffuseColor = [1.0, 1.0, 1.0]
        DataRepresentation1.CubeAxesYLabelFormat = '%-#6.3g'
        DataRepresentation1.CubeAxesYAxisVisibility = 1
        DataRepresentation1.SelectionPointLabelFontFamily = 'Arial'
        DataRepresentation1.CubeAxesUseDefaultYTitle = 1
        DataRepresentation1.SelectScaleArray = ''
        DataRepresentation1.CubeAxesYTitle = 'Y-Axis'
        DataRepresentation1.ColorAttributeType = 'CELL_DATA'
        DataRepresentation1.AxesOrigin = [0.0, 0.0, 0.0]
        DataRepresentation1.UserTransform = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        DataRepresentation1.SpecularPower = 100.0
        DataRepresentation1.Texture = []
        DataRepresentation1.SelectionCellLabelShadow = 0
        DataRepresentation1.AmbientColor = [1.0, 1.0, 1.0]
        DataRepresentation1.BlockOpacity = {}
        DataRepresentation1.MapScalars = 1
        DataRepresentation1.PointSize = 2.0
        DataRepresentation1.CubeAxesUseDefaultXTitle = 1
        DataRepresentation1.SelectionCellLabelFormat = ''
        DataRepresentation1.Scaling = 0
        DataRepresentation1.StaticMode = 0
        DataRepresentation1.SelectionCellLabelColor = [0.0, 1.0, 0.0]
        DataRepresentation1.EdgeColor = [0.0, 0.0, 0.5000076295109483]
        DataRepresentation1.CubeAxesXAxisTickVisibility = 1
        DataRepresentation1.SelectionCellLabelVisibility = 0
        DataRepresentation1.NonlinearSubdivisionLevel = 1
        DataRepresentation1.CubeAxesColor = [1.0, 1.0, 1.0]
        DataRepresentation1.Representation = 'Surface'
        DataRepresentation1.CustomRange = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
        DataRepresentation1.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
        DataRepresentation1.Orientation = [0.0, 0.0, 0.0]
        DataRepresentation1.CubeAxesXTitle = 'X-Axis'
        DataRepresentation1.ScalarOpacityUnitDistance = 2170.6532965413962
        DataRepresentation1.BackfaceOpacity = 1.0
        DataRepresentation1.SelectionPointLabelFontSize = 18
        DataRepresentation1.SelectionCellFieldDataArrayName = parameter
        DataRepresentation1.SelectionColor = [1.0, 0.0, 1.0]
        DataRepresentation1.BlockColor = {}
        DataRepresentation1.Ambient = 0.0
        DataRepresentation1.CubeAxesXAxisMinorTickVisibility = 1
        DataRepresentation1.ScaleFactor = 5243.983899999969
        DataRepresentation1.BackfaceAmbientColor = [1.0, 1.0, 1.0]
        DataRepresentation1.ScalarOpacityFunction = piecewise
        DataRepresentation1.SelectMaskArray = ''
        DataRepresentation1.SelectionLineWidth = 2.0
        DataRepresentation1.CubeAxesZAxisMinorTickVisibility = 1
        DataRepresentation1.CubeAxesXAxisVisibility = 1
        DataRepresentation1.CubeAxesXLabelFormat = '%-#6.3g'
        DataRepresentation1.Interpolation = 'Gouraud'
        DataRepresentation1.CubeAxesZLabelFormat = '%-#6.3g'
        DataRepresentation1.SelectMapper = 'Projected tetra'
        DataRepresentation1.SelectionCellLabelFontFamily = 'Arial'
        DataRepresentation1.SelectionCellLabelItalic = 0
        DataRepresentation1.CubeAxesYAxisMinorTickVisibility = 1
        DataRepresentation1.CubeAxesZGridLines = 0
        DataRepresentation1.ExtractedBlockIndex = 0
        DataRepresentation1.SelectionPointLabelOpacity = 1.0
        DataRepresentation1.UseAxesOrigin = 0
        DataRepresentation1.CubeAxesFlyMode = 'Closest Triad'
        DataRepresentation1.Pickable = 1
        DataRepresentation1.CustomBoundsActive = [0, 0, 0]
        DataRepresentation1.CubeAxesGridLineLocation = 'All Faces'
        DataRepresentation1.SelectionRepresentation = 'Wireframe'
        DataRepresentation1.SelectionPointLabelBold = 0
        DataRepresentation1.ColorArrayName = ('CELL_DATA', parameter)
        DataRepresentation1.SelectionPointLabelItalic = 0
        DataRepresentation1.AllowSpecularHighlightingWithScalarColoring = 0
        DataRepresentation1.SpecularColor = [1.0, 1.0, 1.0]
        DataRepresentation1.CubeAxesUseDefaultZTitle = 1
        DataRepresentation1.LookupTable = pvlookup
        DataRepresentation1.SelectionPointSize = 5.0
        DataRepresentation1.SelectionCellLabelBold = 0
        DataRepresentation1.Orient = 0
        Render()
        
        
        imgdir = "./images"
        
        try :
            shutil.rmtree(imgdir)
        except :
            pass        
        
        if not os.path.exists(imgdir):
            os.makedirs(imgdir)
        
        ##This loop will go through all the timesteps and save out the images to the specified directory
        for tstepsnum in xrange(0, 20):
        	RenderView1.ViewTime = tsteps[tstepsnum]
        	Render()

        	WriteImage("images/" + str(tstepsnum) +".png", Magnification=10)
        	print("Image " + str(tstepsnum + 1) + "/" + str(len(tsteps)) + " was exctracted: " + str(tstepsnum/len(tsteps)*100) + "% of images rendered.")
        else:
         DataRepresentation1.Opacity = 0
         ScalarBarWidgetRepresentation1 = CreateScalarBar( TextPosition=1, Title=titletype, Position2=[0.1299999999999999, 0.5], TitleOpacity=1.0, TitleFontSize=12, NanAnnotation='NaN', TitleShadow=1, AutomaticLabelFormat=1, DrawAnnotations=1, TitleColor=[1.0, 1.0, 1.0], AspectRatio=15.0, NumberOfLabels=10, ComponentTitle='', Resizable=1, DrawNanAnnotation=0, TitleFontFamily='Arial', Visibility=1, LabelFontSize=10, LabelFontFamily='Arial', TitleItalic=0, LabelBold=1, LabelItalic=0, Enabled=1, LabelColor=[1.0, 1.0, 1.0], Position=[0.8141469013006885, 0.37274368231046917], Selectable=0, UseNonCompositedRenderer=1, LabelOpacity=0.9, TitleBold=0, LabelFormat='%-#6.3g', Orientation='Vertical', LabelShadow=0, LookupTable=pvlookup, Repositionable=1 )
         GetRenderView().Representations.append(ScalarBarWidgetRepresentation1)
         Render()
         WriteImage("images/legend.png", Magnification=10)
         print("All " + str(tstepsnum + 1) + " images were extracted")

    def trmmsk(self):        
        '''
        ##Here the images will be given a transparent background with the
        alpha channel defined and the images will also be trimmed so that
        ##the exact bounds of the image our known in order to properly overlay
        them onto the basemap later
        '''
        
        
        path = "./images/"
        opacity = int(self.opacity*255)
        for fname in os.listdir(path):
            #print(fname)
        
            def trim(im):
                bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
                diff = ImageChops.difference(im, bg)
                diff = ImageChops.add(diff, diff, 2.0, -100)
                bbox = diff.getbbox()
                if bbox:
                    return im.crop(bbox)

        ##This portion will go through each pixel of the image and if the pixel corresponds to the background color
        ##it will put an alpha channel of 0 or fully transparent. This is so that all we see is the mesh on the basemap
            def runtrim():                
                im = Image.open(path + fname)
                im = trim(im)
                im = im.convert("RGBA")
                pixdata = im.load()
                for y in xrange(im.size[1]):
                    for x in xrange(im.size[0]):
                        if pixdata[x, y] == (244, 171, 0, 255):
        				pixdata[x, y] = (244, 171, 0, 0)
                        elif fname == 'legend.png':
                                print 'passed legend.png'
    				pass
                        elif pixdata[x, y][3] == 255:
        				pixdata[x, y] = (pixdata[x,y][0],pixdata[x,y][1],pixdata[x,y][2],opacity)
                        else:
    				pass
            

        
                im.save(path+fname)
            runtrim()
        print("All images are masked and trimmed.")
        
        ##Resize the legend so that it is not too big when overlaying the viewer
        legenddir = "./images/legend.png"
        legendim = Image.open(legenddir)
        reslegend = (235,581)
        newlegend = legendim.resize(reslegend)
        newlegend.save("./legend.png")
        os.remove(legenddir)
        
    def getbasemap(self):
        '''
        Reproject coordinates of the corners of the cropped mesh so that they
        can be relatable to the base map - if a different project is used for
        the the geometry then it can be redefined below.
        Get the basemap. Here the owslib module will be taken advantage of in
        order to download a high quality basemap for the unstructured gird to
        have geographical context
        '''
        source = osr.SpatialReference()
        source.ImportFromProj4('+proj=sinu +datum=WGS84 +lon_0=-109 +x_0=20000000 +y_0=10000000')
        
        target = osr.SpatialReference()
        target.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        
        transform = osr.CoordinateTransformation(source, target)
        
        pointone = "POINT ("+str(self.xmin)+" "+str(self.ymax)+")"
        pointtwo = "POINT ("+str(self.xmax)+" "+str(self.ymin)+")"
        
        
        point = ogr.CreateGeometryFromWkt(pointone)
        point.Transform(transform)
        
        self.outpoint = point.GetPoint()

        
        self.point2 = ogr.CreateGeometryFromWkt(pointtwo)
        self.point2.Transform(transform)
        
        self.outpoint2 = self.point2.GetPoint()
        #print(outpoint2)
        print('Bounding coordinates have been reprojected')
        
        ##This is the WMS server that is being used
        wms = WebMapService('http://raster.nationalmap.gov/arcgis/services/Orthoimagery/USGS_EROS_Ortho_NAIP/ImageServer/WMSServer?request=GetCapabilities&service=WMS')
        
        outpoint = self.outpoint
        outpoint2 = self.outpoint2
        ##Calculate buffers to impose on the base map - tring 35% on y and 65% on each side
        
        resx = 5000
        resy = 3816
        
        bufx = 1.25
        bufy = 1
        
        mapxmin = outpoint[0] - (outpoint2[0]-outpoint[0])*bufx
        mapxmax = outpoint2[0] + (outpoint2[0]-outpoint[0])*bufx
        
        mapymin = outpoint2[1] - (outpoint[1]-outpoint2[1])*bufy
        mapymax = outpoint[1] + (outpoint[1]-outpoint2[1])*bufy
        
        self.mapxmin = mapxmin
        self.mapxmax = mapxmax
        self.mapymin = mapymin
        self.mapymax = mapymax
        
        overlayx = ((outpoint2[0]-outpoint[0])*bufx)/(mapxmax-mapxmin)*resx
        overlayy = ((outpoint[1]-outpoint2[1])*bufy)/(mapymax-mapymin)*resy
        self.overlayx = int(overlayx)
        self.overlayy = int(overlayy)
        
        fgnewsizex = ((outpoint2[0]-outpoint[0]))/(mapxmax-mapxmin)*resx
        fgnewsizex = int(fgnewsizex)
        fgnewsizey = ((outpoint[1]-outpoint2[1]))/(mapymax-mapymin)*resy
        fgnewsizey = int(fgnewsizey)
        
        self.fgnewsizexy = (fgnewsizex,fgnewsizey)
        print(self.fgnewsizexy)
        
        ##Here the WMS Request parameters are defined including the bounding box.
        img = wms.getmap(   layers=['0'],
                             styles=[],
                             srs='EPSG:4326',
                             bbox=(mapxmin, mapymin, mapxmax, mapymax),
                             size=(resx, resy),
                             format='image/jpeg',
                             transparent=True
                             )
        out = open('./nationalmap.jpg', 'wb')
        out.write(img.read())
        out.close()
        

        
    def runtmapspreview(self):
        '''
        The idea of this method / function is to run through and render each
        time step and make sure the frames correspond to what the user feels
        look representable before running the time machine ruby script
        '''
        self.renderpv()
        self.trmmsk()
        
#------------------------------------------------------------------------------
#functions that need to be ran independent for multiprocess module
#------------------------------------------------------------------------------

def trim(im):
    '''
    This method like the one found above trims the background around the mesh
    to be close to the corners so we can use the xmax,xmin, ymax, ymin as our
    image boundaries. It is also located outside the class so that it can be
    used in the multiprocess package to take advantage of multi-core processing.
    '''
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def runtrim(args):
    '''
    This portion will go through each pixel of the image and if the pixel 
    corresponds to the background color it will put an alpha channel of 0 or
    fully transparent. This is so that all we see is the mesh on the basemap
    '''    
    
    fname = args[0]
    opacity = args[1]
    print args
    im = Image.open(fname)
    im = trim(im)
    im = im.convert("RGBA")
    pixdata = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            if pixdata[x, y] == (244, 171, 0, 255):
				pixdata[x, y] = (244, 171, 0, 0)
            elif fname == './images/legend.png':
                pass
            elif pixdata[x, y][3] == 255:
				pixdata[x, y] = (pixdata[x,y][0],pixdata[x,y][1],pixdata[x,y][2],opacity)
            else:
                pass
    im.save(fname)


  
def underlaymap(args):
    '''
    Run trhough each image and overlay it onto the downloaded basemap
    '''
    print args[0]
    hname = args[0]
    fgnewsizexy = args[1]
    overlayx = args [2]
    overlayy = args[3]
    path = "./images/"        
    tmcname = "new"
    tmcimgdir = "./tmc-1.2.1-linux/ct/"+tmcname+ ".tmc/0100-original-images/"

    background = Image.open('./nationalmap.jpg')
    overlay = Image.open(path + hname)
    overlay = overlay.resize((fgnewsizexy), PIL.Image.ANTIALIAS)
    background.paste(overlay, (overlayx,overlayy), overlay)
    background.save(tmcimgdir + hname)


def runtm(cores, mapxmin, mapxmax, mapymin, mapymax):
    '''
    This is a script to run the Time Machine Video creator from the command line
    This is the first version of the script
    '''

    print('Creating new text file') 
    #Name and directory of the defintion.tmc file
    defname = './tmc-1.2.1-linux/ct/new.tmc/definition.tmc'

    try:
        file = open(defname,'w')   # Trying to create a new file or open one
        file.write('''{
  "sort_by": "filename",
  "source": {
    "type": "images",

    "tilesize": 512
  },
  "videosets": [
    {
      "type": "h.264",
      "label": "720p",
      "size": [
        1280,
        720
      ],
      "compression": 24,
      "fps": "3"
    }
  ]
}''')        
        file.close()
    except:
        print('Something went with generating the definition.tmc file')
        sys.exit(0) # quit Python

    #Erase the files that might remain from a prior run which can cause problems
    try :
        shutil.rmtree('./tmc-1.2.1-linux/ct/new.tmc/0200-tiles')
    except :
        pass
    try :
        shutil.rmtree('./tmc-1.2.1-linux/ct/new.tmc/0300-tilestacks')
    except :
        pass
    try :
        shutil.rmtree('./tmc-1.2.1-linux/ct/new.timemachine')
    except :
        pass
    
    workdirectory = "./tmc-1.2.1-linux/ct"
    tmcname = "new"
    
    os.chdir(workdirectory)
    os.system("ruby ct.rb "+ tmcname + ".tmc " + tmcname + ".timemachine -j "+ str(cores))
    
    playercss = tmcname + '.timemachine/css/customUI.css'

    shutil.copyfile('../../legend.png','./new.timemachine/images/legend.png')
    
    #generate an updated css file for allowing the updated legend to be visible
    try:
        file = open(playercss,'w')   # Trying to create a new file or open one
        file.write('''@charset "UTF-8";

.modisCustomPlay.ui-button {
  position: absolute;
  width: 50px;
  height: 50px;
  bottom: 7px;
  left: 21px;
  background: white;
  border: 1px solid #656565;
  border-radius: 35px !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  z-index: 10;
  outline: none;
}

.modisTimeText {
  position: absolute;
  top: 0px;
  width: 91px;
  height: 26px;
  font-size: 28pt;
  text-shadow: -1px 0 #656565, 0 1px #656565, 1px 0 #656565, 0 -1px #656565, 2px 2px 3px rgba(0,0,0,0.3);
  font-family: Arial, Helvetica, sans-serif;
  text-align: right;
  margin-top: -42px;
  margin-left: 14px;
  color: white;
  font-weight: lighter;
  background-color: transparent;
  border: 0px solid #656565;
  z-index: 9;
  border-radius: 3px;
  cursor: default;
}

.modisCustomToggleSpeed.ui-button {
  position: absolute;
  width: 56px;
  height: 16px;
  top: 36px;
  left: 105px;
  background: white;
  border: 1px solid #656565;
  border-radius: 3px !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  z-index: 10;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8pt;
  color: #656565;
  display: none;
}

.modisCustomToggleSpeed .ui-button-text {
  text-align: center;
  padding: 0px;
  padding-top: 0px;
  margin-left: 1px;
}

.toggleLock.ui-button {
  position: absolute;
  width: 20px;
  height: 16px;
  top: -6px;
  left: 124px;
  background: white;
  border: 1px solid #656565;
  border-radius: 3px !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  z-index: 11;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8pt;
  color: #656565;
  display: none;
}

.toggleLock .ui-button-text {
  text-align: center;
  padding: 0px;
  margin-left: 12px;
}

.toggleLock .ui-icon {
  padding: 0px;
  margin-left: -8px;
}

.toggleLockType.ui-button {
  position: absolute;
  width: 38px;
  height: 16px;
  top: 30px;
  left: 161px;
  background: white;
  border: 1px solid #656565;
  border-radius: 3px !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  z-index: 9;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8pt;
  color: #656565;
  display: none;
}

.toggleLockType .ui-button-text {
  text-align: center;
  padding: 0px;
  margin-left: 0px;
}

.toggleLockType .ui-icon {
  padding: 0px;
  margin-left: 0px;
}

.monthSpinnerContainer {
  left: 77px;
  top: -76px;
  position: absolute;
  cursor: pointer;
  z-index: 10;
}

.monthSpinnerTxt {
  left: 32px;
  top: 46px;
  text-shadow: -1px 0 #656565, 0 1px #656565, 1px 0 #656565, 0 -1px #656565, 2px 2px 3px rgba(0,0,0,0.3);
  position: absolute;
  font-size: 18px;
  color: white;
  width: 48px;
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: 550;
}

.googleLogo {
  width: 235px;
  height: 581px;
  position: absolute;
  bottom: 80px;
  right: 15px;
  border: 0px;
  background-image: url("../images/legend.png");
  -ms-transform: scale(0.5); /* IE 9 */
  -webkit-transform: scale(0.5); /* Chrome, Safari, Opera */
  transform: scale(0.5);
  -ms-transform-origin: 100% 100%;
  -webkit-transform-origin: 100% 100%;
  transform-origin: 100% 100%;
}

.googleLogo-touchFriendly {
  bottom: 95px;
}

.customControl {
  position: absolute;
  background-color: rgba(255,255,255,0);
  height: 60px;
  left: 0px;
  right: 0px;
  bottom: 0px;
  width: auto;
  z-index: 19;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
}

.customTimeline {
  position: absolute;
  height: inherit;
  margin-top: 0px;
  width: auto;
}

.customTimeline-touchFriendly {
  margin-top: -29px;
}



.timeText {
  position: absolute;
  top: 0px;
  left: 41px;
  width: 80px;
  height: 25px;
  font-size: 8pt;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  font-family: Arial, Helvetica, sans-serif;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 37px;
  padding-right: 0px;
  color: #656565;
  font-weight: normal;
  background-color: white;
  border: 1px solid #656565;
  z-index: 6;
  border-radius: 3px;
  cursor: default;
  text-align: left;
}

.timeText-touchFriendly {
  top: -28px;
  left: 63px;
  width: 81px;
  height: 33px;
  font-size: 6pt;
}

.timeTextTour {
  left: 23px;
  width: 81px;
  padding-left: 35px;
}

.timeTextHover {
  position: absolute;
  font-size: 6pt;
  text-shadow: -1px 0 #656565, 0 1px #656565, 1px 0 #656565, 0 -1px #656565, 2px 2px 3px rgba(0,0,0,0.3);
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
  color: white;
  font-weight: normal;
  cursor: default;
  z-index: 1;
  opacity: 1;
  cursor: pointer;
  display: none;
}

.endTimeDotClickRegion {
  position: absolute;
  border: 0px;
  opacity: 0;
  cursor: pointer;
  z-index: 6;
}

.endTimeDotContainer {
  position: absolute;
  border: 0px;
}

.endTimeDot {
  border: 1px solid #656565;
  background-color: white;
  opacity: 1;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  margin: 0px auto;
}

.timeTickContainer {
  position: absolute;
  border: 0px;
}

.timeTickGrow {
  border: 1px solid white !important;
  background-color: transparent !important;
}

.timeTick {
  margin: 0px auto;
  border: 1px solid #656565;
  background-color: white;
  opacity: 1;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  border-radius: 2px;
}

.timeTickClickRegion:focus {
  outline: 0;
}

.currentTimeTick {
  position: absolute;
  border: 1px solid #656565;
  background-color: white;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  border-radius: 2px;
  z-index: 5;
}

.timeTickClickRegion {
  position: absolute;
  border: 0px;
  opacity: 0;
  cursor: pointer;
  z-index: 6;
}

.customToggleSpeed.ui-button {
  position: absolute;
  width: 55px;
  height: 23px;
  top: 30px;
  left: 75px;
  background: white;
  border: 1px solid #656565;
  border-radius: 3px !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  z-index: 9;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8pt;
  color: #656565;
  display: none;
}

.customToggleSpeed-touchFriendly.ui-button {
  width: 67px;
  height: 25px;
  top: 14px;
  left: 102px;
  font-size: 10pt;
}

.customToggleSpeed .ui-button-text {
  text-align: center;
  padding: 0px;
  padding-top: 3px;
}

.customPlay.ui-button {
  position: absolute;
  width: 50px;
  height: 50px;
  bottom: 20px;
  left: 20px;
  background: white;
  border: 1px solid #656565;
  border-radius: 35px !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
  z-index: 10;
  outline: none;
}

.customPlay-touchFriendly.ui-button {
  width: 70px;
  height: 70px;
  bottom: 30px;
}

.customHelpLabel.ui-button {
  position: absolute;
  width: 25px;
  height: 25px;
  bottom: 30px;
  right: 20px;
  background: white;
  border: 1px solid #656565;
  border-radius: 15px !important;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
}

.customHelpLabel-touchFriendly.ui-button {
  width: 40px;
  height: 40px;
  bottom: 44px;
  border-radius: 21px !important;
}

.customHelpLabel .ui-icon {
  margin-top: -9px;
}

.customInstructions {
  background-color: rgba(0, 0, 0, 0.5);
  position: absolute;
  top: 0px;
  left: 0px;
  bottom: 0px;
  right: 0px;
  width: auto;
  height: auto;
  z-index: 999;
  display: none;
}

.customInstructions span {
  font-size: 12px;
  color: black;
  position: absolute;
  display: block;
  line-height: 18px;
}

.customInstructions p {
  font-size: 12px;
}

.customInstructions-touchFriendly p {
  font-size: 16px;
}

.customInstructions span.customMovehelp {
  top: 30px;
  left: 110px;
  width: 140px;
  padding: 68px 0px 0px 0px;
  color: white !important;
  background-repeat: no-repeat;
  background-position: center top;
  background-image: url(../images/drag_mouse_white.png);
}

.customInstructions-touchFriendly span.customMovehelp {
  position: absoulte;
  top: 35%;
  left: 30%;
  width: 380px;
  padding: 112px 0px 0px 88px;
  background-image: url(../images/touch/drag_mouse_white.png);
}

.customInstructions span.customZoomhelp {
  background-color: white;
  border: 1px solid #656565;
  top: 150px;
  left: 67px;
  overflow: visible;
  border-radius: 3px;
}

.customInstructions-touchFriendly span.customZoomhelp {
  top: 50px;
}

.customInstructions span.modisCustomSpeedhelp {
  background-color: white;
  border: 1px solid #656565;
  bottom: 32px;
  left: 105px;
  overflow: visible;
  border-radius: 3px;
}

.customInstructions span.customSpeedhelp {
  background-color: white;
  border: 1px solid #656565;
  bottom: 35px;
  left: 74px;
  overflow: visible;
  border-radius: 3px;
}

.customInstructions-touchFriendly span.customSpeedhelp {
  bottom: 48px;
  left: 104px;
}

.customInstructions span.customZoomhelp p {
  margin: 0px -6px 0px -11px;
  padding: 12px 0px 12px 30px;
  background-repeat: no-repeat;
  background-position: center left;
  background-image: url(../images/bubble_edge_vertical_white.png);
  width: 190px;
}

.customInstructions-touchFriendly span.customZoomhelp p {
  width: 240px;
}

.customInstructions span.modisCustomSpeedhelp p {
  margin: 0px 0px -11px 0px;
  padding: 12px 15px 22px 15px;
  background-repeat: no-repeat;
  background-position: 20px 100%;
  background-image: url(../images/bubble_edge_horizontal_white.png);
  width: 190px;
}

.customInstructions-touchFriendly span.modisCustomSpeedhelp p {
  width: 290px;
}

.customInstructions span.customSpeedhelp p {
  margin: 0px 0px -11px 0px;
  padding: 12px 15px 22px 15px;
  background-repeat: no-repeat;
  background-position: 20px 100%;
  background-image: url(../images/bubble_edge_horizontal_white.png);
  width: 190px;
}

.customInstructions-touchFriendly span.customSpeedhelp p {
  width: 250px;
}''')
        file.close()
    except:
        print('Something went with generating the player.css file')
        sys.exit(0) # quit Python
        
    fileone = open('../../tstepstotext.txt', 'r')
    fileoneread = fileone.read()
    
    capture_times = tmcname + '.timemachine/tm.json'
    
    try:
        file = open(capture_times,'w')   # Trying to create a new file or open one
        file.write('''{
  "datasets": [
    {
      "id": "crf24-3fps-1708x960",
      "name": "720p"
    }
  ],
  "sizes": [
    "720p"
  ],
  "capture-times": [
''' + fileoneread + '''
  ],
  "projection-bounds": {
      "east": ''' + str(mapxmax) +''',
      "north": ''' + str(mapymax) +''',
      "south": ''' + str(mapymin) +''',
      "west": ''' + str(mapxmin) +''',
      }
}''')
        file.close()

    except:
        print('Something went wrong with generating the capture times tm.json file')
        sys.exit(0) # quit Python
        
        
        
    viewhtml = tmcname + '.timemachine/view.html'
    
    try:
        file = open(viewhtml,'w')   # Trying to create a new file or open one
        file.write('''<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>

    <link href="css/snaplapse.css" rel="stylesheet" type="text/css"/>
    <link href="css/jquery-ui/smoothness/jquery-ui.custom.css" rel="stylesheet" type="text/css"/>
    <link href="css/defaultUI.css" rel="stylesheet" type="text/css"/>
    <link href="css/smallGoogleMap.css" rel="stylesheet" type="text/css"/>
    <link href="css/scaleBar.css" rel="stylesheet" type="text/css"/>
    <link href="css/visualizer.css" rel="stylesheet" type="text/css"/>
    <link href="css/annotator.css" rel="stylesheet" type="text/css"/>
    <link href="css/customUI.css" rel="stylesheet" type="text/css"/>

    <script src="js/jquery/jquery.min.js" type="text/javascript"></script>
    <script src="js/jquery/jquery-ui.custom.min.js" type="text/javascript"></script>
    <script src="js/jquery/plugins/mouse/jquery.mousewheel.min.js" type="text/javascript"></script>
    <script src="js/kinetic/kinetic.min.js" type="text/javascript"></script>
    <script src="js/org/gigapan/util.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/videoset.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/parabolicMotion.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/timelapse.js" type="text/javascript"></script>
    <script src="js/Math.uuid.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/snaplapse.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/snaplapseViewer.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/mercator.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/visualizer.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/annotator.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/scaleBar.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/smallGoogleMap.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/customUI.js" type="text/javascript"></script>

    <script src="js/org/gigapan/timelapse/defaultUI.js" type="text/javascript"></script>
    <script src="js/org/gigapan/timelapse/urlEncoder.js" type="text/javascript"></script>
    <script src="ajax_includes.js" type="text/javascript"></script>
    <script src="template_includes.js" type="text/javascript"></script>

    <script src="https://maps.google.com/maps/api/js?sensor=false&libraries=places" type="text/javascript" ></script>

    <script type="text/javascript">
      jQuery.support.cors = true;

      var url = "./";

      function init() {
        var settings = {
          url: url,
          enableEditor: true,
          onTimeMachinePlayerReady: function(viewerDivId) {
          },
          datasetType: "landsat",
          scaleBarOptions: {
            scaleBarDiv: "scaleBar1"
          },
          smallGoogleMapOptions: {
            smallGoogleMapDiv: "smallGoogleMap1"
          },
          disableTourLooping: true,
          mediaType: ".mp4",
          showFullScreenBtn: false,
          useThumbnailServer: false,
          showEditorModeButton: false
        };
        timelapse = new org.gigapan.timelapse.Timelapse("timeMachine", settings);
      }

      $(init);
    </script>
  </head>
  <body>
    <div id="timeMachine"></div>
  </body>
</html>''')
        file.close()

    except:
        print('Something went wrong with generating the capture times view.html file')
        sys.exit(0) # quit Python
    

    try:
        os.chdir(tmcname + '.timemachine/')
        os.system("ruby update_ajax_includes.rb")
    except:
        print('Capture times could not be updated')
        sys.exit(0) # quit Python
    
    print ("Your timemachine video entitled " + tmcname + ".timemachine was created. It can be viewed in your browser by opening " + workdirectory + "/" + tmcname + ".timemachine/view.html")
    
#------------------------------------------------------------------------------
#main process
#------------------------------------------------------------------------------
    

user_parameter = 'meshSurfacewaterDepth'
user_contour = 'bluetored'
user_opacity = 0.16




if __name__=="__main__":    
#
###
    runtmaps = tmaps(user_parameter,user_contour,user_opacity)
    runtmaps.renderpv()
    runtmaps.getbasemap()
 
    
    path = "./images/"
    opacity = int(runtmaps.opacity*255)
    combinations = [(os.path.join(path,fname), opacity) for fname in os.listdir(path)]
    
    pool = multiprocessing.Pool()                                      
    result = pool.imap(runtrim, 
                      combinations,
                      chunksize=1)
   
    pool.close()
    pool.join()
    
    
    legenddir = "./images/legend.png"
    legendim = Image.open(legenddir)
    reslegend = (235,581)
    newlegend = legendim.resize(reslegend)
    newlegend.save("./legend.png")
    os.remove(legenddir)
    
    
    tmcname = "new"
    parenttmdir ="./tmc-1.2.1-linux/ct/"+tmcname+ ".tmc"
    tmcimgdir = "./tmc-1.2.1-linux/ct/"+tmcname+ ".tmc/0100-original-images/"
    
    try :
        shutil.rmtree(parenttmdir)
    except :
        pass
    
    try :
        if not os.path.exists(parenttmdir):
            os.makedirs(parenttmdir)
        if not os.path.exists(tmcimgdir):
            os.makedirs(tmcimgdir)
    except :
        pass
    path = "./images/"
    fgnewsizexy = runtmaps.fgnewsizexy
    overlayx = runtmaps.overlayx
    overlayy = runtmaps.overlayy
    underlaycombo = [(hname, fgnewsizexy, overlayx, overlayy) for hname in os.listdir(path)]


    pool = multiprocessing.Pool()                                      
    result = pool.imap(underlaymap, 
                      underlaycombo,
                      chunksize=1)
   
    pool.close()
    pool.join()

    try :
        shutil.rmtree(path)
    except :
        pass
    print('Each rendered image has been overlain onto a basemap')
            
    mapxmin = runtmaps.mapxmin
    mapxmax = runtmaps.mapxmax
    mapymin = runtmaps.mapymin
    mapymax = runtmaps.mapymax
    
    cores = 4
    runtm(cores, mapxmin, mapxmax, mapymin, mapymax)
    