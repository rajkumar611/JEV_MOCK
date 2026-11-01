import json
from typing import Optional
from src.models import (
    ClaimRequest, ClaimResponse, NoulType, ChoiceType, JevAPIError
)
from src.config import Config
from src.logger import setup_logger


logger = setup_logger(__name__)


class JevClient:
    """Mock Jev AI Client for insurance claim categorization"""

    def __init__(self, api_endpoint: Optional[str] = None, api_key: Optional[str] = None):
        self.api_endpoint = api_endpoint or Config.JEV_API_ENDPOINT
        self.api_key = api_key or Config.JEV_API_KEY
        self.is_mock = True  # Currently using mock implementation
        logger.info(f"Initialized JevClient with endpoint: {self.api_endpoint}")

    def categorize_claim(self, request: ClaimRequest) -> ClaimResponse:
        """
        Categorize an insurance claim using Jev primitives.

        Args:
            request: ClaimRequest containing claim details

        Returns:
            ClaimResponse with categorization

        Raises:
            JevAPIError: If categorization fails
        """
        try:
            logger.info(f"Categorizing claim: {request.claim_id}")

            if self.is_mock:
                response = self._mock_categorize(request)
            else:
                response = self._api_categorize(request)

            logger.info(f"Successfully categorized claim: {request.claim_id}")
            return response

        except Exception as e:
            logger.error(f"Error categorizing claim {request.claim_id}: {str(e)}")
            raise JevAPIError(f"Failed to categorize claim: {str(e)}")

    def _mock_categorize(self, request: ClaimRequest) -> ClaimResponse:
        """Mock implementation of Jev categorization"""
        logger.debug(f"Using mock categorization for claim: {request.claim_id}")

        message = request.customer_message.lower()

        # Simple heuristic-based categorization (mock logic)
        noul = self._determine_noul(message)
        choice = self._determine_choice(message, noul)
        score = self._calculate_scores(message, noul)
        confidence = self._calculate_confidence(message)
        reasoning = self._generate_reasoning(noul, choice, score)
        suggested_message = self._generate_suggested_message(choice)

        response = ClaimResponse(
            claim_id=request.claim_id,
            noul=noul,
            choice=choice,
            score=score,
            confidence=confidence,
            reasoning=reasoning,
            suggested_message=suggested_message
        )

        return response

    def _determine_noul(self, message: str) -> NoulType:
        """Determine the nature (Noul) of the claim"""
        keywords = {
            NoulType.CLAIM_ESCALATION: ["urgent", "escalate", "supervisor", "manager", "unfair"],
            NoulType.CLAIM_DISPUTE: ["wrong", "incorrect", "disagree", "dispute", "deny"],
            NoulType.CLAIM_COMPLAINT: ["complaint", "disappointed", "poor", "service", "bad"],
            NoulType.CLAIM_INQUIRY: ["question", "when", "status", "update", "where"],
        }

        for noul_type, kws in keywords.items():
            if any(kw in message for kw in kws):
                return noul_type

        return NoulType.UNKNOWN

    def _determine_choice(self, message: str, noul: NoulType) -> ChoiceType:
        """Determine the recommended action (Choice)"""
        if noul == NoulType.CLAIM_ESCALATION:
            return ChoiceType.ESCALATE_TO_SUPERVISOR
        elif noul == NoulType.CLAIM_DISPUTE:
            return ChoiceType.MANUAL_REVIEW
        elif noul == NoulType.CLAIM_COMPLAINT:
            return ChoiceType.MANUAL_REVIEW
        elif noul == NoulType.CLAIM_INQUIRY:
            if "approved" in message or "yes" in message:
                return ChoiceType.AUTO_APPROVE
            return ChoiceType.REQUEST_MORE_INFO
        else:
            return ChoiceType.MANUAL_REVIEW

    def _calculate_scores(self, message: str, noul: NoulType) -> dict:
        """Calculate score metrics (legitimacy, urgency, risk)"""
        # Simplified scoring logic
        legitimacy = 75  # Default legitimacy
        if noul == NoulType.CLAIM_DISPUTE:
            legitimacy = 60
        elif noul == NoulType.CLAIM_INQUIRY:
            legitimacy = 85

        urgency = 50  # Default urgency
        if noul == NoulType.CLAIM_ESCALATION:
            urgency = 90
        elif noul == NoulType.CLAIM_COMPLAINT:
            urgency = 70

        risk = 40  # Default risk
        if "deny" in message.lower():
            risk = 70
        elif noul == NoulType.CLAIM_ESCALATION:
            risk = 60

        return {
            "legitimacy": legitimacy,
            "urgency": urgency,
            "risk": risk
        }

    def _calculate_confidence(self, message: str) -> float:
        """Calculate overall confidence in categorization"""
        # Confidence based on message clarity
        words = message.split()
        confidence = min(100, 60 + len(words) * 0.5)  # More details = higher confidence
        return round(confidence, 2)

    def _generate_reasoning(self, noul: NoulType, choice: ChoiceType, score: dict) -> str:
        """Generate explanation of categorization"""
        return (
            f"Claim categorized as {noul.value}. "
            f"Recommended action: {choice.value}. "
            f"Legitimacy score: {score['legitimacy']}/100, "
            f"Urgency: {score['urgency']}/100, "
            f"Risk level: {score['risk']}/100."
        )

    def _generate_suggested_message(self, choice: ChoiceType) -> str:
        """Generate suggested response to customer"""
        messages = {
            ChoiceType.AUTO_APPROVE: "Your claim has been approved. Thank you for your patience.",
            ChoiceType.MANUAL_REVIEW: "Your claim requires manual review. We'll contact you shortly.",
            ChoiceType.REJECT: "Unfortunately, your claim cannot be approved. Please review the denial letter.",
            ChoiceType.ESCALATE_TO_SUPERVISOR: "Your case is being escalated to a supervisor for immediate attention.",
            ChoiceType.REQUEST_MORE_INFO: "We need additional information to process your claim. Please contact us.",
        }
        return messages.get(choice, "We're reviewing your claim.")

    def _api_categorize(self, request: ClaimRequest) -> ClaimResponse:
        """Real API implementation (placeholder for future use)"""
        raise NotImplementedError("Real API implementation coming soon")
