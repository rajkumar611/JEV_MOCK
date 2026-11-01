from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class NoulType(str, Enum):
    """Noul represents the nature/type of the claim"""
    CLAIM_INQUIRY = "claim_inquiry"
    CLAIM_COMPLAINT = "claim_complaint"
    CLAIM_DISPUTE = "claim_dispute"
    CLAIM_ESCALATION = "claim_escalation"
    UNKNOWN = "unknown"


class ChoiceType(str, Enum):
    """Choice represents the recommended action"""
    AUTO_APPROVE = "auto_approve"
    MANUAL_REVIEW = "manual_review"
    REJECT = "reject"
    ESCALATE_TO_SUPERVISOR = "escalate_to_supervisor"
    REQUEST_MORE_INFO = "request_more_info"


@dataclass
class Score:
    """Score represents the confidence/severity metrics"""
    legitimacy: float = Field(ge=0, le=100)  # 0-100: How legitimate the complaint is
    urgency: float = Field(ge=0, le=100)     # 0-100: How urgent the claim is
    risk: float = Field(ge=0, le=100)        # 0-100: Risk level of approval


class ClaimRequest(BaseModel):
    """Request model for Jev categorization"""
    claim_id: str
    customer_message: str
    claim_type: Optional[str] = None
    customer_id: str


class ClaimResponse(BaseModel):
    """Response model from Jev categorization"""
    claim_id: str
    noul: NoulType = Field(description="Nature of the claim")
    choice: ChoiceType = Field(description="Recommended action")
    score: dict = Field(description="Score metrics (legitimacy, urgency, risk)")
    confidence: float = Field(ge=0, le=100, description="Overall confidence in categorization")
    reasoning: str = Field(description="Explanation of the categorization")
    suggested_message: Optional[str] = Field(None, description="Suggested response to customer")


class JevError(Exception):
    """Base exception for Jev-related errors"""
    pass


class JevAPIError(JevError):
    """Exception for Jev API errors"""
    pass
