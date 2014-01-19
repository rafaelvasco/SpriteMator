'''
Created on 12/10/2013

@author: Rafael
'''

class ResourcesCache(object):
    
    _resources = {}

    @staticmethod
    def get(name):
        
        return ResourcesCache._resources[name]

    @staticmethod
    def registerResource(name,  resource):
        
        ResourcesCache._resources[name] = resource
        
    @staticmethod
    def dispose():
        
        ResourcesCache._resources.clear()