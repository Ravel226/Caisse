# src/transaction.py
from datetime import datetime

class TransactionHistory:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, order_items, total):
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": [(item.name, item.price) for item in order_items],
            "total": total
        }
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions
