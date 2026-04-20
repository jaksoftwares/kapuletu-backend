def test_approve_transaction():
    from services.approval.service import approve_transaction
    result = approve_transaction("tx123")
    assert result["status"] == "approved"
