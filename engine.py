class Engine(object):
    """Experiment Engine"""

    def __init__(self):
        self.lib = Library()

    def load_dependencies(self, dependencies):
        for dep in dependencies:
            self.lib.import_module(dep)

class Library(object):
    """Library"""
    def import_module(self, module_name):
        if module_name not in self.__dict__:
            setattr(self, module_name, __import__(module_name))

def main():
    # Load Experiment File

    # Initialize any libraries before
    pass

