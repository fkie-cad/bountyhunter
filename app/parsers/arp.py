import ipaddress

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            ip = self._locate_ip(match)
            if ip:
                for mp in self.mappers:
                    source = self.set_value(mp.source, ip, self.used_facts)
                    target = self.set_value(mp.target, ip, self.used_facts)
                    relationships.append(
                        Relationship(source=Fact(mp.source, source),
                                     edge=mp.edge,
                                     target=Fact(mp.target, target))
                    )
                    
        return relationships

    @staticmethod
    def _locate_ip(line):
        try:
            ip = line.split()[0]
            ipaddress.IPv4Address(ip)
            return ip
        except Exception:
            pass
        return None
