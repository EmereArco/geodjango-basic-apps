# GeoDjango Workshop, FOSS4G 2008 #

**Presented by Josh Livni and Christopher Schmidt**

**Document contributions from Tim Sutton and Tyler Erickson**

TOPICS
  * 1: Intro
  * 2: Installation
  * 3: Starting your project
  * 4: Creating your application
  * 5: Modifying some actual data
  * 6: Building A Public Website
  * 7: Importing from a Shapefile
  * 8: Some Actual GIS
  * 9: More GeoDjango Features


### 1.  INTRODUCTION ###

NOTE:  This document has been modified from the actual workshop given at FOSS4G.  For example, installation instructions have been removed (as they will soon be deprecated by those available at geodjango.org).  Various other modifications have also taken place.

Code for this project may be downloaded from _http://geodjango-basic-apps.googlecode.com/svn/trunk/projects/cape/_


---


According to django website (djangoproject.com), Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.  For projects where you need to get a robust database driven application online in a timely manner, Django can be an exceptional tool.

In line with another popular Django slogan, GeoDjango has been called a Geographic Web Framework for Perfectionists with Deadlines.  As of Django v1.0, GeoDjango is part of the core set of Django packages that ship with the default download.  Adding Geographic capabilities to a Django project is as simple as ensuring you have the base software stack, and enabling the gis contrib package within Django.

This workshop is designed for people who may be new to Django, but have familiarity with python and general web concepts, such as HTML/CSS, templating, and apache or other web servers.  Although it is not required, you will likely get more out of this workshop if you try make it through the introductory Django tutorial at djangoproject.com before the FOSS4G conference.



### 2: INSTALLATION ###

GeoDjango can work with different spatial databases, and can function without GDAL/OGR.  However, for the purposes of this workshop we will be using PostGIS and GDAL/OGR.


2.1: VMWare Virtual Machine (Recommended):

A VMWare image will be provided to workshop participants on DVD at the start of the workshop.

The VMWare image has all the required software pre-installed on a linux base, including:
  * GEOS
  * GDAL
  * PROJ.4
  * PostgreSQL
  * PostGIS
  * Python 2.5
  * pyscopg2
  * Django 1.0
  * OpenLayers

Under the assumption we may not have network access, the VMWare image also includes a WMS server that can be used by OpenLayers to display some basic administrative boundaries as a background to the data we'll be interacting with.

> VMWARE REQUIREMENTS:

  * DVD Reader (CD Reader does not count)
  * At least 6GB Free Space on hard drive
    * If Windows, be sure drive is NOT formatted FAT32 (must be NTFS)
  * VMWare Player v2.05 or VMWare Fusion (for MAC) installed and working


2.3: Self Installation:

REMOVED

2.4 Test your installation

Before we get started with Django, let's be sure we have all the software correctly installed.
  * Open a new terminal window (on windows, do Start -> run -> cmd)
  * Go to the location you want to start your new project
    * On Linux:  _cd /projects/geodjango_
On Windows:  cd \geodjango
  * Type "python" to start the python interpreter, then do:
  * _import django_
You should get no response
  * Then type:
```
from django.contrib.gis.gdal import HAS_GDAL
HAS_GDAL
```
You should get a result of 'True'.  If not, something is amiss with your GDAL installation.


### 3:  STARTING YOUR GEODJANGO PROJECT ###

For this workshop, we will be creating a project called "cape", a simple database driven web application that lets users add and edit geospatial data via a map interface.

NOTE:  A django 'project' can contain many django 'applications', which can exist simply as code inside subfolders within your project folder or a folder anywhere on your PYTHONPATH.  We will be creating both a project and an application from scratch, and we will also include some other applications to bring in some features for us that we don't want to build ourselves.  One nice thing about this is by decoupling our application from a particular website/project, we can reuse the generic application we're building today in any GeoDjango website with just a few simple lines of code saying to include it.

  * Create the Project: We will create a new project from scratch. Go to your project folder (eg c:\geodjango) and type:
```
django-admin.py startproject cape
```

> This will create a folder called cape with some basic python scripts to initiate a django project, including a manage.py script that can be run to do various django tasks and a settings.py file (see below).


