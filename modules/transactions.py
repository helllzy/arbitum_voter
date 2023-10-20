from config import PROPOSAL_ID
from models.account import Account


class Module:
    def __init__(self, account: Account):
        self.account = account


    async def start(self, module):

        match module:
            case 'Delegate':
                to=self.account.arb_address
                data='0x5c19a95c' + '0'*24 + self.account.address.lower()[2:]

            case 'Vote':
                to=self.account.governor_address
                data='0x56781388' + PROPOSAL_ID + '0'*63 + '1'

        return await self.account.send_transaction(
            to=to,
            data=data
            )
