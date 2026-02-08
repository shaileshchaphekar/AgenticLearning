"""
Example client to test the transaction agent locally
"""

import json
from datetime import datetime, timedelta

def test_transaction_recording():
    """Test transaction recording with example data"""
    from transaction_agent import record_transaction
    
    # Test cases
    test_cases = [
        {
            "beneficiary": "Acme Corporation",
            "date": "2024-02-05",
            "amount": 2500.50,
            "purpose": "Monthly consulting services"
        },
        {
            "beneficiary": "Sarah Johnson",
            "date": "2024-02-06",
            "amount": 1500,
            "purpose": "Freelance project payment"
        },
        {
            "beneficiary": "Global Supplies Inc",
            "date": "2024-02-07",
            "amount": 3200.75,
            "purpose": "Office equipment and supplies"
        },
        {
            "beneficiary": "John Smith",
            "date": "2024-02-08",
            "amount": 5000,
            "purpose": "Annual subscription renewal"
        }
    ]
    
    print("=" * 60)
    print("TRANSACTION AGENT - LOCAL TEST")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[Test {i}] Recording transaction...")
        print(f"  Beneficiary: {test_case['beneficiary']}")
        print(f"  Date: {test_case['date']}")
        print(f"  Amount: ${test_case['amount']}")
        print(f"  Purpose: {test_case['purpose']}")
        
        result = record_transaction(
            beneficiary=test_case['beneficiary'],
            date=test_case['date'],
            amount=test_case['amount'],
            purpose=test_case['purpose']
        )
        
        if result['success']:
            print(f"  ✓ SUCCESS - Transaction ID: {result['transaction_id']}")
        else:
            print(f"  ✗ FAILED - {result['message']}")

def test_conversation_flow():
    """Test multi-turn conversation with ChatGPT (requires API key)"""
    try:
        from openai_integration import chat_with_transaction_agent
        
        print("\n" + "=" * 60)
        print("CHATGPT CONVERSATION TEST")
        print("=" * 60)
        
        # Simulate a conversation
        messages = [
            "Hi! I need to record a payment to John Doe for $1000 on January 15th. It was for freelance work.",
            "Actually, let me also record another transaction - paid ABC Corp $2500 on January 20 for consulting.",
            "Can you show me what transactions I've recorded?"
        ]
        
        conversation_history = None
        
        for msg in messages:
            print(f"\nUser: {msg}")
            response = chat_with_transaction_agent(msg, conversation_history)
            print(f"Agent: {response['response']}")
            
            if response['transactions_recorded']:
                for txn in response['transactions_recorded']:
                    print(f"  ✓ Recorded: {txn['transaction_id']}")
            
            conversation_history = response['conversation_history']
    
    except ImportError:
        print("OpenAI integration not available. Install openai package to test ChatGPT integration.")

def validate_inputs():
    """Test input validation"""
    from transaction_agent import record_transaction
    
    print("\n" + "=" * 60)
    print("INPUT VALIDATION TESTS")
    print("=" * 60)
    
    invalid_cases = [
        {
            "name": "Missing beneficiary",
            "beneficiary": "",
            "date": "2024-02-08",
            "amount": 100,
            "purpose": "Test"
        },
        {
            "name": "Invalid date format",
            "beneficiary": "John",
            "date": "08/02/2024",
            "amount": 100,
            "purpose": "Test"
        },
        {
            "name": "Negative amount",
            "beneficiary": "John",
            "date": "2024-02-08",
            "amount": -100,
            "purpose": "Test"
        },
        {
            "name": "Invalid amount",
            "beneficiary": "John",
            "date": "2024-02-08",
            "amount": "not a number",
            "purpose": "Test"
        }
    ]
    
    for test in invalid_cases:
        print(f"\n[Test] {test['name']}")
        result = record_transaction(
            beneficiary=test['beneficiary'],
            date=test['date'],
            amount=test['amount'],
            purpose=test['purpose']
        )
        
        if not result['success']:
            print(f"  ✓ Correctly rejected - {result['message']}")
        else:
            print(f"  ✗ Should have been rejected but wasn't")

if __name__ == "__main__":
    print("\n🚀 Starting Transaction Agent Tests...\n")
    
    # Run tests
    test_transaction_recording()
    validate_inputs()
    
    try:
        test_conversation_flow()
    except Exception as e:
        print(f"\nNote: ChatGPT test skipped - {str(e)}")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("=" * 60)
