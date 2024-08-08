import re

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser


class Parser(BaseParser):

    def parse(self, blob):
        relationships = []
        
        for match in self.line(blob):
            cleartext_passwords = self._get_passwords(match)
        
            for cleartext_password in cleartext_passwords:
                for mp in self.mappers:
                    source = self.set_value(mp.source, cleartext_password, self.used_facts)
                    target = self.set_value(mp.target, cleartext_password, self.used_facts)
                    relationships.append(
                        Relationship(source=Fact(mp.source, source),
                                     edge=mp.edge,
                                     target=Fact(mp.target, target))
                    )
                
        return relationships

    @staticmethod
    def _get_passwords(line):
        password_list=set()
    
        if "* Password :" in line:
            pattern = re.compile(r"\s*\* Password : ")
            split_results = pattern.split(line)
            
            for split_result in split_results:
                if split_result and not split_result == "(null)":
                    password_list.add(split_result)
            
        return password_list
            
