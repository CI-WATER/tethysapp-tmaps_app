from django.shortcuts import render
from .model import SessionMaker, StreamGage
import base64
import hmac, hashlib
import os
import json
from tethys_apps.sdk.gizmos import GoogleMapView
from tethys_apps.sdk.gizmos import MapView, MVDraw, MVView, MVLayer, MVLegendClass
from tethys_apps.sdk import get_spatial_dataset_engine




def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'tmaps_app/home.html', context)
def load(request):
    """
    Controller that will echo the name provided by the user via a form.
    """
    # Default value for name
    name = ''

    # Define Gizmo Options
    text_input_options = {'display_text': 'Enter New Project Name',
                          'name': 'name-input'}

    # Check form data
    if request.POST and 'name-input' in request.POST:
       name = request.POST['name-input']
       
    select_input2 = {'display_text': 'Select Supported File Type',
                'name': 'select1',
                'multiple': False,
                'options': [('ADHydro', '1'), ('GSSHA', '2'), ('RAPID', '3')],
                'initial': ['GSSHA']}


    # Create template context dictionary
    context = {'name': name,
               'text_input_options': text_input_options,
               'select_input2': select_input2}

    return render(request, 'tmaps_app/load.html', context)
    
def preview(request):
    """
    Controller that will echo the name provided by the user via a form.
    """
    # Default value for name
    name = ''

    slider2 = {'display_text': 'Opacity of Mesh Overlay',
               'name': 'slider2',
               'min': 0,
               'max': 1,
               'initial': 0.5,
               'step': 0.01,}
               
    select_input4 = {'display_text': 'Select The Parameter To Be Rendered',
                'name': 'select4',
                'multiple': False,
                'options': [('Groundwater Head', 'meshGroundwaterHead'), ('Surfacewater Depth', 'meshSurfacewaterDepth'),( 'Evaporation', 'meshEvaporation'), ('Transpiration', 'meshTranspiration')],
                'initial': ['Groundwater Head']}
                
    select_input3 = {'display_text': 'Select The Contour Theme',
                'name': 'select3',
                'multiple': False,
                'options': [('Cool to Warm', 'cooltowarm'), ('Blue to Cyan', 'bluetocyan'), ('Blue to Red', 'bluetored'),( 'Blue Yellow Red', 'blueyellowred'), ('Rainbow Desat', 'rainbowdesat')],
                'initial': ['Cool to Warm']}

    showpreview = False
    ##When the load page has submitted variables from the user, the code makes sure 
    ##the variables do not change after refereshing the context variable and sends 
    ##the user input variables to tmaps.py
    if request.POST and 'slider2' in request.POST:
       usr_slider2 = request.POST['slider2']
       usr_select4 = request.POST['select4']
       usr_select3 = request.POST['select3']
       
       def replace_line(file_name, line_num1, line_num2, line_num3, text1, text2, text3):
           '''This method is called to write out the changes the users submits
               and make sure they make it to the tmaps code'''
           lines = open(file_name, 'r').readlines()
           lines[line_num1] = text1
           lines[line_num2] = text2
           lines[line_num3] = text3
           out = open(file_name, 'w')
           out.writelines(lines)
           out.close()
    
       f = os.path.abspath(__file__)
       b = os.path.dirname(f)
       a = os.path.join(b,'tmaps_tethys.py')
       
       tmaps_input1 = 'user_parameter = \'' + usr_select4 + '\'\n'
       tmaps_input2 = 'user_contour = \'' + usr_select3 + '\'\n'
       tmaps_input3 = 'user_opacity = ' + usr_slider2 + '\n'
       
       replace_line(a,1274,1275,1276,tmaps_input1,tmaps_input2,tmaps_input3)

       
       
       ##Reset the variable sent by the user to the associated inital value that
       ##the object requires as an initial value
       if usr_select3 == 'cooltowarm':
            init_select3 = 'Cool to Warm'         
       elif usr_select3 == 'bluetocyan':
            init_select3 = 'Blue to Cyan'
       elif usr_select3 == 'bluetored':
            init_select3 = 'Blue to Red'
       elif usr_select3 == 'blueyellowred':
            init_select3 =  'Blue Yellow Red'
       elif usr_select3 == 'rainbowdesat':
            init_select3 = 'Rainbow Desat'
     
       else:
           pass
       
       if usr_select4 == 'meshTranspiration':
            init_select4 = 'Transpiration'         
       elif usr_select4 == 'meshSurfacewaterDepth':
            init_select4 = 'Surfacewater Depth'
       elif usr_select4 == 'meshGroundwaterHead':
            init_select4 = 'Groundwater Head'
       elif usr_select4 == 'meshEvaporation':
            init_select4 =  'Evaporation'
     
       else:
           pass    
       
       select_input4 = {'display_text': 'Select The Parameter To Be Rendered',
                'name': 'select4',
                'multiple': False,
                'options': [('Groundwater Head', 'meshGroundwaterHead'), ('Surfacewater Depth', 'meshSurfacewaterDepth'),( 'Evaporation', 'meshEvaporation'), ('Transpiration', 'meshTranspiration')],
                'initial': [init_select4]}
                
       slider2 = {'display_text': 'Opacity of Mesh Overlay',
               'name': 'slider2',
               'min': 0,
               'max': 1,
               'initial': usr_slider2,
               'step': 0.01,}
       
       select_input3 = {'display_text': 'Select The Contour Theme',
                'name': 'select3',
                'multiple': False,
                'options': [('Cool to Warm', 'cooltowarm'), ('Blue to Cyan', 'bluetocyan'), ('Blue to Red', 'bluetored'),( 'Blue Yellow Red', 'blueyellowred'), ('Rainbow Desat', 'rainbowdesat')],
                'initial': [init_select3]}

       showpreview = True


    # Create template context dictionary
    context = {'slider2': slider2,
               'select_input4': select_input4,
               'select_input3': select_input3,
               'showpreview': showpreview}
       
    
    return render(request, 'tmaps_app/preview.html', context)

    
