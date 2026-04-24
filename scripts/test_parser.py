import sys
import os
import json

# Add project root to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ingestion.parser_engine import parse_message

def test_parser():
    """
    Test Utility: Validates the AI Parsing Engine against real-world message samples.
    
    This script allows developers to quickly verify how the parser handles 
    different message formats (MPESA, Bank Alerts, Informal Text) without 
    running the full backend infrastructure.
    """
    # Sample real-world and synthetic financial messages
    test_cases = [
        # 1. Official MPESA Received (Standard Kenyan Pattern)
        "UDLQC1OXZA Confirmed.You have received Ksh2,500.00 from DICKSON MWANIKI 0720000971 on 21/4/26 at 10:29 PM",
        
        # 2. Official MPESA Sent (Outbound pattern)
        "OIB819DJS2 Confirmed. Ksh 1,200.00 sent to JANE DOE 0711222333 on 15/4/26 at 11:00 AM.",
        
        # 3. Informal/Manual Entry (Simple structured text)
        "John Doe sent 1500 for welfare",
        
        # 4. Informal/Manual Entry (Reverse order)
        "5000 from Mary for roof contribution",
        
        # 5. Bank Alert Style (Standard banking notification)
        "Credit: KES 10,000.00 from PETER MAIN on 2026-04-20 14:00. Ref: TXN998877",
        
        # 6. Messy/Short Message (Ambiguous text)
        "Roof contribution 2500 Peter",
        
        # 7. High Value / Currency variation (Normalization check)
        "Ksh 150,000.00 from Welfare Fund"
    ]

    print("="*80)
    print(f"{'RAW MESSAGE':<50} | {'AMOUNT':<8} | {'NAME':<15} | {'CONF'}")
    print("-"*80)

    # Process each test case through the parser engine
    for msg in test_cases:
        result = parse_message(msg)
        
        name = str(result.get("sender_name"))[:15]
        amount = result.get("amount", 0.0)
        conf = result.get("confidence_score", 0.0)
        
        # Output results in a structured table for review
        print(f"{msg[:50]:<50} | {amount:<8,.2f} | {name:<15} | {conf:.2f}")

    print("="*80)

if __name__ == "__main__":
    test_parser()
