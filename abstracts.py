from abc import ABC, abstractmethod

class Exporter(ABC):
    """
    Abstract class defining our exporter plugin. 
    This will serve as the template for exporting all manner of content from houdini.
    PyPlug will index all of our plugins and look for implementations of this exporter.
    """
    @classmethod
    @abstractmethod
    def viable(self, **kwargs):
        """
        Test for anythin in the scene/content which the plugin can extract.
        
        :param context: If None, all nodes will be searched, 
        otherwise only nodes connected to the context node will be searched. 
        nodes under

        :return: True if anything viable is found
        """
        pass
    @classmethod
    @abstractmethod
    def export(self, directory, **kwargs):
        """
        This will export data to external files.
        :param directory: Location on disk to save data
        :param kwargs: optional keyword data

        :return: List of exported files
        """
        pass

class Importer(ABC):
    def __init__(self):
        pass
    
    @classmethod
    @abstractmethod
    def viable(self, **kwargs):
        pass
    
    @classmethod
    @abstractmethod
    def import_asset(self, **kwargs):
        pass
class UI(ABC):
    @abstractmethod
    def viable(self, **kwargs):
        pass

    @abstractmethod
    def build_ui(self, **kwargs):
        pass
    
    @abstractmethod
    def bind_functions(self, **kwargs):
        pass
    
    @abstractmethod
    def get_ui(self):
        pass
