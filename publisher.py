import nats
import json

class Publisher:

    def __init__(self, server_url):
        self.server_url = server_url

    async def publish_result(self, result, queue):
        nc = await nats.connect(self.server_url)
        await nc.publish(queue, json.dumps(result).encode())
        print('Sent to address', queue, 'message:', result)
        await nc.close()

    async def __call__(self, result, queue):
        await self.publish_result(result, queue)
