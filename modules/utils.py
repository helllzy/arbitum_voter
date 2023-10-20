from random import randint, choice
from asyncio import sleep

from functools import wraps
from loguru import logger
from web3 import Web3

from config import MAX_GWEI

logger.add('data/logs.log')


async def sleeping(secs, text=None, color="white") -> None:
    if text:
        await info(text, color)

    await sleep(randint(*secs))


async def info(text, color="white") -> None:
    logger.opt(colors=True).info(f'<{color}>{text}</{color}>')


def check_gas(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        while True:
            try:
                w3 = Web3(
                     Web3.HTTPProvider(
                          choice(['https://ethereum.publicnode.com',
                                  'https://1rpc.io/eth',
                                  'https://rpc.ankr.com/eth'])))
                eth_gas_price = round(w3.from_wei(w3.eth.gas_price, 'gwei'), 2)

                if eth_gas_price > MAX_GWEI:
                    logger.warning(
                        f"gas`s {eth_gas_price} | sleep 30 seconds"
                        )
                    await sleep(30)
                else:
                    break

            except:
                pass

        return await func(*args, **kwargs)
    return wrapper
