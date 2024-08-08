from plugins.bountyhunter.app.bountyhunter_svc import BountyHunterService

name = 'BountyHunter'
description = 'A plugin for complete attack scenarios for Caldera.'
address = '/plugin/bountyhunter/gui'


async def enable(services):
    bountyhunter_svc = BountyHunterService(services)
    services.get('app_svc').application.router.add_route('GET', '/plugin/bountyhunter/gui', bountyhunter_svc.splash)
