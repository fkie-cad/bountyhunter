from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        for match in self.line(blob):
            path = self._locate_path(match)
            if path:
                for mp in self.mappers:
                    source = self.set_value(mp.source, path, self.used_facts)
                    target = self.set_value(mp.target, path, self.used_facts)
                    relationships.append(
                        Relationship(source=Fact(mp.source, source),
                                     edge=mp.edge,
                                     target=Fact(mp.target, target))
                    )
                    
        return relationships

    @staticmethod
    def _locate_path(line):
        try:
            # scp output differs between different hosts/versions(?)
            # Kali
            if "scp: debug2: do_upload: upload local" in line:
                return line.split("to remote")[1].replace('"', "").strip()
            # Ubuntu 22.04
            elif "debug1: Sending command: scp -v -t" in line:
                return line.split("-t ")[1]
        except Exception:
            pass
        return None
