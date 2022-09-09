import sys
import asyncio

from config.loggers import logger
from applications import parsing


if __name__ == "__main__":
    
    try:
        match sys.argv[1]:
            case "parsing":
                main = parsing.main
            case _:
                raise ValueError("you can enter only [parsing, dev, sheets]")
    except ValueError as e:
        logger.error(e)
        exit()

    url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering"
    asyncio.run(main(url))
    


