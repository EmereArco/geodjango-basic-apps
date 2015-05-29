# GeoIP #
Steps to setup and configure the GeoIP project

This [Download](http://code.google.com/p/geodjango-basic-apps/source/browse/trunk/projects/geoip) provides a sample project called 'geoip' with an application called 'whereami'.

It it designed to highlight the mapping of users based on an external IP address using the [GeoIP](http://www.maxmind.com/) library, and an integrated convenience utility from within GeoDjango.


---

The default url of the GeoIP app:

![http://geodjango-basic-apps.googlecode.com/svn/images/geoip_whereami.png](http://geodjango-basic-apps.googlecode.com/svn/images/geoip_whereami.png)

---

### Dependencies for GeoIP Project ###

  * GeoIP C libary and python bindings
  * Note, **no database is needed** for this app and there is no models.py file
    * Therefore, **do not** put `django.contrib.gis` in your INSTALLED\_APPS

## Steps to run the GeoIP project ##

### Step 1 ###
Install the GeoIP C library and python api: http://www.maxmind.com/app/python

```
$ wget http://www.maxmind.com/download/geoip/api/c/GeoIP-1.4.4.tar.gz
$ tar xvf GeoIP-1.4.4.tar.gz
$ cd GeoIP-1.4.4
$ ./configure
$ make
$ sudo make install
```

**Note:** the GeoIP lib needs zlib.h, so you may need to `sudo apt-get install zlibc zlib1g-dev libssl-dev`

```
$ wget http://www.maxmind.com/download/geoip/api/python/GeoIP-Python-1.2.2.tar.gz
$ tar xvf GeoIP-Python-1.2.2.tar.gz
$ cd GeoIP-Python-1.2.2
$ python setup.py install

# if on linux, run:
$ ldconfig # and confirm that 'usr/local/lib' is in /etc/ld.so.conf
```

### Step 2 ###
Download Maxmind GeoLiteCity.dat: http://www.maxmind.com/download/geoip/database/

```
$ wget http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
$ gzip -d GeoLiteCity.dat.gz
```

### Step 3 ###
Extract or copy the .dat file to the `data` dir and confirm that the GEOIP\_LOCATION in settings.py points to this directory (absolute or relative).

### Step 4 ###
```
python manage.py runserver
```

### Step 5 ###
To run remotely you'll need to sign up for a free Google Maps API key and use it to fill in the value for the GOOGLE\_MAPS\_API\_KEY setting in settings.py.