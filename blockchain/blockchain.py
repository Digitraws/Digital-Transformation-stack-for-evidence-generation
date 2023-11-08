import os
from dotenv import load_dotenv
from pinatapy import PinataPy
from solana import createTransaction

load_dotenv()


def main(path_to_file):
    pinata = PinataPy(os.environ["PINATA_API_KEY"], os.environ["PINATA_API_SECRET"])
    res = pinata.pin_file_to_ipfs(path_to_file)
    uri = "https://gateway.pinata.cloud/ipfs/" + res["IpfsHash"]

    print("File Upload Successfull")
    print("IPFS URI: ", uri)

    print("Committing to Solana on Program ID: ", os.environ["SOLANA_PROGRAM_ID"])

    res = createTransaction(
        uri=uri,
        keypair_path=os.environ["SOLANA_KEYPAIR_PATH"],
        program_id=os.environ["SOLANA_PROGRAM_ID"],
    )
    print("Transaction response: ", res)


evidence_path = os.path.abspath("../client/evidence.zip")

main(evidence_path)