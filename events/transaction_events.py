from events.event_bus import emit_event

def handle_transaction_approved(transaction):
    emit_event("TRANSACTION_APPROVED", transaction)
