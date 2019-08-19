import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 

def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof


def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        last_proof = requests.get(f'{node}/last_proof').json()['proof']

        new_proof = proof_of_work(last_proof)

        proof_guess = {"proof": new_proof}
        proof_data = requests.post(f'{node}/mine', json=proof_guess)

        if proof_data.json()["message"] == "New Block Forged":
            coins_mined += 1
            print(f"Coins mined: {coins_mined} \n")
        else:
            print(proof_data.json()["message"])

