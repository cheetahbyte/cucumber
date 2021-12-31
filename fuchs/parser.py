from fuchs.cache import Cache, Counter
import typing
import re
from fuchs.utils import url_for
from fuchs.utils import Document

class FuchsParser:
    """Class for evaluating and analyzing the HTML code"""
    def __init__(self) -> None:
        self.cache: Cache = Cache()
        self.counter: Counter = Counter()

    def feed(self, content: str, **kwargs) -> None:
        """Feed the hungry fox"""
        # load vars to cache
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.cache.store(key, Document(**value))
                continue
            self.cache.store(key, value)
        # parse lazy fox tags
        lazy_fox = r"<\?fuchs(.*?)\?>"
        tags = re.finditer(lazy_fox, content, re.DOTALL | re.IGNORECASE)
        lazy_fox_tags: typing.List[re.Match] = [m for m in tags]
        for tag in lazy_fox_tags:
            self.LazyFoxParser.parse(tag, self)
        # remove all lazy fox tags
        content = re.sub(lazy_fox, "", content, flags=re.DOTALL | re.IGNORECASE)
        # parse inline tags
        inline_fox = r"(<[ |\n]*.*fuchs:(\w+)=\"(.*)\"[ |\n]*>)(.*)(</\w+>)"
        tags = re.finditer(inline_fox, content, re.MULTILINE)
        inline_fox_tags: typing.List[re.Match] = [m for m in tags]
        for tag in inline_fox_tags:
            evaluated, tag = self.InlineFoxParser.parse(tag, self)
            if evaluated is not True:
                content = content.replace(tag, "")
            else:
                pass
        # parse variables
        variables_regex = r"{{([ |\n]*.*[ |\n]*)}}"
        variables = re.finditer(variables_regex, content, re.MULTILINE)
        variables_tags: typing.List[re.Match] = [m for m in variables]
        for tag in variables_tags:
            var = self.VariableFoxParser.parse(tag, self)
            # replace variable tag with variable value
            if isinstance(var, dict):
                var = Document(**var)
            content = content.replace(tag.group(0), str(var))
        return "\n".join([ p for p in content.split("\n")])

    class LazyFoxParser:
        """class, to parse the lazy_fox tags in the HTML code"""
        @staticmethod
        def parse(tag: re.Match, cls: "FuchsParser") -> None:
            """Extracts the Python code from the tag"""
            # remove pre- and suffix
            tag: str = tag.groups()[0]
            if "\n" in tag:
                local_tag = [t for t in tag.split("\n") if t != "" and t.isspace() is False][0]
                while local_tag.startswith(" "):
                    cls.counter.incr()
                    local_tag = local_tag[1:]
                local_tag = ""
                for t in tag.split("\n"):
                    if t.isspace() is True:
                        continue
                    l_count = 0
                    while t.startswith(" ") and l_count < cls.counter.data["count"]:
                        l_count += 1
                        t = t[1:]
                    local_tag += t + "\n"
                # is multiline
                exec(local_tag, globals(), cls.cache.data)
                # filter all vars create while executing expression
                local_vars = [(k, v) for k, v in locals().items() if k != "tag" and k != "expr" and k != "local_tag"]
                # return if local_vars not exists
                if not local_vars:
                    return
                for k,v in local_vars:
                    cls.cache.store(k, v)

            else:
                for expr in tag:
                    exec(tag, globals(), cls.cache.data)
                    # filter all vars create while executing expression
                    local_vars = [(k, v) for k, v in locals().items() if k != "tag" and k != "expr"]
                    # return if local_vars not exists
                    if not local_vars:
                        return
                    for k,v in local_vars:
                        cls.cache.store(k, v)

    class InlineFoxParser:
        """class to parse all inline fox tags"""
        @staticmethod
        def parse(tag: re.Match, cls: "FuchsParser") -> typing.Union[typing.Tuple[bool, str], str]:
            """Executes the logic inside the inline Fox statement"""
            start_tag, statement, expression, tag_content, end_tag = tag.groups()
            if statement == "if":
                val: bool = eval(expression, globals(), cls.cache.data)
                return val, "".join([start_tag, tag_content, end_tag])
            if statement == "content":
                return tag

    class VariableFoxParser:
        """class to replace variables"""
        @staticmethod
        def parse(tag: re.Match, cls: "FuchsParser") -> typing.Union[int, str, dict]:
            """Replaces the variable with the value from the cache"""
            variable = tag.groups()[0]
            val = eval(variable, globals(), cls.cache.data)
            return val