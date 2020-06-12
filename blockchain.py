# Initializing the blockchain
blockchain = []


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain."""
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    """ Append a new value as well as the last blockchain value to the blockchain

     Aruments:
         :transaction_amount: The amount that should be added.
         :last_transaction: The last blockchain transaction (default [1])
     """
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    """ Returns the input of the user (a new transction amount) as a float"""
    user_input = float(input('Your transaction amount please: '))
    return user_input


tx_amount = get_user_input()
add_value(tx_amount)

# tx_amount = get_user_input()
add_value(last_transaction=get_last_blockchain_value(), transaction_amount=get_user_input())

tx_amount = get_user_input()
add_value(last_transaction=get_last_blockchain_value(), transaction_amount=tx_amount)

print(blockchain)

# # Global local variables
# name  = 'Aris'
# def get_name():
# 	name = input("Your name please:")
# get_name()
# print(name)

# def greet(name, age =29):
# 	print('Hellot ' + 'me name is ' + name + ', I am ' + str(age) )
# greet('aris')

# # Keyword arguments
# def greet(name, age):
# 	print('My name is ' + name + ' and I am ' + str(age))
# greet(age=29, name='Aris')

# fucking hell this is a fucking nightmare
# I cant even describe it because it wouldn't feel like a nightmare in words
# this is some real bullshit
# its not like I have not been trying 
# Is it not enough? Maybe
# Can I try harder? Maybe
# Will this shit ever end? For sure
