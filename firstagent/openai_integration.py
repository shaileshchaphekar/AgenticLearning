"""
OpenAI Assistant Integration for Transaction Agent
Handles ChatGPT conversation and function calling
"""

import openai
import json
import os
from transaction_agent import record_transaction

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define tools/functions that ChatGPT can use
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "record_transaction",
            "description": "Record a financial transaction with beneficiary name, date, amount, and purpose. This will store the transaction in an Excel file on AWS S3.",
            "parameters": {
                "type": "object",
                "properties": {
                    "beneficiary": {
                        "type": "string",
                        "description": "Name of the beneficiary (person/organization receiving the payment)"
                    },
                    "date": {
                        "type": "string",
                        "description": "Transaction date in YYYY-MM-DD format"
                    },
                    "amount": {
                        "type": "number",
                        "description": "Transaction amount in currency units"
                    },
                    "purpose": {
                        "type": "string",
                        "description": "Purpose or description of the transaction"
                    }
                },
                "required": ["beneficiary", "date", "amount", "purpose"]
            }
        }
    }
]

def process_tool_call(tool_name: str, tool_input: dict):
    """Process function calls from ChatGPT"""
    if tool_name == "record_transaction":
        return record_transaction(
            beneficiary=tool_input.get('beneficiary'),
            date=tool_input.get('date'),
            amount=tool_input.get('amount'),
            purpose=tool_input.get('purpose')
        )
    return {"error": f"Unknown tool: {tool_name}"}

def chat_with_transaction_agent(user_message: str, conversation_history=None):
    """
    Main function to interact with the transaction agent
    
    Args:
        user_message: User's message/request
        conversation_history: Previous conversation messages (optional)
    
    Returns:
        dict: Agent's response and any recorded transactions
    """
    if conversation_history is None:
        conversation_history = []
    
    # System prompt for the agent
    system_prompt = """You are a helpful financial transaction recording agent. Your job is to:
1. Listen to users describe financial transactions
2. Extract transaction details: beneficiary name, date, amount, and purpose
3. Ask clarifying questions if any details are missing
4. Confirm transaction details with the user before recording
5. Use the record_transaction function to save transactions to AWS S3

Be friendly, professional, and accurate. Always confirm all details before recording."""
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Call OpenAI Assistant API
    response = openai.ChatCompletion.create(
        model="gpt-5.2",
        messages=[
            {"role": "system", "content": system_prompt},
            *conversation_history
        ],
        tools=TOOLS,
        tool_choice="auto",
        max_tokens=1000
    )
    
    assistant_message = response.choices[0].message
    transactions_recorded = []
    
    # Process tool calls if any
    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            tool_result = process_tool_call(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )
            
            if tool_result.get('success'):
                transactions_recorded.append(tool_result)
            
            # Add assistant's function call to history
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [tool_call]
            })
            
            # Add tool result to history
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })
    
    return {
        "response": assistant_message.content or "Transaction processed",
        "transactions_recorded": transactions_recorded,
        "conversation_history": conversation_history
    }

def create_assistant():
    """Create a new OpenAI Assistant (run once during setup)"""
    assistant = openai.beta.assistants.create(
        name="Transaction Recorder",
        instructions="You are a helpful financial transaction recording assistant. Help users record transactions by collecting beneficiary, date, amount, and purpose information.",
        model="gpt-4",
        tools=TOOLS
    )
    print(f"Assistant created with ID: {assistant.id}")
    return assistant.id
