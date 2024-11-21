
from random import randint
from .api import Api
from .tiktok import TikTok

from .helpers.device import Device


class Flow:
    """ Pre-made flow for actions like in real app

    # usage
    instance = TikTokApi(proxies=proxies,debug=False)
    flow = Flow(instance)
    flow.device_register()
    """

    def __init__(self, main: TikTok):
        """__init__

        Args:
            main (TikTok): TikTok instance
        """
        self.main = main
        self.api = Api(self.main)

    async def device_register(self):
        device = Device(self.main)
        # print("Registering Device")
        device.prepareDevice()
        await self.api.get_domains.v5(with_device=False)
        await self.api.service.device_register()
        """
        Contact https://t.me/sovitt

        """

        # print("Device Register complete")
