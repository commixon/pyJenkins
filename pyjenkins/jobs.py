import requests
from helpers import api_url


class Job(object):
    """
    Class describing a Job
    """
    def __init__(self, name, color, url, views=[], auth=None, verify=True):
        """
        Here happens the main initialization of the Job class.

        :param name: Name of the job
        :param color: Color matches the state of the job (e.g. blue is ok, red
        is broken etc)
        :param url: The url of Jenkins. We could take the job['url'] but this
        :param views:  View in which the job belonds (e.g. All, Custom)
        :param auth: Auth is a tuple of (username, password). It is used in the
        requests for authentication. This is passed on by the Jenkins class
        initialization and normally you should not worry about this.
        :param verify: Verify, as the auth param is passed on by the Jenkins
        Class initialization.

        """
        self.name = name
        self.color = color
        self.url = url+"/job/"+name
        self.views = views
        self.details = None
        self.auth = auth
        self.verify = verify
        self.params = {}

        self.populate_details()
        self.populate_params()

    def populate_details(self):
        """
        To get details of each job you have to make a GET request to the
        jobs url. This returns a huge json dict with all available details
        for the jobs

        :returns: details dict for the job
        """
        try:
            details = requests.get(api_url(self.url),
                                   auth=self.auth,
                                   verify=self.verify).json()
            self.details = details
            return self.details
        except Exception as e:
            print e

    def populate_params(self):
        """
        If this is a parametrized job, then self.params dict will
        hold all the information. We populate it in an ugly way, as
        the response in a dict, of a list of dicts with lists etc...

        'actions' is actually a list of dicts. The way to check if a
        job is parametrized or not is to check if the list is empty.

        That is what we do here...

        :returns: params
        """
        if self.details['actions']:
            actions = self.details['actions']
        else:
            return

        #ugly as fuck, but the ugly json responses request ugly loops :)
        for action in actions:
            if "parameterDefinitions" in action.keys():
                params = action['parameterDefinitions']
                for param in params:
                    name = param['name']
                    description = param['description']
                    kind = param['type']
                    default = param['defaultParameterValue']['value']
                    self.params[name] = {
                        'name': name,
                        'description': description,
                        'type': kind,
                        'default': default
                    }

        return self.params

    def build(self, payload=None):
        """
        Build a job without parameters. Just a post request to /build

        :returns: The status_code of the POST request
        """
        try:
            ret = requests.post(self.url+"/build", auth=self.auth,
                                verify=self.verify)

            print ret.status_code
        except Exception as e:
            print e

    def build_parametrized(self, payload=None):
        """
        Build a parametrized job. If no payload is given, then the default
        values are used.

        :returns: The status_code of the POST request
        """
        try:
            if not payload:
                payload = {}
                for param in self.params.keys():
                    payload['param'] = self.params[param]['default']

            ret = requests.post(self.url+"/buildWithParameters",
                                auth=self.auth, verify=self.verify,
                                data=payload)

            print ret.status_code
        except Exception as e:
            print e


class View(object):
    """
    Describes a view
    """
    def __init__(self, name, url, description=None, auth=None,
                 verify=None):
        self.name = name
        #this is an ugly hack, most of the times it is not needed, but if you
        #have an https connection, then Jenkins returns http instead of https
        self.url = url+"/view/"+name
        self.jobs = []
        self.description = description
        self.auth = auth
        self.verify = verify
        self.details = None

        self.populate_details()
        self.list_jobs()

    def populate_details(self):
        try:
            details = requests.get(api_url(self.url),
                                   auth=self.auth,
                                   verify=self.verify).json()
            self.details = details
            return self.details
        except Exception as e:
            print e

    def list_jobs(self):
        for job in self.details['jobs']:
            self.jobs.append(job)

        return self.jobs

__author__ = 'Chris Loukas a.k.a.:commixon, <commixon@gmail.com'
