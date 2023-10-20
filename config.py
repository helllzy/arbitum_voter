######################################################
# Main settings connected to account & transactions ##
######################################################

# all transactions will be completed via ONE of these RPC
RPC = ['https://rpc.ankr.com/arbitrum', 'https://arbitrum-mainnet.infura.io']

# delay between accounts
DELAY = [100, 200]

# all transactions will be completed below this gas price
MAX_GWEI = 6.15

# True if you want to randomize wallets execution
RANDOMIZE_WALLETS = True

# True if you want to use proxy. each account must have a proxy.
# provide your proxies in data/proxies.txt. format: ip:port:user:passw
USE_PROXY = False

# you can find it in any CastVote transaction
# previous id ex: cc955e31357eef096312216247b3f13ec835a84787cb337ebee38d5a95c035cc
PROPOSAL_ID = ''
