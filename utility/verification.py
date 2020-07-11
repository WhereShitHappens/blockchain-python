"""Provides verifications helper methods."""

from utility.hash_util import hash_string_256, hash_block


class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """Validate a proof o fwork number and see if it solves the puzzle algorith

        Arguments:
            :transactions: The transactions of the block for which the proof is needed
            :last_hash: The previous block's hash which will be stored in the block
            :proof: The proof number we're testing.
        """
        # Create a string with all the hash inputs
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        print(guess)
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2] == '00'
    @classmethod
    def verify_chain(cls, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            # We are going through every block and compare the 'previous_hash' value
            # to the corresponding HASHED entry in the blockchain
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True
    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        # is_valid = True
        # for tx in open_transactions:
        #     if verify_transaction(tx):
        #         is_valid = True
        #     else:
        #         is_valid = False
        # return is_valid
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
    @staticmethod
    def verify_transaction(transaction, get_balance):
        """Verify a transaction by checking whether the sender has sufficient coin balance

        Arguments:
        :transaction: Get passed from the ad_transaction function
        """
        sender_balance = get_balance()
        print('Sender balance: ', sender_balance)
        return sender_balance >= transaction.amount

