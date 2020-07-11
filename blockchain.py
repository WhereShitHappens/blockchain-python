# Version 0.2.9 // 150

import functools

import json

from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction


MINING_REWARD = 10

print(__name__)

class Blockchain:
    def __init__(self, hosting_node_id):
        # The first block of the blockchain is declared in the constructor method of the Blockchain class
        genesis_block = Block('genesis', '', [], 100, 0)
        # Kick starting the blockchain. Double underscores makes it harder for the attributes to be called from outside
        self.chain = [genesis_block]
        # Transactions that are pending to be mined.
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

        # Using a set adds another layer of security making sure there are no duplicate values
        # Indexing won't be required
        # Depreciated
        participants = {'Aris'}

    @property
    def chain(self):
        return self.__chain[:]

    # def get_chain(self):
    #     # Returning a copy of the chain
    #     return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        """We are using to predict cases where the blockchain file is inaccessible
            in which case will initiate a new blockchain.
            Note that the commented code is in case we need to revert back to using Pickle
        """
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                # file_content = pickle.loads(f.read())
                print(file_content)
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                # We use the range selector on the line to remove the new line
                # backslash n character
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                # blockchain = [{'previous_hash': block['previous_hash'], 'index': block['index'], ]} for block in blockchain]
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    # converted_tx = [OrderedDict(
                    #         [('sender', tx['sender']),
                    #          ('recipient', tx['recipient']),
                    #          ('amount', tx['amount'])]) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    # updated_transaction = OrderedDict(
                    #     [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        # What happens here is that when we can't find the blockchain file we will produce a new blockchain
        except (IndexError, IOError):
            print('Handled exception...')
            # pass
        finally:
            print('Cleanup! This will run even if there is an error')

    def save_data(self):
        """Save blockchain & open transactions snapshot to a file """
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                # Pickle
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        # This is how we can access the valid_proof function from our verification script
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        """
        We are checking for the amount the participant has received and sent
        :param participant: aka transaction['sender']
        :return:
        """
        participant = self.hosting_node
        # We create a list that keeps track of all the senders in the blockchain
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                     for block in self.__chain]
        # Since the open transactions are not part of the chain yet, we check them as well
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,
                                       tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                        for block in self.__chain]
        amount_received = functools.reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        print('Balance: ', amount_received - amount_sent)
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent with the transaction (default = 1.0)
        """
        # We will be using a dictionary for transactions as well, not to be confused with a blockchain block
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }
        transaction = Transaction(sender, recipient, amount)
        # transaction = OrderedDict(
        #     [('sender', sender), ('recipient', recipient), ('amount', amount)])
        # This is where we pass the transaction to the next function
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)
            print('Open transactions: ', self.__open_transactions)
            self.save_data()
            return True
        return False

    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        # reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
        # Creating a copy of the open transaction list prevents the reward transaction doesnt
        # become part of the open transactions, in case we don't reach the code that empties it.
        # Impoortant to copy by reference instead of value. Otherwise changes in one list affect the other
        copied_transactions = self.__open_transactions[:]
        # The last transaction in every block is the mining reward
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        # Below is the code of the block we were using before block started using classes
        # block = {
        #     'previous_hash': hashed_block,
        #     'index': len(blockchain),
        #     'transactions': copied_transactions,
        #     'proof': proof
        # }
        # We are using double underscore, otherwise we would append to the copy of the chain
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        print('Hashed block: ', hashed_block)
        print('Blockchain', self.__chain)
        return True