> Note:  If django-admin is not in your path you may need to preface the command with the full path of the django binaries, (eg c:\python25\lib\site-packages\django\bin\ on windows)


  * Modify the Settings: In the cape project, we now have a settings.py, which you should open in your favorite text editor, and make some important changes:

```
DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'cape'
DATABASE_USER = 'postgres'      
#scroll down to see this
INSTALLED_APPS = (
#...don't delete what's already here
    'django.contrib.admin',
    'django.contrib.gis',
 )
```

> Note: you will also need to set the DATABASE\_PASSWORD to the password for your postgres user if it has one.


  * Create and Sync your Database: Now that we've told Django to include some contributed applications of interest, and where to find our database, we need to create the actual database for our website. From within the cape project folder type:
```
createdb -T postgis -U postgres cape
python manage.py syncdb 
```


  * NOTE:  If createdb is not on your path, you may need to preface the command with the full path of the postgres binaries, (eg c:\Program Files\PostgreSQL\8.3\bin on windows)
  * NOTE:  Your PostGIS template may be called template\_postgis, depending on the instructions your followed to create the initial postgis database.
  * During the syncdb process various tables will be installed in your database including an authentication table. It will prompt you for a superuser and choose a simple superuser name and password (user/user for example).


  * Start the Webserver: Finally!  At the command line in the cape folder, run this command to start up the built-in webserver:
