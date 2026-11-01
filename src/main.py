import json
import sys
from datetime import datetime
from pathlib import Path
from src.jev_client import JevClient
from src.services import ClaimProcessingService
from src.config import Config
from src.logger import setup_logger


logger = setup_logger(__name__)


def get_sample_complaint() -> dict:
    """Provide a realistic insurance claim complaint"""
    return {
        "claim_id": "CLM-2026-001892",
        "customer_id": "CUST-445521",
        "complaint": (
            "I filed my car insurance claim three months ago after a collision on Highway 101. "
            "The incident report was filed on time, and I've provided all requested documentation. "
            "However, I haven't received any update on my claim status. When I call the support line, "
            "I'm put on hold for hours only to be told that my claim is still under review. "
            "This is unacceptable! I have medical bills piling up, and my car is still unfixed. "
            "I need someone in management to review this immediately. This is the worst customer "
            "service experience I've ever had with your company. I'm very frustrated and disappointed."
        )
    }


def process_complaint() -> None:
    """Main function to process an insurance complaint using Jev"""

    logger.info("=" * 80)
    logger.info("Starting Insurance Claim Complaint Processing with Jev")
    logger.info(f"Environment: {Config.ENVIRONMENT}")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 80)

    try:
        # Initialize clients and services
        jev_client = JevClient()
        service = ClaimProcessingService(jev_client)

        # Get sample complaint
        sample = get_sample_complaint()
        logger.info(f"\nProcessing Claim ID: {sample['claim_id']}")
        logger.info(f"Customer ID: {sample['customer_id']}")

        # Process the claim
        response = service.process_claim(
            claim_id=sample["claim_id"],
            customer_message=sample["complaint"],
            customer_id=sample["customer_id"]
        )

        # Display results
        print("\n" + "=" * 80)
        print("CLAIM CATEGORIZATION RESULTS")
        print("=" * 80)
        print(f"\nClaim ID: {response.claim_id}")
        print(f"\n📋 NOUL (Nature of Claim): {response.noul.value}")
        print(f"   Description: {_get_noul_description(response.noul)}")

        print(f"\n✅ CHOICE (Recommended Action): {response.choice.value}")
        print(f"   Description: {_get_choice_description(response.choice)}")

        print(f"\n📊 SCORE (Metrics):")
        print(f"   • Legitimacy: {response.score['legitimacy']}/100")
        print(f"   • Urgency: {response.score['urgency']}/100")
        print(f"   • Risk: {response.score['risk']}/100")

        print(f"\n🎯 Confidence: {response.confidence}%")
        print(f"\n📝 Reasoning:\n   {response.reasoning}")
        print(f"\n💬 Suggested Response to Customer:\n   {response.suggested_message}")

        print("\n" + "=" * 80)
        print("JSON OUTPUT")
        print("=" * 80)
        print(json.dumps(response.model_dump(), indent=2))

        print("\n✅ Results saved successfully!")
        logger.info("Claim processing completed successfully")

    except Exception as e:
        logger.error(f"Error processing complaint: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


def _get_noul_description(noul) -> str:
    """Get description for Noul type"""
    descriptions = {
        "claim_inquiry": "Customer is asking for information/status",
        "claim_complaint": "Customer has a complaint about service",
        "claim_dispute": "Customer disputes the claim decision",
        "claim_escalation": "Customer demands immediate escalation",
        "unknown": "Claim nature could not be determined"
    }
    return descriptions.get(noul.value, "Unknown")


def _get_choice_description(choice) -> str:
    """Get description for Choice type"""
    descriptions = {
        "auto_approve": "Automatically approve the claim",
        "manual_review": "Send to human agent for review",
        "reject": "Deny the claim with explanation",
        "escalate_to_supervisor": "Escalate to management immediately",
        "request_more_info": "Ask customer for additional information"
    }
    return descriptions.get(choice.value, "Unknown")


if __name__ == "__main__":
    process_complaint()
