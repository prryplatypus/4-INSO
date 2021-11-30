import asyncio
import aiohttp
from bs4 import BeautifulSoup


queue = asyncio.Queue()


async def asincrono():
    urls = [
        'https://www.imdb.com/',
        'https://www.amazon.es/',

    ]
    for url in urls:
        async with aiohttp.ClientSession() as session:
            content = await session.get(url)
            content = await content.text()

            soup = BeautifulSoup(content, 'html.parser')
            img_urls = []

            for img in soup.find_all('img'):
                img_urls.append(img['src'])
                print(f"{img['src']}")

            try:
                img_responses = await asyncio.gather(
                    *[session.get(img) for img in img_urls]
                )

                imgs = await asyncio.gather(
                    *[resp.read() for resp in img_responses]
                )

                for url, file in zip(img_urls, imgs):
                    with open(f'downloaded_images/{url.split("/")[-1]}', 'wb') as f:
                        f.write(file)
            except OSError as err:
                print(f'{err=}')
            except IOError as err:
                print(f'{err}')
            except Exception:
                print('get error')

        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(asincrono())
