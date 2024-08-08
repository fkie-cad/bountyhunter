from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):
    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            port = self._get_port(match)
            os = self._get_os(match)

            for mp in self.mappers:
                if port and mp.target == "host.ports.open":
                    source = self.set_value(mp.source, port, self.used_facts)
                    target = self.set_value(mp.target, port, self.used_facts)
                    relationships.append(
                        Relationship(source=Fact(mp.source, source),
                                     edge=mp.edge,
                                     target=Fact(mp.target, target))
                    )
                elif os and mp.target == "host.os":
                    source = self.set_value(mp.source, os, self.used_facts)
                    target = self.set_value(mp.target, os, self.used_facts)
                    relationships.append(
                        Relationship(source=Fact(mp.source, source),
                                     edge=mp.edge,
                                     target=Fact(mp.target, target))
                    )

        return relationships

    @staticmethod
    def _get_port(line):
        try:
            if "open" in line:
                port = line.split()[0].split('/')[0]
                service_info = line.split(None, 3)[2]
                version_info = line.split(None, 3)[3]
                return port + '/' + service_info + '/' + version_info
        except Exception:
            pass
        return None

    @staticmethod
    def _get_os(line):
        try:
            if "Service Info: " in line:
                if "Windows" in line:
                    return "Windows"
                elif "Linux" in line:
                    return "Linux"
        except Exception:
            pass
        return None
