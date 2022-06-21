from abc import ABC, abstractmethod, abstractproperty
import sys, os
from pathlib import Path
import inspect
import importlib
from importlib import util
from ast import ClassDef, parse, ImportFrom

sys.path.append(os.path.join(os.getcwd(), "python", "plugins"))
sys.path.append(os.path.join(os.getcwd(), "python", "houtils"))
sys.path.append(os.path.join(os.getcwd(), "python", "pyplug"))

class Factory():

    def __init__(self, name="", version="", env_vars="", base_class=None, paths=[]):
        #store params
        self.paths = paths
        for path in self.paths:
            sys.path.append(path)

        self.base_class = base_class
        self.version = version
        self.env_vars = env_vars
        self.name = name
        
        """
        loop through all of the paths provided and return plugins which contain implementations of the base class
        """
        self.plugins = []
        self.refresh(paths=self.paths, base_class=self.base_class)

    def get(self, plugin_name, refresh=False):
        """
        Return a specific plugin based on a name. 
        """
        return self.plugins[self.plugins.index(plugin_name)]

    def available(self):
        """
        Return list of available plugins.
        """
        
        return self.plugins

    def get_paths(self):
        """
        Return directories this factory will index.
        """
        return self.paths
    
    def refresh(self, paths, base_class):
        """
        This function loops through paths.
        For each, parse the file and get a list of defined classes.
        
        Compare the base class parameter to see if the abstract 
        is defined in the module.

        If it is, add it to the list of available plugins. 
        """
        for p in paths:
            for root, dirs, files in os.walk(p, topdown=False):
                #ignore pycache folder
                if os.path.basename(os.path.normpath(root)) != "__pycache__":
                    for name in files:
                        
                        if name.endswith(".py") and name != "__init__.py":
                            full_file = os.path.join(root, name)
                            #remove .py from file name
                            file_name = name[:-3]
        
                            #generate module import name
                            module_name = os.path.basename(os.path.normpath(root))
                            module_name = module_name+"."+file_name


                            try:
                                #parse module
                                mod = importlib.import_module(module_name)
                                src = inspect.getsource(mod)
                                p=parse(inspect.getsource(mod))

                                #get list of class names defined in the module
                                names = []    
                                for node in p.body:
                                    if isinstance(node, ClassDef):
                                        names.append(node.name)
                                    elif isinstance(node, ImportFrom):
                                        names.extend(imp.name for imp in node.names)

                                    if base_class in names:
                                        self.register(mod)
                            except Exception as e:
                                print("Could not parse module: ", module_name, e)

    def register(self, plug_in):
        """
        Add a plug in to the list of available plugins.

        Quick check to ensure no duplication. 
        """
        if plug_in not in self.plugins:
            self.plugins.append(plug_in)
