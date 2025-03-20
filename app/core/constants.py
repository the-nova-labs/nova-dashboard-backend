import os

#DATABASE_URL = "sqlite:///test-nova-leaderboard.db"
DATABASE_URL = os.getenv("DATABASE_URL")
NETWORK = "local"
SUBNET_UID = 68
NEURON_EPOCH_LENGTH = 25
BLOCK_IN_SECONDS = 12
API_TOKEN = os.getenv("API_TOKEN")
VALIDATOR_API_KEY = os.getenv("VALIDATOR_API_KEY")