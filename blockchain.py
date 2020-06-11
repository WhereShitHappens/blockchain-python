blockchain = [[1]]

def add_value(transaction_amount):
    blockchain.append([blockchain[-1], transaction_amount])
    print(blockchain)

add_value(2)
add_value(0.9)
add_value(45.0587)

print(blockchain[-1])
print(blockchain[-2])

22
