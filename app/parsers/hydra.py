from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        
        for match in self.line(blob):
            user, pwd = self._locate_creds(match)
            
            if user: 
                for mp in self.mappers:
                    # In case the SSH user is being parsed, create a new relationship between the user fact and the existing IP address
                    if mp.target=="host.ssh.user":
                        source = self.set_value(mp.source, user, self.used_facts)
                        target = self.set_value(mp.target, user, self.used_facts)
                        relationships.append(
                            Relationship(source=Fact(mp.source, source),
                                         edge=mp.edge,
                                         target=Fact(mp.target, target))
                        )
                    
                    # In case the SSH password is being parsed, create a new relationship between the password fact and the corresponding user
                    elif mp.target=="host.ssh.pwd":
                        source = self.set_value(mp.source, user, self.used_facts)
                        target = self.set_value(mp.target, pwd, self.used_facts)
                        relationships.append(
                            Relationship(source=Fact(mp.source, source),
                                         edge=mp.edge,
                                         target=Fact(mp.target, target))
                        )
                    
        return relationships

    @staticmethod
    def _locate_creds(line):
        try:
            line_split = line.split()
        
            if line_split[3] == "login:" and line_split[5] == "password:":
                user, password = line_split[4], line_split[6]   
            return user, password               
        except Exception:
            pass
        return None, None