```
python manage.py runserver
```

  * View the site: At this point, we have a basic web application (which doesn't do much), and can visit it by going to http://localhost:8000/.  You should notice an error page welcoming you to Django, but pointing out there's nothing to see yet.  As the error notes, we need to create some URLS we can use.

  * Modify your URLS:  The last step we need to do is tell Django what to do when someone actually tries to load a webpage.  We'll start by enabling the admin application, which will give you a nice interface for creating, editing, and deleting objects.  The controller for this is the urls.py in the cape folder.  Simply uncomment the following three lines :
```
from django.contrib import admin
admin.autodiscover()
# ...
(r'^admin/(. *)', admin.site.root),
```


  * View the site again: At this point, we have a basic web application (which doesn't do much), and can visit it by going to http://localhost:8000/admin and logging in with the superuser you created.  You should now see a welcome page showing Users and Groups and Sites - the default contrib packages that we kept installed.
    * Note:  If you are on windows, and get an error about GEOS\_LIBRARY\_PATH, this is a bug that is fixed in the svn trunk of django, but not in v1.0.  To fix this, add the following line to your settings.py:
    * GEOS\_LIBRARY\_PATH='c:\\geodjango\\gdal\\bin\\geos\_c\_fw.dll'




### 4:  CREATING YOUR APPLICATION ###

We're now going to import some administrative boundaries from a shapefile into GeoDjango.  Open up the geodjango python shell (python manage.py shell in the command prompt) to start it up again if you need, and inspect the Shapefile:

```
python manage.py startapp lionshead 
```
Django has now  created some more boilerplate for us, including some empty files that we'll be modifying to add functionality.  Note how you now have a new folder called lionshead, and inside the folder are 3 new files.

The next step is to tell Django to include this new application, like we did with some of the contributed ones above.  Modify your settings.py so the INSTALLED\_APPS tuple includes 'lionshead',

4.1 CREATING YOUR CUSTOM MODELS
In django lingo, we will have a variety of "models", each of which relates to a spatially enabled table in the PostGIS database.  To get an idea of some of the things geodjango offers us, we will be both creating the models by hand, and by auto-generating them from an existing shapefile.

Now is the time to break into teams, so you can help eachother out as you work to get your first models in this application up and running.  For the first phase, we will be creating models manually.  Each team will create the first two models by hand, and ensure they are able to work with the geographic data in these models using the default GeoDjango admin panel.

For this application, we're going to build a model for recording  Locations of Interest (points), and a model for storing election wards (polygons).

Open up your models.py, and let's create our first model.  Your models.py should look like this:
```
from django.contrib.gis.db import models
class InterestingLocation(models.Model):
    """A spatial model for interesting locations """
    name = models.CharField(max_length=50, )
    description = models.TextField() 
    interestingness = models.IntegerField() 
    geometry = models.PointField(srid=4326) #EPSG:4236 is the spatial reference for our data
    objects = models.GeoManager() # so we can use spatial queryset methods
 
    def __unicode__(self): return self.name 
```

Because we've added the lionshead application to our INSTALLED\_APPS for our project, and created a new model in the lionshead application, we can now run the syncdb command again to have django create the appropriate table for us in our PostGIS database:

```
python manage.py syncdb 
```

### 5:  MODIFYING SOME ACTUAL DATA ###

5.1  WITH THE PYTHON SHELL

  * It's important to know how to interact with django using the python command shell.  Don't worry if you're not a pro python programmer and/or are new to django.  Let's go to your command prompt in the cape folder, and start up the django shell:

```
python manage.py shell 
```
  * Before we go any further, we're going to load a little Django helper script to insert a new projection into PostGIS, so we can work with the 'spherical mercator' background maps for later in our project:

```
from django.contrib.gis.utils import add_postgis_srs
add_postgis_srs(900913) 
```

  * Create a new Interesting Location:
```
from lionshead.models import InterestingLocation
from django.contrib.gis.geos import Point
il = InterestingLocation()
il.name = 'some place'
il.interestingness = 3
il.geometry = Point(-16.57,14.0)
il.save() 
```

  * Now we've saved the point, we need a way to view it.  For this, we'll use a custom map-enabled admin view that comes with GeoDjango.


5.2  IN THE ADMIN

At this point, we could start building some views and templates that we will need in order to actually display data from this model in our public facing site.  However, since we're lazy (for now), let's register this model with the admin, and then we can use it to modify and view our data. First create a new file called "admin.py" in the lionshead folder, and add these import lines to the top:
```
from django.contrib.gis import admin
from models import  *
```

Below the imports, create a new OSMGeoAdmin class, and register the model with the admin package.  The OSMGeoAdmin uses OpenStreetMap data for the background, and displays points in a 'spherical mercator' projection.

```
class InterestingLocationAdmin(admin.OSMGeoAdmin):
     list_display = ('name','interestingness')
     list_filter = ('name','interestingness',)
     fieldsets = (
       ('Location Attributes', {'fields': (('name','interestingness'))}),
       ('Editable Map View', {'fields': ('geometry',)}),
     )
 
    # Default GeoDjango OpenLayers map options
     scrollable = False
     map_width = 700
     map_height = 325
```

# Register our model and admin options with the admin site


```
admin.site.register(InterestingLocation, InterestingLocationAdmin)
```
Ok - now, assuming no typos, we should be able to reload http://localhost:8000/admin in the browser and see our new Locations model.  Click on it, and then at the top right click 'Add Interesting Location' to add a new Interesting Location.  You will need to fill out the name and interestingness values (by default they are required, and we did not specify they are optional), and then you can click the map to add a new location, and save.

At this point, we have covered one of the key functionalities of GeoDjango and of building yourself a GIS enabled website:  An interactive map that lets you view/modify spatial data that's stored inside PostGIS.

To summarize what we've done so far:
  * Created a Django Project and Application
  * Created a new Model for point data
  * Registered our Model with the Admin package
  * Added and edited some data

### 6: BUILDING A PUBLIC WEBSITE ###

The next step we'll do is customize some views and associated templates which will be the public facing website.  To display our map publicly, we are going to build two basic items:
  * A KML of all our locations
  * An OpenLayers Map that displays the KML appropriately


6.1: OUR FIRST VIEW
  * Open up the views.py for editing, and type in the following:
```
from django.shortcuts import render_to_response
from django.contrib.gis.shortcuts import render_to_kml
from lionshead.models import  *
 
def all_kml(request):
     locations  = InterestingLocation.objects.kml()
     return render_to_kml("placemarks.kml", {'places' : locations}) 
```

> Pretty simple, eh?  As you can see, we've imported a few things:
    * 
      * render\_to\_response -- unused in our code so far
      * render\_to\_kml -- a geodjango shortcut for spitting out kml to our templates
      * all our models (for now, just InterestingLocation)
> In our all\_kml method, we simply retrieved all our InterestingLocation objects from the database, and sent them off to a "placemarks.kml" which can access them via a variable called "places".

6.2 OUR FIRST TEMPLATES

Next, we need to make that placemarks.kml.  Oh wait - actually we don't, since a basic templates.kml is already included for us with the GeoDjango installation.  You can go see it at django/contrib/gis/templates/gis/kml

Since Django knows about our contrib.gis package, and it's associated templates, we can use the placemarks.kml by telling our view where this specific template is relative to our base gis templates folder.
Change the render\_to\_kml in the view we made from "placemarks.kml" to the relative path from our gis contrib templates:  "gis/kml/placemarks.kml"/

NOTE:  If we wanted to customize these (which we will later), we could simply copy them to our own 'templates' subfolder, and they would take precedence over the default contrib templates, but for now these generic ones will do.

At this point, we should just be able to access our view and be good to go.  But how do we access it?

6.3 URLS

We still haven't given Django enough information to know how to direct users to a particular page.  This is where the urls.py comes in - it controls which views get loaded based on what URL a user is requesting.  Open up the urls.py and add the following import statement:
```
from lionshead.views import  *
  
And then, add this line under the admin tuple: 
(r'^kml/', all_kml) 
```
This URL pattern says that if someone goes to http://yoursite/kml ,django will run the all\_kml view, and do whatever it says to do (in our case, return some kml placemarks)

Now load up http://localhost:8000/kml

6.4 THE PUBLIC MAP PAGE

Not only did GeoDjango automagically set the appropriate KML mime-type for us, but with just a 3 line view and a simple url pattern, we have a nice kml showing all our geodata.  Feel free to add a new location or two via the Admin site, and reload the kml.

Now that we have a working kml feed, we can add it to a map.  But first we need a map to add it to, and for this we're going to create a new view and associated template that will display an openlayers map for the public:

Back in your views.py, add the following method:

```
def map_page(request):
     lcount = InterestingLocation.objects.all().count()
     return render_to_response('map.html', {'location_count' : lcount}) 
```

This view says that it will load a template called "map.html", and that template will get passed the total number of location objects we have in the database.  Let's create that template:

In your lionshead folder, create a folder called 'templates', and within this folder, create a new file called 'map.html'.   This file should look something like this:
```
<html>
  <head>
    <script src="http://openlayers.org/api/OpenLayers.js"></script>
    <script type="text/javascript">
        var map, base_layer, kml;
        function init(){
            map = new OpenLayers.Map('map');
            base_layer = new OpenLayers.Layer.WMS( "OpenLayers WMS",
               "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
            kml = new OpenLayers.Layer.GML("KML", "/kml/", 
               { format: OpenLayers.Format.KML });
            map.addLayers([base_layer, kml]);
            map.zoomToMaxExtent();
            }
    </script>
  </head>
  <body onload="init()">
    Hi.  There should be a total of {{location_count}} Locations.<br />
    <div id="map"></div>
  </body>
</html>
```
And again, we need to create a url mapping so we can get to this view.  In urls.py, add:
```
    (r'^$', map_page) 
```

We've now mapped the root of the site (/) to the index view we created, which in turn will display the map.html with the location\_count variable dynamically filled in by Django.

This combination of a view and a template (along with an associated url mapping) are how we'll build most of the public facing pages.  There are a variety of shortcuts that Django offers, letting you entirely skip the creation of views for common view tasks, and letting you build your views in a generic manner so they can be reused by multiple urls and templates, but all that is out of the scope of this workshop.

If we wanted to provide an alternative download form for users who wanted to open the data in something like (for example) Google Earth, we could add a regular HTML link to the /kml/ URL:
```
  <body onload="init()">
    Hi.  There should be a total of {{location_count}} Locations.<br />
    To see this data in Google Earth, <a href="/kml/">Open as KML</a>.
    <div id="map"></div>
  </body>
```

### 7: IMPORTING FROM A SHAPEFILE ###

We're now going to import some administrative boundaries from a shapefile into GeoDjango.  Open up the geodjango python shell (python manage.py shell in the command prompt to start it up again if you need , and inspect the Shapefile:

```
from django.contrib.gis.gdal import DataSource 
wards = DataSource('data/wards_4326.shp')
layer = wards[0]
print layer.fields
print len(layer) # getting the number of features in the layer
print layer.geom_type.name # Should a polygon
print layer.srs.name # WGS84
```


Now that we know what attributes the shapefile has, we can create a model for it.  Open up your models.py in your text editor, and add a new model:
```
class Ward(models.Model):
     """Spatial model for Cape Town Wards"""
     subcouncil = models.CharField(max_length=20)
     party = models.CharField(max_length=50)
     ward = models.CharField(max_length=50)
     cllr = models.CharField(max_length=150)
     geometry = models.MultiPolygonField(srid=4326)
     objects = models.GeoManager()
 
    def __unicode__(self): return '%s (%s)' % (self.cllr, self.party) 
```

Now that the Model is created, we can run syncdb to have django create us the associated table in the database.  At the command line, run:

```
python manage.py syncdb
```

And, back in our python shell, we can define the Layer Mapping and import the code

```
from lionshead.models import Ward
from django.contrib.gis.utils import mapping, LayerMapping
print mapping(wards)
lm = LayerMapping(Ward, wards, mapping(wards, geom_name='geometry'))
lm.save(verbose=True)
```

This will read the data from the provinces shapefile and load it into our Ward model in PostGIS.

As before, we need to hook this up into our Admin, so open up admin.py and add a new class:

```
class WardAdmin(admin.OSMGeoAdmin):
     list_display = ('cllr','ward')
     fieldsets = (
       ('Location Attributes', {'fields': (('cllr','ward'))}),
       ('Editable Map View', {'fields': ('geometry',)}),
     )
 
     scrollable = False
     map_srid = 4326
     debug = True
 
# Register our model and admin options with the admin site
 admin.site.register(InterestingLocation, InterestingLocationAdmin)
 admin.site.register(Ward, WardAdmin) 
```

NOTE:  We could also add more openlayers options to the admin.  For example, we can give a different URL for the OpenLayers library, as follows:
> openlayers\_url = '/static/openlayers/lib/OpenLayers/js'
In this case, we would need to also modify our urls.py so that /static would point to a local location for our static files:
```
     (r'^static/(?P<path>. *)$', 'django.views.static.serve', {
       'document_root': 'q:\projects\cape\static', 'show_indexes': True}),
```
For a larger list of options we can pass to the map admin, see http://code.djangoproject.com/browser/django/trunk/django/contrib/gis/admin/options.py


### 8: SOME ACTUAL GIS ###

Once we have done this, we could certainly create a similar KML output to the InterestingPoint KML we created above for all the Ward geometries. But as much fun as displaying one data layer at a time can be, let's instead create a more complex view that displays just one ward (which will be specified in the URL), and have this view feed a map template that highlights the appropriate ward, and all the Interesting Locations that are within 5 miles of that ward.


In this section, we'll be creating a ward-specific viewing page. That ward page will list the interesting points inside the ward, and list them in the HTML page, and finally display a map.

First, we'll edit the urls.py file. Earlier, we built a urls.py that had in it:
```
(r'^kml/', all_kml),
 (r'^/$', map_page) 
```
Now, we'll be adding one more URL to this list:
```

(r'^kml/', all_kml),
 (r'^/$', map_page),
 (r'^wards/(?P<id>[0-9] *)/', ward),
```

We've added an item for viewing a specific ward. You'll see here that there is additional syntax in this URL: This URL matching is a regular expression, and allows us to pull the ID from the URL and use it as a parameter to the ward function we're going to write.

There are two different queries we want to perform in order to build the ward page. First, we want to take the passed in ID, and we want to find the associated ward. If the ID is invalid, we want to return a 404 to the user. Django has a shortcut for this type of thing, because it's a relatively common operation. Like all shortcuts, it is in django.shortcuts, and it's called 'get\_object\_or\_404'. We'll use this to get our ward:

```
from django.shortcuts import get_object_or_404
 ...
 def ward(request, id):
     ward = get_object_or_404(Ward, pk=id)
```

Using this, we get the ward we care about as the ward variable. Then, we'll want to find nearby interesting points -- within 5 miles of the borders of our ward.

NOTE xxxxxx Change below to actually use a 5mile buffer xxxxxxxxx


```
def ward(request, id):
     ward = get_object_or_404(Ward, pk=id)
     interesting_points = InterestingLocation.objects.filter(
         geometry__intersects=(ward.geometry)) 
```

Then, we'll pass both of these objects -- the ward, and the list of locations -- into the ward template.

```
def ward(request, id):
     ward = get_object_or_404(Ward, pk=id)
     interesting_points = InterestingLocation.objects.filter(
          geometry__intersects=(ward.geometry))
     return render_to_response("ward.html", { 
      'ward': ward, 'interesting_points': interesting_points }) 
```

Next, we'll build our template. Because we'll be building a map again, we can start with the same template as we use for our map\_page view, so start by copying 'map.html' to 'ward.html' in your lionshead/templates directory.

Now, instead of loading data from the KML view we created earlier, we're going to create features directly in our template. You could also create a second view to serve your data up to be loaded asynchronously (as we did with the KML before): this is just demonstrating another way to achieve the same goal. So, remove the 'kml = new OpenLayers.Layer.GML' line and the line that follows it from the new 'ward.html' template.

Next, you'll be creating a geometry from GeoJSON created in the template.

```
    geojson_format = new OpenLayers.Format.GeoJSON()
    ward = geojson_format.read({{ ward.geometry.geojson|safe}})[0];
    // We mark it 'safe' so that Django doesn't escape the quotes.
 
    ward.attributes = { 'name': "{{ward.name}}", 'type': 'ward'}; 
    vectors = new OpenLayers.Layer.Vector("Data");
    vectors.addFeatures(ward);
```

Next, change the 'kml' in the addLayers call to 'vectors'. Also, we only care about this ward at this time, so we can change the setCenter call to "map.zoomToExtent(ward.geometry.getBounds());" -- This will zoom the map to just the bounds of the ward. Finally, change the {{location\_count}} variable in the text further down the page to simply {{interesting\_points.count}} -- this will issue a `SELECT COUNT(*) FROM` query to the database, giving back a count of the number of matching features.

Now, we should be able to loop over the points in the ward, and add each of them to the map as well. We also want to add them to the HTML page, so we'll do one iteration in the main body of the page, and add features to an array to be parsed in the loading function as we go. Directly above the <div> we'll add the following code:<br>
<br>
<pre><code>    &lt;script&gt; var points = []; &lt;/script&gt;    <br>
     &lt;ul&gt;<br>
     {% for point in interesting_points %}<br>
         &lt;li&gt;{{ point.name }} -- {{point.interestingness}}&lt;/li&gt;<br>
         &lt;script&gt;points.push({{point.geometry.geojson|safe}});&lt;/script&gt;<br>
     {% endfor %}<br>
     &lt;/ul&gt; <br>
</code></pre>

Now, each of your points will be displayed on the map. You can then add code to the initialize function to add them to your vector layer. This should go immediately after the 'vectors.addFeatures' call above.<br>
<br>
<pre><code>    for (var i = 0; i &lt; points.length; i++) {<br>
         point = format.read(points[i])[0]; <br>
         point.attributes = {'type':'point'}; <br>
         vectors.addFeatures(point);<br>
     } <br>
</code></pre>
Now, you can visit your ward page by going to, for example, <a href='http://localhost:8000/wards/96/'>http://localhost:8000/wards/96/</a> . You can compare this to viewing in the admin by visiting <a href='http://localhost:8000/admin/lionshead/ward/96/'>http://localhost:8000/admin/lionshead/ward/96/</a> .<br>
<br>
Now, we can go to <a href='http://localhost:8000/admin/lionshead/interestinglocation/add/'>http://localhost:8000/admin/lionshead/interestinglocation/add/</a>, and scroll to the Southeast of Cape Town. You will see a label that says "Strand". Place a marker in the residential area here, and then visit <a href='http://localhost:8000/wards/96/'>http://localhost:8000/wards/96/</a> again, and you should see a single interesting point listed in this area. Congratulations, you've just combined the data of two different layers in GeoDjango, using a database-backed intersection query.<br>
<br>
<h3>9: MORE GEODJANGO FEATURES</h3>
<pre><code>from django.contrib.gis.geos import  * <br>
from django.contrib.gis.measure import D # D is a shortcut for Distance <br>
from lionshead import InterestingLocation, Ward <br>
from world.models import Countries <br>
<br>
#define a point location <br>
pnt = fromstr('POINT(18.4 -33.9)', srid=4326) <br>
<br>
OUTPUT FORMATS <br>
pnt.geometry.kml <br>
pnt.geometry.geojson <br>
pnt.geometry.gml <br>
<br>
BUFFERING <br>
pnt.buffer(1.5).area <br>
pnt.buffer(1).kml <br>
<br>
<br>
DISTANCE QUERIES <br>
# Distances will be calculated from this point, which does not have to be projected. <br>
# If numeric parameter, units of field (meters in this case) are assumed. <br>
#queryset of all interesting locations within 500 miles, 50km, or 100 chains of this point <br>
qs=InterestingLocation.objects.filter(geometry__distance_lte=(pnt,D(mi=500))) <br>
qs=InterestingLocation.objects.filter(geometry__distance_lte=(pnt,D(km=50)))<br>
qs=InterestingLocation.objects.filter(geometry__distance_lte=(pnt,D(chain=100))) <br>
<br>
<br>
poly = WorldBorders.objects.get(name='Algeria').geometry <br>
for loc in InterestingLocation.objects.distance(poly.centroid): print loc.name, loc.distance.km <br>
<br>
BOUNDING BOX  <br>
qs = Ward.objects.filter(name__in=('foo', 'bar')) <br>
print qs.extent() <br>
</code></pre>


<h3>10: ENTERING DATA FROM THE PUBLIC SITE</h3>

REMOVED<br>
<br>
<br>
<br>
<h3>11: WORKSHOP TROUBLESHOOTING</h3>

It is quite possible workshop attendees will not have internet access.  In this case, the default OpenLayers map settings (which assume they will have access to live WMS or other tile services) will fail.  We can fix this by:<br>
<ul><li>Overriding the default admin map layers, by adding these options to your classes in admin.py:<br>
<pre><code>    wms_url = '/cgi-bin/mapserv?map=/home/user/wms/cape.map&amp;'<br>
    wms_layer = 'countries,wards'<br>
    wms_name = 'Local WMS'<br>
</code></pre>
</li><li>Adding different base WMS layers to the public map view:</li></ul>

<pre><code>var ms_url = '/cgi-bin/mapserv?map=/home/user/wms/cape.map&amp;'<br>
var countries = new OpenLayers.Layer.WMS("Countries",<br>
    ms_url, {layers : 'countries'} );<br>
var wards = new OpenLayers.Layer.WMS("Wards",<br>
    ms_url, {layers : 'wards'} );<br>
<br>
    map.addLayers([countries, wards, kml]);<br>
</code></pre>



<h3>APPENDIX B:     OS X INSTALL</h3>

William Kyngesburye provides a number of geo-related binary packages that can get you most of the way to having Django working and installed without compiling anything from source.<br>
<br>
From <a href='http://www.kyngchaos.com/wiki/software:frameworks'>http://www.kyngchaos.com/wiki/software:frameworks</a> :<br>
<br>
<ul><li>GEOS Framework<br>
</li><li>Proj4 Framework<br>
</li><li>GDAL Framework</li></ul>

From <a href='http://www.kyngchaos.com/wiki/doku.php?id=software:postgres'>http://www.kyngchaos.com/wiki/doku.php?id=software:postgres</a> :<br>
<ul><li>Postgres<br>
</li><li>PostGIS</li></ul>

After you have installed each of these, you'll need the psycopg2 bindings. I could not find a working version of these for OS X, so I did:<br>
<br>
<blockquote>sudo su<br>
PATH="$PATH:/usr/local/pgsql/bin" python easy_install psycopg2</blockquote>

This requires the OS X Developer tools to be installed.<br>
<br>
Then, just download and install Django itself, and you're all set. If you get a complaint about GEOS_LIBRARY_PATH not being set, add the following to your settings file:<br>
<br>
GEOS_LIBRARY_PATH="/Library/Frameworks/GEOS.framework/unix/lib/libgeos_c.dylib"<br>
