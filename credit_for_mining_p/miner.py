import hashlib
import requests
import os
import uuid

import sys


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:5] == "00000"

def find_and_replace(string, char):
    string = list(string)
    for i in string:
        if i == char:
            del(string[string.index(i)])
    return "".join(string)

def file_exists(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = int(sys.argv[1])
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted

    # Checks if my_id.txt exists and has an ID
    if file_exists('my_id.txt'):
        # Set the ID For mining
        id_file = open("my_id.txt", "r")
        miner_id = id_file.read()

    else:
        # Creates and opens my_id.txt file
        id = open("my_id.txt", "w+")
        # Creates and writes an ID
        UUID = find_and_replace(str(uuid.uuid4()), "-")
        id.write(UUID)

    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof, "miner_id": miner_id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))