def library(request):
    """
    Controller that facilitates the library.html page by pasing the project variables
    """
    
    #This will setup the paths for where the time machines are stored
    f = os.path.abspath(__file__)
    b = os.path.dirname(f)
    #This sets the directory to the subdirectories of where the time machines are located
    a = os.path.join(b,'public/time_machines')
    list_of_tm = os.listdir(a)
    if len(list_of_tm) > 1:
        time_machines_exist=True

        #Sets up a list for the use of the dropdown option
        tm_info_list = []
        tm_options = []
        tm_num = 1

        #Loops through each time machine directory and reads the tmaps_app_info.txt
        for tm in list_of_tm:
            if ".timemachine" not in str(tm):
                continue

            get_select_titles = os.path.join(b,'public/time_machines/'+tm+'/tmaps_app_info.txt')
            tm_info = open(get_select_titles, 'r').read().splitlines()

            get_tm_view = os.path.join(b,'/static/tmaps_app/time_machines/'+tm+'/view.html')

            tm_info_list.append((tm_info, str(tm_num), get_tm_view))
            tm_options.append((tm_info,str(tm_num)))
            tm_num = tm_num + 1


        select_input5 = {'display_text': 'Select Saved Project For Viewing',
                    'name': 'select_input5',
                    'multiple': False,
                    'options': tm_options,
                    'attributes': 'id=select_input5',
                    'initial': tm_info_list[0]}


        # Create template context dictionary
        context = {'select_input5': select_input5,
                   'time_machines_exist': time_machines_exist,
                   'tm_info_list': json.dumps(tm_info_list)}

        return render(request, 'tmaps_app/library.html', context)

    else:
        time_machines_exist = False

        # Create template context dictionary
        context = {'time_machines_exist': time_machines_exist}

        return render(request, 'tmaps_app/library.html', context)


def makeyourown(request):
    """
    Controller that facilitates the makeyourown.html page by pasing the project variables
    """

    context = {}

    return render(request, 'tmaps_app/makeyourown.html', context)