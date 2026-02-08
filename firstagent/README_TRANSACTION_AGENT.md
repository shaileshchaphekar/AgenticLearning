# Transaction Recording Agent with ChatGPT

A serverless AI agent that leverages ChatGPT to help you record financial transactions. Simply describe your transaction in natural language, and the agent will capture the details (beneficiary, date, amount, purpose) and store them in an Excel file on AWS S3.

## 🎯 Features

✅ **Natural Language Input** - Describe transactions conversationally  
✅ **Intelligent Extraction** - Automatically extracts transaction details  
✅ **Excel Export** - Stores transactions in formatted Excel on S3  
✅ **ChatGPT Integration** - Uses OpenAI's GPT-5.2 for smart conversations  
✅ **Serverless** - Runs on AWS Lambda (minimal cost)  
✅ **Validation** - Automatic input validation and error handling  
✅ **Confirmation** - Agent confirms details before saving  

## 📋 Transaction Details Captured

- **Beneficiary**: Name of person/organization
- **Date**: Transaction date (YYYY-MM-DD)
- **Amount**: Transaction amount
- **Purpose**: Description of transaction
- **Transaction ID**: Auto-generated unique ID
- **Timestamp**: When recorded

## 🏗️ Architecture

```
┌─────────────────┐
│   ChatGPT       │ (User converses with agent)
│   (Frontend)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│   OpenAI API                │ (GPT-5.2 with function calling)
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   AWS Lambda                │ (Serverless backend)
│   transaction_agent.py      │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   AWS S3                    │ (Excel storage)
│   transactions.xlsx         │
└─────────────────────────────┘
```

## 🚀 Quick Start

### 1. **Local Testing** (Before AWS Deployment)
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_agent.py
```

### 2. **Deploy to AWS**
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed AWS setup.

### 3. **Configure ChatGPT Integration**
- Get OpenAI API key from https://platform.openai.com/
- Set up custom GPT or use API integration
- Test conversations

## 💬 Example Conversation

```
User: "I paid Lisa Chen $500 on Feb 8th for graphic design work"

Agent: "I'll record this transaction. Let me confirm the details:
- Beneficiary: Lisa Chen
- Amount: $500
- Date: 2024-02-08
- Purpose: Graphic design work

Should I proceed? (yes/no)"

User: "Yes"

Agent: "✓ Perfect! Transaction recorded successfully.
Transaction ID: A7F2K9X1"
```

## 📁 Files

| File | Purpose |
|------|---------|
| `transaction_agent.py` | Core transaction recording logic |
| `openai_integration.py` | ChatGPT integration with function calling |
| `test_agent.py` | Local testing suite |
| `requirements.txt` | Python dependencies |
| `DEPLOYMENT_GUIDE.md` | AWS deployment instructions |
| `README.md` | This file |

## 🔧 Requirements

- Python 3.9+
- AWS Account (free tier eligible)
- OpenAI API key (GPT-5.2 access)
- Installed packages:
  - boto3 (AWS SDK)
  - openpyxl (Excel handling)
  - openai (OpenAI API)

## 📊 Output Format (Excel)

The agent creates an Excel file with this structure:

| Transaction ID | Date | Beneficiary | Amount | Purpose | Created At |
|---|---|---|---|---|---|
| A1B2C3D4 | 2024-02-05 | Acme Corp | 2500.50 | Consulting | 2024-02-08 10:30:00 |
| E5F6G7H8 | 2024-02-06 | Sarah J | 1500 | Freelance work | 2024-02-08 11:15:00 |

## 🔐 Security

- API keys stored in AWS Secrets Manager
- IAM roles for access control
- S3 encryption enabled
- Audit logging via CloudWatch
- No credentials in code

## 💰 Cost Estimate

- **AWS Lambda**: ~$0.20 per million requests (1M free/month)
- **S3 Storage**: Minimal (~$0.023/GB)
- **OpenAI API**: ~$0.01-0.03 per request

**Total**: <$1/month for typical use

## 🔄 Workflow

```
1. User describes transaction to ChatGPT
       ↓
2. GPT-5.2 extracts details using function calling
       ↓
3. Lambda function validates inputs
       ↓
4. Excel file fetched from S3 (or created if new)
       ↓
5. Transaction added with formatted details
       ↓
6. Excel saved back to S3
       ↓
7. Confirmation sent to user with Transaction ID
```

## 📝 API Endpoint

### Record Transaction
```bash
POST /api/transaction

{
  "action": "record_transaction",
  "beneficiary": "John Doe",
  "date": "2024-02-08",
  "amount": 1000,
  "purpose": "Payment for services"
}
```

**Response**:
```json
{
  "success": true,
  "transaction_id": "A1B2C3D4",
  "details": {
    "beneficiary": "John Doe",
    "date": "2024-02-08",
    "amount": 1000,
    "purpose": "Payment for services"
  }
}
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_agent.py
```

Tests include:
- Transaction recording
- Input validation
- ChatGPT conversation flow
- Error handling

## 🐛 Troubleshooting

### S3 Access Error
- Verify bucket name matches environment variable
- Check IAM permissions
- Enable S3 versioning

### OpenAI API Errors
- Verify API key is correct
- Check GPT-4 access (requires paid account)
- Monitor rate limits

### Module Import Errors
```bash
pip install -r requirements.txt
```

## 🔗 Integration Methods

## 📝 API Endpoint

### Record Transaction

- [ ] Multi-user support
- [ ] Transaction categories
- [ ] Monthly reports
- [ ] Real-time notifications
- [ ] Expense analytics
- [ ] Integration with accounting software
- [ ] Mobile app
- [ ] Voice input

## 📄 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please submit issues and pull requests.

## 📞 Support

For issues, questions, or deployment help:
1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review error logs in CloudWatch
3. Test locally with `test_agent.py`

---

**Built with ❤️ using Python, AWS, and OpenAI**
