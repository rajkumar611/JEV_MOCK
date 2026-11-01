# Quick Start Guide

## What Was Built?

An **enterprise-grade Python application** that demonstrates Jev AI categorization of insurance claim complaints using three key primitives:

### 🎯 The Three Jev Primitives

1. **Noul** (Nature/Type)
   - Categorizes what kind of message it is
   - Example: `claim_complaint`, `claim_escalation`, `claim_inquiry`

2. **Choice** (Recommended Action)
   - Suggests what to do with the claim
   - Example: `manual_review`, `escalate_to_supervisor`, `auto_approve`

3. **Score** (Metrics)
   - Quantifies key dimensions
   - Legitimacy (0-100): How valid is the complaint?
   - Urgency (0-100): How time-sensitive is it?
   - Risk (0-100): What's the risk if we approve?

---

## Project Structure

```
JEV/
├── src/
│   ├── main.py              ← Entry point (run this!)
│   ├── jev_client.py        ← Mock Jev AI client
│   ├── services.py          ← Business logic
│   ├── models.py            ← Data models
│   ├── config.py            ← Configuration
│   └── logger.py            ← Logging setup
├── results/                 ← Output JSON results
├── logs/                    ← Application logs
├── README.md                ← Full documentation
└── requirements.txt         ← Dependencies
```

---

## Run the Application

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Program
```bash
python -m src.main
```

### Step 3: Check Results

**Console Output**: Shows categorization results with all three primitives

**Results File**: `results/claim_CLM-2026-001892.json`
```json
{
  "claim_id": "CLM-2026-001892",
  "noul": "claim_complaint",
  "choice": "manual_review",
  "score": {
    "legitimacy": 75,
    "urgency": 70,
    "risk": 40
  },
  "confidence": 100.0,
  "reasoning": "...",
  "suggested_message": "..."
}
```

**Logs**: `logs/jev_claim_processor.log`

---

## Sample Output

```
================================================================================
CLAIM CATEGORIZATION RESULTS
================================================================================

Claim ID: CLM-2026-001892

📋 NOUL (Nature of Claim): claim_complaint
   Description: Customer has a complaint about service

✅ CHOICE (Recommended Action): manual_review
   Description: Send to human agent for review

📊 SCORE (Metrics):
   • Legitimacy: 75/100
   • Urgency: 70/100
   • Risk: 40/100

🎯 Confidence: 100.0%

💬 Suggested Response to Customer:
   Your claim requires manual review. We'll contact you shortly.
```

---

## Enterprise Features Included

✅ **Type Safety**: Full type hints with Pydantic validation  
✅ **Logging**: Console + rotating file logs with full context  
✅ **Configuration**: Environment-based settings (.env)  
✅ **Error Handling**: Custom exceptions and comprehensive error messages  
✅ **Separation of Concerns**: Client → Service → Models layers  
✅ **Mock Implementation**: Ready to swap with real Jev API  
✅ **JSON Output**: Structured results for downstream processing  
✅ **Documentation**: Comprehensive README and inline comments  

---

## Next Steps

### 1. Customize the Complaint
Edit `src/main.py` - `get_sample_complaint()`:
```python
def get_sample_complaint() -> dict:
    return {
        "claim_id": "CLM-2026-002000",
        "complaint": "Your custom complaint here..."
    }
```

### 2. Integrate Real Jev API
Get API credentials from Typesafe, then:
1. Update `.env` file with real endpoint
2. Implement `_api_categorize()` in `src/jev_client.py`
3. Set `self.is_mock = False`

### 3. Add Database Integration
Create `src/database.py` for persistence

### 4. Add Unit Tests
Create `tests/` directory with test cases

---

## Architecture Diagram

```
┌─────────────────────┐
│   main.py           │  Entry point with sample complaint
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ ClaimProcessing     │  Service layer - orchestrates flow
│ Service             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   JevClient         │  AI client - calls Jev (mock for now)
│  (mock / real API)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Models            │  Data structures:
│ (ClaimRequest,      │  - NoulType, ChoiceType, Score
│  ClaimResponse)     │  - Pydantic validation
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Results JSON +     │  Structured output
│  Logs               │
└─────────────────────┘
```

---

## Key Files at a Glance

| File | Purpose |
|------|---------|
| `src/main.py` | Entry point, orchestration |
| `src/jev_client.py` | Jev integration (mock) |
| `src/services.py` | Business logic, file I/O |
| `src/models.py` | Pydantic models, enums |
| `src/config.py` | Configuration management |
| `src/logger.py` | Logging infrastructure |

---

## Questions?

1. **How do I change the complaint?** → Edit `get_sample_complaint()` in `main.py`
2. **How do I use the real Jev API?** → See README.md "Extending This Project"
3. **Where are results saved?** → `results/` and `logs/` directories
4. **How do I understand the scores?** → See README.md "Jev Primitives" section

---

**Ready to extend this?** Check out the full README.md for integration instructions!
