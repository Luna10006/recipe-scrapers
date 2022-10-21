# mypy: allow-untyped-defs

from ._abstract import AbstractScraper
from ._decorators import opengraph_fallback


class ACoupleCooks(AbstractScraper):
    @classmethod
    def host(cls):
        return "acouplecooks.com"

    def title(self):
        return self.schema.title()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    @opengraph_fallback
    def image(self):
        return self.schema.image()

    def instructions(self):
        return self.schema.instructions()

    def ingredients(self):
        return self.schema.ingredients()
