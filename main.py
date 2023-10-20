from sys import platform
from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy, run
from random import shuffle, choice

from inquirer.themes import load_theme_from_dict as loadth
from termcolor import cprint, colored
from inquirer import List, prompt

from modules.transactions import Module
from models.account import Account
from data.data import KEYS, HELZY
from config import RANDOMIZE_WALLETS, DELAY
from modules.utils import (
    sleeping,
    logger,
    check_gas,
    info
)


async def main():
    if RANDOMIZE_WALLETS:
        shuffle(KEYS)

    for key_id, key in enumerate(KEYS, start=1):
        try:
            account = Account(key, key_id)
        except:
            logger.critical(key_id, 'PROXY ERROR', sep=" | ")
            continue
        
        logger.debug(f"{key_id} | Working on: {account.address}")

        await module_proceeding(account)

        await sleeping(DELAY, 'Sleeping between wallets', 'yellow')


@check_gas
async def module_proceeding(account: Account, retry: int = 0) -> None:
    
    await info(f"{account.id} | Actual module: {module}")

    while retry < 5:
        retry += 1

        result = await Module(account).start(module)

        if result:
            return

        await sleeping([60, 120], 'Sleeping between module retries', 'yellow')


def get_action() -> str:

    theme = {
        "Question": {
            "mark_color": "cyan"
        },
        "List": {
            "selection_color": "bold_green",
            "selection_cursor": ">>>",
            "unselected_color": "red"
        }
    }

    question = [
        List(
            'action',
            message=colored("Choose the action", 'cyan'),
            choices=['Delegate', 'Vote']
        )
    ]

    return prompt(questions=question, theme=loadth(theme))['action']


if __name__ == '__main__':
    cprint(choice(HELZY), choice(['green', 'magenta', 'light_cyan']))

    module = get_action()

    if platform.startswith("win"):
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    run(main())
