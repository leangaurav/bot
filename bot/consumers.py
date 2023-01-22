import json
import time
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


#########
# UTIlS #
#########
def set_google_creds_path(path: str):
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
set_google_creds_path('token.json')


from .asr.google import AsrConfig,AudioEncoding, AsrType, get_async_streaming_asr_client


asr_config = AsrConfig(
    sample_rate=8000,
    encoding=AudioEncoding.MULAW,
    asr_type=AsrType.GOOGLE,
    language="en-US",
   )

async def audio_stream_from_file(file_path: str, chunk_size: int, sleep_time: float):
    with open(file_path, 'rb') as audio_file:
        while True:
            data = audio_file.read(chunk_size)
            if data == '':
                break
            yield data
            await asyncio.sleep(sleep_time)

class TwilioConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("connect start")
        await self.accept()
        print("connect half")

        asr_results_iter = await get_async_streaming_asr_client(asr_config, audio_stream_from_file('lathe.wav', 4000, 0.5))

        print("connect print")
        async for resp in asr_results_iter:
            print(resp)

        print("connected")

    async def disconnect(self, close_code):
        print("Disconnected")


    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)

