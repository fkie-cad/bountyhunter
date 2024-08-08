from re import compile

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            host = self._get_host(match)
            if host:
                for mp in self.mappers:
                    source = self.set_value(mp.source, host, self.used_facts)
                    target = self.set_value(mp.target, host, self.used_facts)
                    relationships.append(
                        Relationship(source=Fact(mp.source, source),
                                     edge=mp.edge,
                                     target=Fact(mp.target, target))
                    )

        return relationships

    @staticmethod
    def _get_host(line):
        pattern = compile("Nmap scan report for (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

        try:
            if 'Nmap scan report for' in line:
                return pattern.match(line).group(1)
        except Exception:
            pass
        return None
