import os
from fuchs.parser import FuchsParser

class FuchsTemplate:
    def __init__(self, dirname: str = None) -> None:
        self.parser = FuchsParser()
        if os.path.exists(dirname):
            self.dirname = dirname
        else:
            raise FileNotFoundError(f"Directory {dirname} does not exist")

    def render(self, filename: str, **kwargs) -> str:
        with open(os.path.join(self.dirname, filename)) as f:
            template = f.read()
        template = self.parser.feed(template, **kwargs)
        return template
        