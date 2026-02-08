# Transaction Recording Agent Setup Guide

## Overview
This is a serverless ChatGPT-integrated agent that records financial transactions to an Excel file stored on AWS S3.

## Architecture
```
ChatGPT (OpenAI API)
    ↓
AWS Lambda Function
    ↓
Transaction Agent (Python)
    ↓
AWS S3 (Excel File)
```

## Prerequisites
- AWS Account with S3 and Lambda access
- OpenAI API key (for GPT-4 access)
- Python 3.9+
- AWS CLI configured

## Setup Steps

### 1. Create S3 Bucket
```bash
aws s3 mb s3://your-transaction-bucket --region us-east-1
```

### 2. Create Lambda Execution Role
```bash
aws iam create-role --role-name transaction-agent-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach S3 policy
aws iam attach-role-policy --role-name transaction-agent-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

### 3. Package Lambda Functions
```bash
mkdir lambda_package
cd lambda_package
pip install -r ../requirements.txt -t .
cp ../transaction_agent.py .
cp ../openai_integration.py .
zip -r ../lambda_function.zip .
```

### 4. Create Lambda Function
```bash
aws lambda create-function \
  --function-name transaction-recorder \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/transaction-agent-role \
  --handler transaction_agent.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --environment Variables={S3_BUCKET_NAME=your-transaction-bucket,OPENAI_API_KEY=your-api-key}
```

### 5. Create API Gateway Endpoint
```bash
# Create REST API
aws apigateway create-rest-api --name transaction-api --description "Transaction Agent API"

# Create resource and method
# (Use AWS Console for easier setup)
```

### 6. Configure ChatGPT Integration

#### Option A: Using OpenAI Assistant API
```python
from openai_integration import create_assistant
assistant_id = create_assistant()
# Use this ID in your ChatGPT custom GPT configuration
```

#### Option B: Using Custom GPT
1. Go to https://chatgpt.com/gpts
2. Create a new GPT
3. Add action with your Lambda API Gateway endpoint
4. Configure the function schema from the code

## Environment Variables
Set these in Lambda:
- `S3_BUCKET_NAME`: Your S3 bucket name
- `OPENAI_API_KEY`: Your OpenAI API key

## Usage Examples

### Direct Lambda Call
```bash
curl -X POST https://your-api-endpoint/record \
  -H "Content-Type: application/json" \
  -d '{
    "action": "record_transaction",
    "beneficiary": "John Doe",
    "date": "2024-02-08",
    "amount": 5000,
    "purpose": "Monthly salary"
  }'
```

### ChatGPT Conversation
```
User: "I paid ABC Corp $2500 for consulting services on Feb 8, 2024"

Agent: "I'll record this transaction. Let me confirm:
- Beneficiary: ABC Corp
- Amount: $2500
- Date: 2024-02-08
- Purpose: Consulting services

Is this correct? (yes/no)"

Agent: ✓ Transaction recorded successfully!
Transaction ID: A1B2C3D4
```

## File Structure
```
.
├── transaction_agent.py       # Core transaction recording logic
├── openai_integration.py      # ChatGPT integration
├── requirements.txt           # Python dependencies
├── DEPLOYMENT_GUIDE.md        # This file
└── test_agent.py             # Local testing (optional)
```

## Testing Locally
```python
from transaction_agent import record_transaction

# Test recording a transaction
result = record_transaction(
    beneficiary="Test Company",
    date="2024-02-08",
    amount=1000,
    purpose="Test transaction"
)
print(result)
```

## Monitoring
- CloudWatch Logs: Check Lambda execution logs
- S3 Console: View transactions.xlsx file
- OpenAI API Dashboard: Monitor API usage

## Troubleshooting

### "No module named boto3"
```bash
pip install -r requirements.txt
```

### S3 Access Denied
- Verify IAM role has S3 permissions
- Check bucket name in environment variable

### OpenAI API Errors
- Verify API key is correct
- Check account has GPT-4 access
- Monitor rate limits

## Cost Estimation
- Lambda: ~$0.20/million requests (free tier: 1M/month)
- S3: ~$0.023/GB stored (minimal for Excel file)
- OpenAI API: Variable based on usage (~$0.03/1K tokens)

## Security Best Practices
- Store API keys in AWS Secrets Manager
- Use IAM roles instead of access keys
- Enable S3 versioning for Excel file
- Encrypt Lambda environment variables
- Use VPC endpoints for private S3 access

## Future Enhancements
- [ ] Multi-user support with separate transaction logs
- [ ] Transaction categorization (income, expense, transfer)
- [ ] Monthly summaries and reports
- [ ] Real-time notifications
- [ ] Transaction editing/deletion
- [ ] Financial analytics dashboard
- [ ] Support for multiple currencies
- [ ] Integration with accounting software (QuickBooks, etc.)
