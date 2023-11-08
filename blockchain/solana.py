import json
import base58
from solathon.core.instructions import *
from solathon import Client, Transaction, PublicKey, Keypair


client = Client("https://api.devnet.solana.com")

def getKeypair(keypair_path):
    with open(keypair_path, "r") as f:
        data = json.load(f)

    private_key_bytes = bytes(data[:32])
    private_key = base58.b58encode(private_key_bytes)
    keypair = Keypair.from_private_key(private_key)
    return keypair


def createTransaction(keypair_path, program_id, uri):
    account = getKeypair(keypair_path)
    program_id = PublicKey(program_id)
    data = uri.encode()
    instr = Instruction(program_id=program_id, keys=[], data=data)
    tx = Transaction(instructions=[instr], signers=[account])
    result = client.send_transaction(tx)
    return result
