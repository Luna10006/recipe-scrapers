# mypy: disallow_untyped_defs=False
import re
from typing import Optional, Union

from ._abstract import AbstractScraper
from ._schemaorg import SchemaOrg
from ._utils import normalize_string


class FOKSchema(SchemaOrg):
    def category(self):
        cat = super().category()
        r = re.compile('.*<a href=".+">(.+)</a>')
        m = r.match(cat)
        if m:
            return normalize_string(m[1])
        return cat


class ForksOverKnives(AbstractScraper):
    @classmethod
    def host(cls):
        return "forksoverknives.com"

    def __init__(
        self,
        html: Union[str, bytes],
        url: Union[str, None],
        wild_mode: Optional[bool] = False,
    ):
        super().__init__(url=url, wild_mode=wild_mode, html=html)
        self.schema = FOKSchema(self.page_data)

    def author(self):
        author = self.soup.find("div", attrs={"class": "post-info"}).find("a")
        return normalize_string(author.get_text())

    def title(self):
        return self.schema.title()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        yields = normalize_string(
            self.soup.find("i", attrs={"class": "icon-serving"}).next_sibling.get_text()
        )
        # Get the first string after "Makes".
        return yields.split(" ", 1)[1]

    def image(self):
        return self.schema.image()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        return self.schema.instructions()

    def ratings(self):
        ratings = normalize_string(
            self.soup.find("div", attrs={"class": "headline"})
            .find("span", attrs={"class": "rated-count"})
            .get_text()
        )
        # Unwrap parens
        ratings = ratings[1:]
        # return the first element
        return float(ratings.split()[0])

    def category(self):
        return self.schema.category()
