#TMAPS App For Viewing Time Machines
*tethysapp-adhydro_streamflow*

**This app is created to run in the Tethys programming environment.
See: https://github.com/CI-WATER/tethys and http://tethys-platform.readthedocs.org/en/1.0.0/**

##Prerequisites:
- Tethys Platform (CKAN, PostgresQL, GeoServer)
- Browser that supports HTML5

##Installation:
Clone the app into the directory you want:
```
$ git clone https://github.com/CI-WATER/tethysapp-tmaps_app.git
$ cd tethysapp-tmaps_app
$ git submodule init
$ git submodule update
```
Then install the app in Tethys Platform:
```
$ . /usr/lib/tethys/bin/activate
$ cd tethysapp-tmaps_app
$ python setup.py install
$ python manage collectstatic

```
Restart the Apache Server:
See: http://tethys-platform.readthedocs.org/en/1.0.0/production.html#enable-site-and-restart-apache

##Quick Setup Workflow For Viewing Time Machines

- Use the TMAPS code on the CI-WATER GitHub repository for generating Time Machines
- To incorporate Time Machines into the TMAPS Tethys app, place the '.timemachine' folder generated from TMAPS into the 'public/time_machines' directory of the app.
- Be sure that there is a file called 'tmaps_app_info.txt' in the '.timemachine' folder which contains identifying metadata about your Time Machine.


##Updating the App:
Update the local repository and Tethys Platform instance.
```
$ . /usr/lib/tethys/bin/activate
$ cd tethysapp-tmaps_app
$ git pull
$ git submodule update
$ tethys manage collectstatic
```
Restart the Apache Server:
See: http://tethys-platform.readthedocs.org/en/1.0.0/production.html#enable-site-and-restart-apache