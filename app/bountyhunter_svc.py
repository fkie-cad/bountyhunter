from aiohttp_jinja2 import template

from app.utility.base_service import BaseService


class BountyHunterService(BaseService):
    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.file_svc = services.get('file_svc')
        self.data_svc = services.get('data_svc')
        self.contact_svc = services.get('contact_svc')
        self.log = self.add_service('bountyhunter_svc', self)

    @template('bountyhunter.html')
    async def splash(self, request):
        abilities = [a for a in await self.data_svc.locate('abilities') if await a.which_plugin() == 'bountyhunter']
        adversaries = [a for a in await self.data_svc.locate('adversaries') if await a.which_plugin() == 'bountyhunter']
        return dict(abilities=abilities, adversaries=adversaries)
        return dict()
