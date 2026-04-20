def test_parse_message():
    from services.ingestion.parser_engine import parse_message
    result = parse_message("KES 500 from 254700000000")
    assert result["amount"] == "500"
