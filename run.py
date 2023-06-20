import asyncio
from contextlib import suppress

from core.bot_app import main

if __name__ == '__main__':
    with suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
