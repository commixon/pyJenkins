import requests
import json


class Jenkins(object):
    """

    """
    def __init__(self, host, user=None, passdw=None, token=None):
        self.host = host
        self.user = user
        self.passwd = passdw
        self.token = token
        self.connection = self.connect()

    def connect(self):
        ret = requests.get(self.host+"/api/json", auth=(self.user, self.passwd))
        if ret.ok:
            return ret
        else:
            print "No connection"

    def list_responses(self):
        print self.connection.json()

__author__ = 'Chris Loukas a.k.a.:commixon, <commixon@gmail.com'
