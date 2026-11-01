# Jev Insurance Claim Categorization System

An enterprise-grade Python application demonstrating the use of Jev AI for categorizing insurance claim complaints using the Noul, Choice, and Score primitives.

## Project Structure

```
JEV/
├── src/
│   ├── main.py              # Entry point with sample complaint
│   ├── jev_client.py        # Jev AI client (mock implementation)
│   ├── services.py          # Business logic service layer
│   ├── models.py            # Data models and enums
│   ├── config.py            # Configuration management
│   └── logger.py            # Logging setup
├── results/                 # Output directory for results
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## What is Jev?

Jev is an AI framework for intelligent categorization and routing. This project uses Jev's three core primitives:

### 1. **Noul** (Nature of the Claim)
Represents the fundamental type/nature of the customer's message:
- `claim_inquiry`: Information request about claim status
- `claim_complaint`: Customer complaint about service
- `claim_dispute`: Customer disputes the claim decision
- `claim_escalation`: Customer demands immediate escalation
- `unknown`: Unable to determine

### 2. **Choice** (Recommended Action)
Represents the recommended next action:
- `auto_approve`: Automatically approve the claim
- `manual_review`: Route to human agent for review
- `reject`: Deny the claim with explanation
- `escalate_to_supervisor`: Escalate to management
- `request_more_info`: Ask customer for more information

### 3. **Score** (Metrics)
Quantitative metrics for decision-making:
- **Legitimacy** (0-100): How valid/legitimate the complaint is
- **Urgency** (0-100): How time-sensitive the claim is
- **Risk** (0-100): Risk level if approved

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
cd JEV
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file (optional):
```bash
cp .env.example .env
```

4. Configure environment variables if needed:
```
JEV_API_ENDPOINT=http://localhost:8000/api/v1/jev
JEV_API_KEY=your-api-key-here
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## Running the Application

```bash
python -m src.main
```

### Expected Output

The application will:
1. Process a hardcoded insurance claim complaint
2. Send it to Jev for categorization
3. Display results in a formatted table
4. Output results as JSON
5. Save results to `results/` directory
6. Create logs in `logs/` directory

### Sample Output

```
================================================================================
CLAIM CATEGORIZATION RESULTS
================================================================================

Claim ID: CLM-2026-001892

📋 NOUL (Nature of Claim): claim_escalation
   Description: Customer demands immediate escalation

✅ CHOICE (Recommended Action): escalate_to_supervisor
   Description: Escalate to management immediately

📊 SCORE (Metrics):
   • Legitimacy: 75/100
   • Urgency: 90/100
   • Risk: 60/100

🎯 Confidence: 82.5%

📝 Reasoning:
   Claim categorized as claim_escalation. Recommended action: escalate_to_supervisor. 
   Legitimacy score: 75/100, Urgency: 90/100, Risk level: 60/100.

💬 Suggested Response to Customer:
   Your case is being escalated to a supervisor for immediate attention.

================================================================================
JSON OUTPUT
================================================================================
{
  "claim_id": "CLM-2026-001892",
  "noul": "claim_escalation",
  "choice": "escalate_to_supervisor",
  "score": {
    "legitimacy": 75,
    "urgency": 90,
    "risk": 60
  },
  "confidence": 82.5,
  "reasoning": "...",
  "suggested_message": "..."
}
```

## Files Overview

### `src/models.py`
Defines Pydantic models for:
- **NoulType**: Enum for claim nature
- **ChoiceType**: Enum for recommended actions
- **Score**: Dataclass for metrics
- **ClaimRequest**: Request model
- **ClaimResponse**: Response model

### `src/jev_client.py`
Mock Jev AI client that:
- Accepts claim requests
- Uses heuristic logic to categorize (mock)
- Returns structured responses with all three primitives
- Ready to integrate with real Jev API

### `src/services.py`
Business logic layer:
- Processes claims through Jev
- Saves results to JSON files
- Manages claim workflow

### `src/config.py`
Configuration management:
- Loads environment variables
- Provides centralized config access
- Supports multiple environments

### `src/logger.py`
Logging setup:
- Console logging
- File logging with rotation
- Structured log formatting

### `src/main.py`
Entry point:
- Contains sample complaint
- Orchestrates the processing flow
- Formats and displays results

## Extending This Project

### To Use Real Jev API

1. Get API credentials from Typesafe
2. Update `.env` file with real endpoint and API key
3. Implement `_api_categorize()` method in `jev_client.py`
4. Change `self.is_mock = False`

### To Add Different Complaints

Modify `get_sample_complaint()` in `src/main.py`:

```python
def get_sample_complaint() -> dict:
    return {
        "claim_id": "CLM-2026-002000",
        "customer_id": "CUST-445522",
        "complaint": "Your custom complaint text here..."
    }
```

### To Add Database Integration

Create a new service in `src/database.py`:
```python
class ClaimDatabase:
    def save_claim(self, response: ClaimResponse):
        # Save to database
        pass
```

## Logging

Logs are stored in the `logs/` directory:
- **Console**: INFO level and above
- **File**: Full details with line numbers
- **Rotation**: 10MB per file, 5 backups

View logs:
```bash
cat logs/jev_claim_processor.log
```

## Error Handling

The application includes comprehensive error handling:
- Validation of inputs via Pydantic
- Custom exception classes
- Detailed logging of errors
- Graceful error messages

## Best Practices Implemented

✅ **Separation of Concerns**: Client, Service, and Models layers  
✅ **Type Safety**: Type hints throughout  
✅ **Configuration Management**: Environment-based config  
✅ **Logging**: Comprehensive logging setup  
✅ **Error Handling**: Custom exceptions and validation  
✅ **Scalability**: Ready for real API integration  
✅ **Documentation**: Code comments and this README  
✅ **Pydantic Models**: Data validation and serialization  

## Next Steps

1. Get Jev API credentials from Typesafe
2. Implement real API integration in `jev_client.py`
3. Add database persistence
4. Create API endpoint wrapper
5. Add unit tests
6. Deploy to production

## Support

For issues or questions about Jev, refer to:
- [Typesafe Documentation](https://typesafe.ai/)
- [Jev API Reference](https://typesafe.ai/jev/api)

---

**Created**: 2026-11-01  
**Version**: 1.0.0  
**License**: MIT
