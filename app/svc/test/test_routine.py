import asyncio

async def test():
    print('test: begin...')
    r = await asyncio.sleep(1)
    print('test: finish.')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.create_task(test())
    loop.create_task(test())
    loop.run_forever()