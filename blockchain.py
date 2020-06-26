# Version 0.2.6 'Happy Birthday to me' edition
print(' *' * 26, '26/06/1990', '* ' * 26)

# Known Version Issues:
# The the balance doesn't update correctly


MINING_REWARD = 10

# The first block of the blockchain
genesis_block = {
    'previous_hash': 'genesis',
    'index': 0,
    'transactions': []
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
    return '-'.join([str(block[key]) for key in block])


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
    We are checking if the participant has enough balance to complete the current transaction
    :param participant: aka transaction['sender']
    :return:
    """
    # We create a list that keeps track of all the senders in the blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant]
                 for block in blockchain]
    # Since the open transactions are not part of the chain yet, we check them as well
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print('tx sender: ', tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant]
                    for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    print('Balance: ', amount_received - amount_sent)
    return amount_received - amount_sent


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    # The last transaction in every block is the mining reward
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
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
    return True


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
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        print(get_balance(owner))
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