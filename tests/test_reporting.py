def test_generate_summary():
    from services.reporting.daily_summary import generate_summary
    result = generate_summary()
    assert "total_collected" in result
