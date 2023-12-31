from loguru import logger


with open('data/priv.txt') as file:
    KEYS = [x.strip() for x in file.readlines()]

if len(KEYS) < 1:
    logger.critical("You didn`t add wallets in priv.txt!")
    exit()

with open('data/proxies.txt') as file:
    PROXIES = dict(zip(KEYS, [x.strip() for x in file.readlines()]))

ARB_ADDRESS=0x912ce59144191c1204e64559fe8253a0e49e6548
ARB_GOVERNOR_ADDRESS=0x789fc99093b09ad01c34dc7251d0c89ce743e5a4

HELZY = [
'''
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  ____  ____  | || |  _________   | || |   _____      | || |   ________   | || |  ____  ____  | |
| | |_   ||   _| | || | |_   ___  |  | || |  |_   _|     | || |  |  __   _|  | || | |_  _||_  _| | |
| |   | |__| |   | || |   | |_  \_|  | || |    | |       | || |  |_/  / /    | || |   \ \  / /   | |
| |   |  __  |   | || |   |  _|  _   | || |    | |   _   | || |     .'.' _   | || |    \ \/ /    | |
| |  _| |  | |_  | || |  _| |___/ |  | || |   _| |__/ |  | || |   _/ /__/ |  | || |    _|  |_    | |
| | |____||____| | || | |_________|  | || |  |________|  | || |  |________|  | || |   |______|   | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
''',
'''
 █████   █████ ██████████ █████       ███████████ █████ █████
░░███   ░░███ ░░███░░░░░█░░███       ░█░░░░░░███ ░░███ ░░███ 
 ░███    ░███  ░███  █ ░  ░███       ░     ███░   ░░███ ███  
 ░███████████  ░██████    ░███            ███      ░░█████   
 ░███░░░░░███  ░███░░█    ░███           ███        ░░███    
 ░███    ░███  ░███ ░   █ ░███      █  ████     █    ░███    
 █████   █████ ██████████ ███████████ ███████████    █████   
░░░░░   ░░░░░ ░░░░░░░░░░ ░░░░░░░░░░░ ░░░░░░░░░░░    ░░░░░    
''',
]
