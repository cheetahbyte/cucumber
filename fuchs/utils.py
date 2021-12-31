class Document:
    """class, to make dict available in the template"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)



def url_for(base_url: str, path: str) -> str:
    """Returns the url for the given filename"""
    middle = ""
    if not path.startswith("/"):
        middle = "/"
    return f"{base_url}"+ middle +f"{path}"

