# The genesis block is the first block, which kick starts the blockchain
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
    }

# Initiating our empty blockchain list
blockchain = [genesis_block]

open_transactions = []
owner = 'Aris'


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain."""
    if len(blockchain) < 1:
        return None
    # We could have used 'else', but return by its nature can only run once
    return blockchain[-1]


# We don't need the '=[1]' default argument since line 20, it is just for reference
def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain

    Arguments:
        :sender: The sender of the coins.
        :recipient: The receiver of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount}
    open_transactions.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    # List comprehension
    # Only possible to join strings
    hashed_block = '-'.join([str(last_block[key]) for key in last_block])

    print(hashed_block)
    for key in last_block:
        value = last_block[key]
        hashed_block = hashed_block + str(value)

    print(hashed_block)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float"""
    # Get the user input, transform it from a string to a float and store it
    tx_recipient = input('Enter the sender of the transaction:')
    tx_amount = float(input('Your transaction amount please: '))
    # We return a tuple
    return tx_recipient, tx_amount


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    """ Essentially we will be checking if the current iteration of a block equals
     with the corresponding list in the blockchain. There are only two elements (parameters)
     in the blockchain, but many lists. That's why we need the index, to check if
     the current element equals its matching list in the blockchain
    """
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid


waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # Add the transaction to the blockchain
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        # Using 'continue' instead would stop the code at the current line and rerun the loo[
        print(blockchain)
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    print('Choice registered!')
    # Executed if it return not True
    # if not verify_chain():
    #     print_blockchain_elements()
    #     print('Invalid blockchain!')
    #     break
else:
    print('User left!')

print('Done!')

# 62
