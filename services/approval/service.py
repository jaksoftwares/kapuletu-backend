def approve_transaction(transaction_id):
    # Logic to move from pending to QLDB ledger
    return {"status": "approved", "transaction_id": transaction_id}

def reject_transaction(transaction_id):
    return {"status": "rejected", "transaction_id": transaction_id}
