from aiohttp_jinja2 import template

from app.utility.base_service import BaseService
from app.objects.c_adversary import Adversary


import json
from aiohttp import web
import os
import asyncio

class BountyHunterService(BaseService):
    def __init__(self, services):
        self.auth_svc = services.get("auth_svc")
        self.file_svc = services.get("file_svc")
        self.data_svc = services.get("data_svc")
        self.contact_svc = services.get("contact_svc")
        self.log = self.add_service("bountyhunter_svc", self)

    async def create_or_update_everything_adversary(self):
        abilities = [
            a
            for a in await self.data_svc.locate("abilities")
            if await a.which_plugin() == "bountyhunter"
        ]

        everything = {
            'id': '491e94b1-cd73-437b-aa9e-70eccb467d7d',
            'name': 'Everything BountyHunter',
            'description': 'An adversary with all adversary abilities from the BountyHunter plugin',
            'atomic_ordering': [
                ability.ability_id
                for ability in abilities
            ],
        }
        obj = Adversary.load(everything)
        obj.access = self.data_svc.Access.RED
        await self.data_svc.store(obj)

    @template("bountyhunter.html")
    async def splash(self, request):
        abilities = [
            a
            for a in await self.data_svc.locate("abilities")
            if await a.which_plugin() == "bountyhunter"
        ]
        adversaries = [
            a
            for a in await self.data_svc.locate("adversaries")
            if await a.which_plugin() == "bountyhunter"
        ]

        return dict(abilities=abilities, adversaries=adversaries)

    async def scenarios(self, request):
        """
        Queries all files in the `conf` directory of bountyhunter
        and returns all scenarios (directories) as an array
        """
        scenarios = []
        try:
            scenarios = os.listdir("plugins/bountyhunter/conf")
            scenarios.sort()
            scenarios.remove("agenda_mapping.json")
        except:
            pass

        return web.json_response(scenarios)

    async def mirror(self, request):
        """
        This sample endpoint mirrors the request body in its response
        """
        request_body = json.loads(await request.read())
        return web.json_response(request_body)
