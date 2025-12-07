

import config
import os
import importlib


def import_plugins_from_directory(directory=None):
    """Import all python modules in this package's directory and register their __help__.

    If `directory` is None, imports modules from the current package directory.
    """
    pkg_name = __name__  # e.g. 'nandha.plugins'
    pkg_dir = os.path.dirname(__file__)
    if directory:
        pkg_dir = directory

    for file in os.listdir(pkg_dir):
        if not file.endswith('.py') or file == '__init__.py':
            continue

        module_name = file[:-3]
        full_name = f"{pkg_name}.{module_name}"
        try:
            module = importlib.import_module(full_name)
        except Exception:
            # keep importing best-effort; plugins should handle their own errors
            continue

        # register module help if present
        if hasattr(module, '__module__') and hasattr(module, '__help__'):
            key = module.__name__.rsplit('.', 1)[-1].lower()
            config.MODULE[key] = module.__help__


# Import plugins automatically when package is imported
import_plugins_from_directory()

