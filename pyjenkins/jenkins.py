import requests
import json

from requests.exceptions import SSLError
from jobs import Job, View
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
    def __init__(self, url, user=None, passwd=None, token=None,
                 verify=True, init=True):
        """
        :param url: The Jenkins url
        :param user: If authentication is needed, the user used for the
        connection
        :param passwd: If authentication is needed, the password for the user
        :param token: If csrf token, or any other token is to be used for
        extra security
        :param verify: If there is a https url and the certificate cannot be
        verified, by default requests will raise an SSL_ERROR. However, by
        passing verify=False we bypass the certificate verification. USE WITH
        CARE
        :param init: By default init is True. This means that every time you
        initiate a Jenkins object it will try and populate everything by the
        initialization (e.g. jobs, views, details etc). However this takes some
        time. You could pass init=False and call self.list_jobs() explicitly
        when you want for example to init the jobs param.
        """
        self.url = url
        self.auth = (user, passwd)
        self.user = user
        self.passwd = passwd
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
        """
        The initial connect to the jenkins servers

        :returns ret: The response of the connection made
        """
        try:
            ret = requests.get(api_url(self.url),
                               auth=self.auth,
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
        """
        For each job found in the details dict, a new Job object is initialized
        and added to the self.jobs list.

        :returns jobs: List of Job objects
        """
        jobs = []
        for job in self.details['jobs']:
            instance = Job(job['name'], job['color'], url=self.url,
                           auth=self.auth, verify=self.verify)
            jobs.append(instance)

        self.jobs = jobs
        return jobs

    def list_views(self):
        """
        For each view found in the details dict, a new View object is
        initialized and added to the self.views list.

        :returns views: List of View objects
        """
        views = []
        for view in self.details['views']:
            #All is a dummy view returned by the API. It actually contains all
            #the available jobs and thus we do not need it
            if "All" != view['name']:
                instance = View(view['name'], url=self.url, auth=self.auth,
                                verify=self.verify)
                views.append(instance)

        self.views = views
        return views

    def start_job(self, job, params={}):
        job.build(params)

__author__ = 'Chris Loukas a.k.a.:commixon, <commixon@gmail.com'
