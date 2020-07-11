from blockchain import Blockchain
from utility.verification import Verification

class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = 'ARIS'
        self.blockchain = Blockchain(self.id)

    def get_user_choice(self):
        user_choice = input('Your choice: ')
        return user_choice

    def print_blockchain_elements(self):
        for (index, block) in enumerate(self.blockchain.chain):
            print('block number ', index, 'block contents: ', block)
        else:
            print('*' * 20)
            print('Complete blockchain: ', self.blockchain)
            print('-' * 20)

    def get_transaction_value(self):
        tx_recipient = input('Enter the recipient of the transaction: ')
        # Important to make sure the input gets converted to a float number
        tx_amount = float(input('Enter the amount to send to ' + tx_recipient + ': '))
        # Returning a two value tuple
        return tx_recipient, tx_amount

    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print('What do you want to do today? Select an option: ')
            print('1: Make a new transaction')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks and the blockchain')
            print('4: Output the participants')
            print('5: Show balance')
            print('6: Check transaction validity')
            print('q: Exit the program')
            print('h: Manipulate the blockchain')
            print('9: Print a block')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                # We transfer the values from the tuple to local variables
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                print(self.blockchain.participants)
            elif user_choice == '5':
                print(self.blockchain.get_balance)
            elif user_choice == '6':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == 'q':
                break
            elif user_choice == 'h':
                if len(self.blockchain.get_chain()) >= 0:
                    self.blockchain.get_chain()[0] = {
                        'previous_hash': '',
                        'index': 0,
                        'transactions': [{'sender': 'Chris', 'recipient': 'Aris', 'amount': 667}]
                    }
            elif user_choice == '9':
                block_number = int(input('Enter block number you want to print: '))
                print(self.blockchain.get_chain()[block_number])
            # In order for the verification to work, at least one valid block has to be mined
            if not Verification.verify_chain(self.blockchain.chain):
                print('Invalid blockchain!')
                break
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))

# We want to make sure that the input is executed only if node.py is the __main__
if __name__ == '__main__':
    node = Node()
    node.listen_for_input()

print(__name__)