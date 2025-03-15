import bittensor as bt
import datetime
import threading
import time
from app.core.constants import (
    SUBNET_UID,
    NETWORK,
    NEURON_EPOCH_LENGTH,
    BLOCK_IN_SECONDS
)
from app.utils.misc import ttl_get_block

class Metagraph:
    @property
    def block(self) -> int:
        return ttl_get_block(self)

    def __init__(self):
        self.subtensor = bt.subtensor(network=NETWORK)
        self.metagraph = self.subtensor.metagraph(netuid=SUBNET_UID)
        self.last_update = self.block

    def get_uid(self, hotkey: str) -> int:
        self.sync()
        try:
            uid = self.metagraph.hotkeys.index(hotkey)
            return uid
        except ValueError:
            return -1

    def sync(self):
        if self.block - self.last_update > NEURON_EPOCH_LENGTH:
            self.metagraph.sync(subtensor=self.subtensor)
            self.last_update = self.block
        
METAGRAPH = Metagraph()