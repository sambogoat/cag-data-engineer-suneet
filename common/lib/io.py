import os

def abspath(path: str) -> str:
    """Return the path as an absolute path"""    
    if not os.path.isabs(path):
        return os.path.join(root_dir(), path)
    else:
        return path

