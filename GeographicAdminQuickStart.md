# Geographic Admin #
Getting started with the Geographic Admin Project

### Overview ###

This [Download](http://code.google.com/p/geodjango-basic-apps/source/browse/trunk/projects/geographic_admin) provides a sample project called 'geographic\_admin' with an application called 'world'.

The project code shows the minimal code needed to spatially enable the the Admin and Databrowse contrib applications with an OpenLayers map interface and OpenStreetMap basedata in the Google Mercator Projection (EPSG:900913), utilizing a world borders shapefile from [Thematic Mapping Blog](http://www.thematicmapping.org) in WGS 84 projection (EPSG:4326).

  * This project should be a useful place to start if you are familiar with Django but new to GeoDjango and GIS/mapping ideas. It should also be useful to folks familiar with mapping but new to web development and not afraid to dive into some python code. With just a few settings tweaks to your django configuration file for your database user and password you should be able to get up and running.

  * The biggest challenge for users new to GIS will be installing the dependencies of GDAL, GEOS, Proj.4and PostGIS. If you have trouble feel free to drop into the #geodjango room on irc.freenode.net to ask questions. If you get frustrated with these installations, you won't be alone. Even seasoned GIS developers can run into tricky installation issues with the c libraries of GDAL and GEOS, and PostGIS (because it depends upon GEOS and Proj.4).

### Dependencies for GeographicAdmin ###

  * Django >= 1.0
  * PostgreSQL
  * PostGIS
  * Psycopg2
  * GEOS
  * Proj.4
  * GDAL
  * Internet Connection (for OpenLayers JS and OpenStreetMap tiles)

**See http://code.djangoproject.com/wiki/GeoDjangoInstall for all installation details.**

## Steps to Run Geographic Admin ##

### Step 1  |  Make Sure Django is Installed ###

> a. Install Django from Trunk:
```
svn co http://code.djangoproject.com/svn/django/trunk/ django-svn-trunk
```
> Or grab the latest release from: http://www.djangoproject.com/download/

> b. Make sure that Django is on your PYTHONPATH.
```
$ export PYTHONPATH=/path/to/django-svn-trunk:
# or put that in your .bash_profile (environment settings)
```

> c. Test that Django can be found on your PYTHONPATH
```
$ python
>>> import django # should cause no errors
```

> d. OPTIONAL: Confirm your Django import location (watch out for multiple installations):
```
>>> django.__file__
'/Users/spring/src/django-svn-trunk/django/__init__.py'
# confirm that is the path to Django folder you just downloaded
```

### Step 2  |  Download the Geographic Admin Project ###

Download the Geographic Admin project [directory](http://code.google.com/p/geodjango-basic-apps/source/browse/trunk/projects/geographic_admin) to your desired location on your local filesystem.


```
$ svn checkout http://geodjango-basic-apps.googlecode.com/svn/trunk/projects/geographic_admin 
$ cd geographic_admin # your new project directory
```

  * **Note**: this project does not include the project name (only the app name) in any of the code, therefore maintaining a more flexible design approach. For an example of this note that the settings.py uses `ROOT_URLCONF = 'urls'` rather than `'geographic_admin.urls'`, allowing you to rename the project folder to anything you'd like. See Malcolm Tredinnick's post on ['Developing Without Projects'](http://www.pointy-stick.com/blog/2007/11/09/django-tip-developing-without-projects/) for background on this approach.

  * Also, this project's settings.py uses dynamic paths for a variety of other settings so you shouldn't need to put the project folder on your PYTHONPATH. The development server ( `python manage.py runserver` ) will handle assigning the needed paths at startup.

### Step 3  |  Create your Database ###


> a. If you are creating your first PostGIS database, create a **template** like so (otherwise skip to step 3b):
```
# Create a database with UTF encoding
$ createdb -E UTF8 -O postgres -U postgres template_postgis

# Load the required language for PostGIS
$ createlang plpgsql -d template_postgis -U postgres

# Load postgis functions and spatial reference info
# which are sometimes installed in the postgres share directory ($ pg_config --sharedir)
# Also look for lwpostgis.sql and spatial_ref_sys.sql in (/usr/share/  or /usr/local/share/)

# Once you have found the correct location, load the first sql into your template db:
$ psql -d template_postgis -U postgres -f /usr/share/lwpostgis.sql

# Note: ignore any NOTICES, like 'psql:/usr/share/lwpostgis.sql:44: NOTICE:  type "histogram2d" is not yet defined'
# You should see output like:
BEGIN
CREATE FUNCTION
CREATE OPERATOR
CREATE TYPE
CREATE AGGREGATE
COMMIT

# Then load the geographic projection tables
$ psql -d template_postgis -U postgres -f /usr/share/spatial_ref_sys.sql

# if you get an error about not being able to find  `geos` add /usr/local/lib to /etc/ld.so.conf
# And run:
$ ldconfig # Then restart PostgreSQL
```

  * You can now use this template for any future GeoDjango projects.

> b. Create a postgis enabled database called geoadmin from the template:
```
$ createdb -T template_postgis -U postgres geoadmin
```

### Step 4  |  Check your projections ###

Projections Background

  * To use the custom `ModelAdmin` subclass available in GeoDjango and used in this app called 'OSMGeoAdmin', you need to add the google spherical mercator projection to your database's `spatial_ref_sys` table. Unfortunately its not going to be there by default. If you forgot to do this you will see an error like:
```
AddToPROJ4SRSCache: Cannot find SRID (900913) in spatial_ref_sys
```

  * **Note**: you may want to add this projection to your `template_postgis` database.

How to Add Google Spherical Mercator

  * The load\_data.py script (see Step 8 below) will attempt to add the google mercator projection automatically when importing the sample data. If you do not rely on this script to load data you will need to add the google projection into your database manually.
    * GeoDjango also includes a utility (that requires a proper installation of GDAL 1.5.2 or the setting of the GDAL\_DATA\_DIR for <= 1.5.1) that will add the projection for you:
```
from django.contrib.gis.utils import add_postgis_srs
add_postgis_srs(900913)
```
  * This projection can also be found in the [utilities folder](http://geodjango-basic-apps.googlecode.com/svn/trunk/projects/geographic_admin/utilities/) as an sql insert as originally downloaded from: http://spatialreference.org/ref/user/google-projection/

### Step 5  | Edit your settings.py ###

Set your postgres user and password in settings.py

### Step 6  |  Use Django to setup your Database ###

Create your database schema
> a. OPTIONAL: **test** what table creation will look like in SQL with:
```
$ python manage.py sqlall world
# if you get an error that says: 
# ImportError: No module named django.core.management
# then go back to Step 1!
```

> You should get the table creation sample SQL output with special OpenGIS geometry hooks:
```
BEGIN;
CREATE TABLE "world_worldborders" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "area" integer NOT NULL,
    "pop2005" integer NOT NULL,
    "fips" varchar(2) NOT NULL,
    "iso2" varchar(2) NOT NULL,
    "iso3" varchar(3) NOT NULL,
    "un" integer NOT NULL,
    "region" integer NOT NULL,
    "subregion" integer NOT NULL,
    "lon" numeric(8, 3) NOT NULL,
    "lat" numeric(7, 3) NOT NULL
)
;
SELECT AddGeometryColumn('world_worldborders', 'geometry', 4326, 'MULTIPOLYGON', 2);
ALTER TABLE "world_worldborders" ALTER "geometry" SET NOT NULL;
CREATE INDEX "world_worldborders_geometry_id" ON "world_worldborders" USING GIST ( "geometry" GIST_GEOMETRY_OPS );
COMMIT;
```

> b. Now, let Django create your database schema with:
```
$ python manage.py syncdb
#say yes to the prompt to create a superuser (this will be your Admin Panel login)
```

> Make sure in the syncdb output you see the line:
```
Installing custom SQL for world.WorldBorders model
```

### Step 7  |  View your Project in a Browser ###

> a. Test the application by running the development server
```
$ python manage.py runserver
# ...then go to http://localhost:8000/
#...quit with ctrl -c
```

> b. If you are installing on a **remote server** and want to view via the web:
```
$ python manage.py runserver 0.0.0.0:8000
# ...then go to http://your_domain_name:8000/
```

### Step 8   |  Load Some Actual Spatial Data ###

> a. Load the sample data with the provided script (Uses GDAL 'layermapping')
```
$ python load_data.py
```
  * This should output the countries loaded if successful:
```
[...]
Saved: Falkland Islands (Malvinas)
Saved: Micronesia, Federated States of
Saved: French Polynesia
Saved: France
Saved: Gambia
Saved: Gabon
Saved: Georgia
Saved: Ghana
[...]
```

  * If you get error like `ImportError: cannot import name mapping`, then it either means you have not properly installed GDAL or GeoDjango cannot find the libgdal library using `ctypes.util.find_library`. See http://geodjango.org/docs/install.html#id20 for more details on installation help.
```
$ python load_data.py 
Traceback (most recent call last):
  File "load_data.py", line 16, in <module>
    from django.contrib.gis.utils import mapping, LayerMapping, add_postgis_srs
ImportError: cannot import name mapping
```

### Step 9   |  View your Project with Data ###

Run the server again and enjoy testing out the Admin and Databrowse:
```
$ python manage.py runserver
```


# FAQ #

**Q**: What version of Django do I need to use to get GeoDjango?

**A**: As of August 5th, GeoDjango can be found in SVN trunk within the contrib/gis folder. Download a checkout of svn trunk or a Django >=1.0 release.

**Q**: Okay, so this is a full example project, but is there a tutorial on how to add GeoDjango functionality to my existing application?

**A**: Yes, see FOSS4GWorkshop and http://geodjango.org/docs/tutorial.html

**Q**: I'm getting a 'module OSMGeoAdmin not found error'. What's causing that?

**A**: OSMGeoAdmin is a special GeoDjango subclass of the Django ModelAdmin that will automatically create an OpenLayers map with OpenStreetMap tiles. It requires a working installation of the GDAL library, so if GDAL is not found the Admin will not work and that `OSMGeoAdmin` class will not be available. So, either install GDAL or switch the ModelAdmin to `GeoModelAdmin` which does not depend on GDAL.

**Q**: I'm getting a 'Exception Value: Error encountered checking Geometry returned from GEOS C function GEOSGeomFromHEX\_buf' error when saving data in the Admin panel map. Is that a GEOS installation problem?

**A**: Maybe, but it is much more likely an installation problem with your Proj.4 library, since Proj.4 is used (within PostGIS) to do the coordinate transformations needed when saving spatial objects in the admin. You are likely seeing a GEOS error because GEOS is the library smart enough to see that something is wrong, while you are missing some kety Proj.4 files. Go back and reinstall Proj.4 and the Proj.4 transformation/datum data. See: http://geodjango.org/docs/install.html#proj-4.  For more info see: http://code.google.com/p/geodjango-basic-apps/issues/detail?id=3

**Q**: I'm on Windows and getting an Error like: "the ordinal 2254 could not be located" in libeay32.dll, when running the HAS\_GDAL tests after installation. Subsequent attempts to run the tests result in "HAS\_GDAL" = false.

**A**: You've got a problem with your libraries that relate to libeay32.dll and this is likely not just a GeoDjango problem. Try installing Win32 OpenSSL to fix the problem of different libeay32.dll versions on your system.

**Q**: I've loaded up this project and the first country I viewed in the Admin does not work. I tried clicking on Afghanistan at this url:  http://localhost:8000/admin/world/worldborders/31/ as simply got a blank blue map with a mysterious dot in the middle that says 'North Pole'. One time it also said 'Peñagrande'. WTF?

**A**: You must be using Safari which has a bug in it's regex parser. Because the vector failed the map defaults to 0,0 coordinates, which just happens to land on some interesting OSM data (http://lists.openstreetmap.org/pipermail/talk/2008-November/031421.html). Load it up in Firefox and you should get a vector layer of Afghanistan rather than a gas station in middle of the south Atlantic ocean. :)