<p>
<a href="https://pypi.org/project/PyRPAN">
    <img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/PyRPAN">
</a>

<a href="https://pypi.org/project/flake8/">
    <img height="20" alt="Flake badge" src="https://img.shields.io/badge/code%20style-flake8-blue.svg">
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
**Source Code**: [github.com/b1uejay27/PyRPAN](https://github.com/b1uejay27/PyRPAN)<br>
**PyPi**: [pypi.org/project/PyRPAN](https://pypi.org/project/PyRPAN)<br>
**Discord Server**: [discord.gg/DfBp4x4](https://discord.gg/DfBp4x4)
