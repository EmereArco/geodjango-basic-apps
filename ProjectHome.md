![http://geodjango.org/images/geodjango.png](http://geodjango.org/images/geodjango.png)

### GeoDjango Basic Apps ###
Quickstart samples highlighting basic GeoDjango integration with existing contrib apps (**GeographicAdmin**), utilities of GeoDjango (**GeoIP**), and (to come) fully pluggable geoapps.

These projects aim to be a useful starting point for both experienced Django programmers who are new to GIS (Geographical Information Systems), as well as those with some background in mapping but who learn best through tangible examples.

All code has been developed on Django 1.0 release/trunk.

### Overview ###
Stats from Ohloh:

|&lt;wiki:gadget url="http://www.ohloh.net/p/16385/widgets/project\_languages.xml" border="0" height="220" width="320"/&gt; |&lt;wiki:gadget url="http://www.ohloh.net/p/16385/widgets/project\_factoids.xml" border="0" height="220" width="320"/&gt;|
|:--------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------|

### Downloads ###

**GeographicAdmin**  - A sample project that highlights the Django Admin and Databrowse with GeoDjango spatial features (embedded OpenLayers maps) is [available](http://code.google.com/p/geodjango-basic-apps/source/browse/trunk/projects/geographic_admin), with installations instructions at GeographicAdminQuickStart. This project includes sample data.

**GeoIP** - A sample project that utilizes the GeoDjango wrapper around the GeoIP python library, used for mapping IP addresses is [available](http://code.google.com/p/geodjango-basic-apps/source/browse/trunk/projects/geographic_admin), with installations instructions at [GeoIPQuickStart](http://code.google.com/p/geodjango-basic-apps/wiki/GeoIPQuickStart).


For further offerings look in [SVN Trunk](http://code.google.com/p/geodjango-basic-apps/source/browse/trunk/) to see what is available. No bundled releases are planned at this time.

  * Note, SVN Trunk is organized by `Projects` and `Apps`. Projects hold full Django projects with a settings.py and the manage.py command. Projects are meant to be downloaded to your location of choice and run immediately using the development server and with minimal setup. The `Apps` directory is designed to hold pluggable geoapps meant to be installed anywhere on your PYTHONPATH, similar to an app like [django-registration](http://code.google.com/p/django-registration/).


---


World Borders dataset within GeoDjango Admin site utilizing newforms-admin branch (now merged into Django trunk):

![http://geodjango-basic-apps.googlecode.com/svn/images/geodjango_admin.png](http://geodjango-basic-apps.googlecode.com/svn/images/geodjango_admin.png)


---


OpenLayers map embedded inside Django Databrowse contrib app which reads the Well Known Text(WKT) from the GeoDjango `geometry` field and can convert to other representations such as GeoJson, KML, GML and projections such as Google Mercator (EPSG:900913):

![http://geodjango-basic-apps.googlecode.com/svn/images/geo_databrowse.png](http://geodjango-basic-apps.googlecode.com/svn/images/geo_databrowse.png)