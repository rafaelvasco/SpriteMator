#--------------------------------------------------------------------------------------------------
# Name:        Resources Cache
# Purpose:     Manages application resources;
#
# Author:      Rafael Vasco
#
# Created:     12/10/13
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#--------------------------------------------------------------------------------------------------


class ResourcesCache(object):
    
    _resources = {}

    @staticmethod
    def get(name):
        
        return ResourcesCache._resources[name]

    @staticmethod
    def register_resource(name,  resource):
        
        ResourcesCache._resources[name] = resource
        
    @staticmethod
    def dispose():
        
        ResourcesCache._resources.clear()