import requests
import json

from requests.exceptions import SSLError
from job import Job, View
from helpers import api_url


class Jenkins(object):
    """
    This is the base class of Jenkins. It describes the Jenkins server
    and initializes a connection. It holds information about jenkins jobs,
    view etc.

    If init == True, then initializes everything, jobs, views, details etc.
    Otherwise it just connects to the jenkins server and you have to call
    list_jobs(), list_views() etc manually
    """
    def __init__(self, url, user=None, passdw=None, token=None,
                 verify=True, init=True):
        """

        """
        self.url = url
        self.user = user
        self.passwd = passdw
        self.token = token
        self.verify = verify
        self.connection = self.connect()
        self.details = self.connection.json()
        self.jobs = None
        self.views = None
        if init:
            self.jobs = self.list_jobs()
            self.views = self.list_views()

    def connect(self):
        try:
            ret = requests.get(api_url(self.url),
                               auth=(self.user, self.passwd),
                               verify=self.verify)
            if ret.ok:
                return ret
            elif ret.status_code == 401:
                raise Exception("Invalid Credentials")
        except SSLError:
            print "SSL Verification is on!"
            print "You could pass verify=False in Jenkins initiation."
            raise SSLError

    def list_jobs(self):
        jobs = []
        for job in self.details['jobs']:
            instance = Job(job['name'], job['color'], url=job['url'])
            self.job_details(instance)
            jobs.append(instance)

        self.jobs = jobs
        return jobs

    def list_views(self):
        views = []
        for view in self.details['views']:
            if not view['name'] == "All":
                instance = View(view['name'], view['url'])
                self.view_details(instance)
                views.append(instance)

        self.views = views
        return views

    def job_details(self, job):
        """
        This one takes the a Job object and fills the job.details with all
        the available details
        """
        try:
            details = requests.get(api_url(job.url),
                                   auth=(self.user, self.passwd),
                                   verify=self.verify).json()
            job.details = details
        except Exception as e:
            print e

    def view_details(self, view):
        """
        This one takes a View object. Fill the property, description and job
        values. Furthermore, for every job that belongs to this view, it appends
         the view's name to the Job.views list property
        """
        try:
            details = requests.get(api_url(view.url),
                                   auth=(self.user, self.passwd),
                                   verify=self.verify).json()

            view.description = details['description']
            view.property = details['property']
            view.jobs = details['jobs']
        except:
            pass

__author__ = 'Chris Loukas a.k.a.:commixon, <commixon@gmail.com'
