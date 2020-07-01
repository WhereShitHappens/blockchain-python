# Version 0.2.7 // 94

import functools
import hashlib as hl
import json


MINING_REWARD = 10

# The first block of the blockchain
genesis_block = {
    'previous_hash': 'genesis',
    'index': 0,
    'transactions': [],
    'proof': 0.0
}

# Kick starting the blockchain
blockchain = [genesis_block]

# Transactions that are pending to be mined.
open_transactions = []

# Using a set adds another layer of security making sure there are no duplicate values
# Indexing won't be required
participants = {'Aris'}

# Names are just placeholders for the hashes that will be implemented later
owner = 'Aris'


def hash_block(block):
    # Later we will use a cryptographic hashing method instead
    return hl.sha256(json.dumps(block).encode()).hexdigest()


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hl.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    # We will be using a dictionary for transactions as well, not to be confused with a blockchain block
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    # This is where we pass the transaction to the next function
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        print('Open transactions: ', open_transactions)
        return True
    return False


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    print('Sender balance: ', sender_balance)
    return sender_balance >= transaction['amount']


def get_balance(participant):
    """
    We are checking for the amount the participant has received and sent
    :param participant: aka transaction['sender']
    :return:
    """
    # We create a list that keeps track of all the senders in the blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant]
                 for block in blockchain]
    # Since the open transactions are not part of the chain yet, we check them as well
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant]
                    for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    print('Balance: ', amount_received - amount_sent)
    return amount_received - amount_sent


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    # Creating a copy of the open transaction list prevents the reward transaction doesnt
    # become part of the open transactions, in case we don't reach the code that empties it.
    # Impoortant to copy by reference instead of value. Otherwise changes in one list affect the other
    copied_transactions = open_transactions[:]
    # The last transaction in every block is the mining reward
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    print('Hashed block: ', hashed_block)
    print('Blockchain', blockchain)
    return True


def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    # Important to make sure the input gets converted to a float number
    tx_amount = float(input('Enter the amount to send to ' + tx_recipient + ': '))
    # Returning a two value tuple
    return tx_recipient, tx_amount


def get_user_choice():
    user_choice = input('Your choice: ')
    return user_choice


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        # We are going through every block and compare the 'previous_hash' value
        # to the corresponding HASHED entry in the blockchain
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid')
            return False
    return True


def verify_transactions():
    # is_valid = True
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid = True
    #     else:
    #         is_valid = False
    # return is_valid
    return all([verify_transaction(tx) for tx in open_transactions])


def print_blockchain_elements():
    for (index, block) in enumerate(blockchain):
        print('block number ', index, 'block contents: ', block)
    else:
        print('*' * 20)
        print('Complete blockchain: ', blockchain)
        print('-' * 20)

waiting_for_input = True

while waiting_for_input:
    print('What do you want to do today? Select an option: ')
    print('1: Make a new transaction')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks and the blockchain')
    print('4: Output the participants')
    print('5: Show balance')
    print('6: Check transaction validity')
    print('h: Manipulate the blockchain')
    print('9: Print a block')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        # We transfer the values from the tuple to local variables
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Added transaction')
        else:
            print('Transaction failed')
    elif user_choice == '2':
        # We empty the list containing the open transactions
        if mine_block():
            # We are resetting the list here, instead of inside the function, so it is not a local variable
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        print(get_balance(owner))
    elif user_choice == '6':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) >= 0:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Aris', 'amount': 667}]
            }
    elif user_choice == '9':
        block_number = int(input('Enter block number you want to print: '))
        print(blockchain[block_number])
    # In order for the verification to work, at least one valid block has to be mined
    if not verify_chain():
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f}'.format('Aris', get_balance('Aris')))