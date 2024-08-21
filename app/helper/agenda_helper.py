from json import load


class Agenda:
    def __init__(self, name, ability_ids, requirements):
        self.name = name
        self.ability_ids = ability_ids
        self.requirements = []
        self._load_requirements(requirements)

    def _load_requirements(self, requirement_list):
        for req_name in requirement_list:
            self.requirements.append(
                Requirement(req_name, requirement_list[req_name])
            )

    def has_unfulfilled_requirements(self, port, service, info):
        has_unfulfilled_requirements = False

        for req in self.requirements:
            if not req.is_met(port, service, info):
                has_unfulfilled_requirements = True
                break

        return has_unfulfilled_requirements


class Requirement:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def is_met(self, port, service, info):
        if self.name == "port":
            return self.value == port
        elif self.name == "service":
            return self.value == service
        elif self.name == "info":
            return self.value == info


class AgendaHelper:
    def __init__(self, mapping_path="plugins/bountyhunter/conf/agenda_mapping.json"):
        self._mapping_path = mapping_path
        self.agendas = []
        self.valid_agendas = []

        self._load_agendas_from_mapping()

    def _load_agendas_from_mapping(self):
        agenda_mapping = _read_json_from_file(self._mapping_path)

        for agenda in agenda_mapping["agendas"]:
            self.agendas.append(Agenda(
                agenda["name"],
                agenda["ability_ids"],
                agenda["requirements"]
            ))

    async def get_valid_agendas(self, ability_links):
        for link in ability_links:
            for fact in link.facts:
                try:
                    port, service, info = fact.value.split("/", 2)

                    for agenda in self.agendas:
                        if not agenda.has_unfulfilled_requirements(port, service, info):
                            await self._add_agenda(agenda)
                except ValueError:
                    pass

        return self.valid_agendas

    async def _add_agenda(self, new_agenda):
        for agenda in self.valid_agendas:
            if agenda.name == new_agenda.name:
                return

        self.valid_agendas.append(new_agenda)


def _read_json_from_file(path):
    with open(path, "r") as f:
        data = load(f)

    return data
