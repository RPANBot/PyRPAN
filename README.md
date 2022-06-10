<p>
<a href="https://pypi.org/project/PyRPAN">
    <img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/PyRPAN">
</a>

<a href="https://pypi.org/project/flake8/">
    <img height="20" alt="Flake badge" src="https://img.shields.io/badge/code%20style-flake8-blue.svg">
</a>
    
<a href="https://pypistats.org/packages/PyRPAN">
    <img height="20" alt="Stats Badge" src="https://img.shields.io/pypi/dm/PyRPAN">
</a>
    
<a href="https://github.com/RPANBot/PyRPAN/blob/main/LICENSE">
    <img height="20" alt="Stats Badge" src="https://img.shields.io/github/license/RPANBot/PyRPAN">
</a>
    
<a href="https://github.com/RPANBot/PyRPAN/stargazers">
    <img height="20" alt="Stats Badge" src="https://img.shields.io/github/stars/RPANBot/PyRPAN">
</a>
    
<a href="https://discord.gg/DfBp4x4">
    <img height="20" alt="Stats Badge" src="https://img.shields.io/discord/725895559973699645.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2">
</a>

</p>

### About

PyRPAN is an async API wrapper made in Python for the Reddit Public Access Network (RPAN), which is Reddit's streaming service.

### Example

```Python
import asyncio

from pyrpan import PyRPAN

rpan = PyRPAN(client_id='client id here', client_secret='client secret here')

async def main():
    broadcasts = await rpan.get_broadcast(id='stream id here')  
    print(broadcast.url)

    await rpan.close()

asyncio.run(main())
```

### Links
**Source Code**: [github.com/RPANBot/PyRPAN](https://github.com/RPANBot/PyRPAN)<br>
**PyPi**: [pypi.org/project/PyRPAN](https://pypi.org/project/PyRPAN)<br>
**Discord Server**: [discord.gg/DfBp4x4](https://discord.gg/DfBp4x4)
