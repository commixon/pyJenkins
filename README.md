pyJenkins
=========

pyJenkins consists of some simple python bindings for the Jenkins' API. It
uses the requests module to send POST and GET requests to your Jenkins server
and parse the json objects of the response.

USE
---

It is rather simple to use pyJenkins::

    from JenkinsPy.jenkins import Jenkins
    jenkins = Jenkins(url, username, passwd, verify, init)

:param url: This is self-explanatory, the url of your jenkins server

:param username: Username

:param passwd: Password

:param verify: By default True. If you have a https url with no confirmed certificate, then this
should be passed in as False

:param init: By default True. If True, then it will initialize jobs, views and
all their details. If False, then you have to call list_jobs() and list_views()
methods explicitly

After initialization you'll have jobs and views as objects in your jenkins object.
