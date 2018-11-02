"""
    exports an intercept() method, which modifies response body
    by processing it through a chain of interceptor classes
    These are things which contain modification settings/rules.
    Every Interceptor must:
    - have process() method - this will be invoked by the service.
      See intercept() docstring for details
    - encapsulate all criterias and data how to modify the response body
"""
from bs4 import BeautifulSoup, NavigableString, Comment
from .utils import multi_insert


class TMInterceptor:
    """
        Takes response body and appends tm_ sign to every word of char_count letters.
        Other settings via __init__():
        - special: word delimiters, see .utils multi_insert() description
        - ignored_tags: where multi_insert() must not look for words
    """
    def __init__(self):
        # interceptor configuration
        self.tm_ = b'\xE2\x84\xA2'.decode()
        self.special = '"()- !.,?[]{}_\n\r\t:;'
        self.char_count = 6
        self.ignored_tags = ['script', 'code']

    def process(self, soup_dom: BeautifulSoup):
        """
            WARNING! MUTATES soup_dom and return it mutated
            Focuses on pure content processing:
            - finds all leafs with pure text inside <body> tag
            - replaces that text with multi_insert processor output
        """
        nav_strings = filter(
            lambda x:
            isinstance(x, NavigableString)
            and x.parent.name not in self.ignored_tags
            and x.strip() != ''
            and not isinstance(x, Comment),
            soup_dom.html.body.descendants
        )
        for ns_ in list(nav_strings):
            ns_.replace_with(multi_insert(ns_, self.tm_, self.char_count, self.special))
        return soup_dom


INTERCEPTORS = [TMInterceptor()]


def intercept(response):
    if INTERCEPTORS:
        soup_dom = BeautifulSoup(response.content.decode('utf-8'), 'html5lib')
        list(map(lambda x: x.process(soup_dom), INTERCEPTORS))
        response.content = soup_dom.encode()
