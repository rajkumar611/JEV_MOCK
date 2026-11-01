import json
from datetime import datetime
from pathlib import Path
from src.models import ClaimRequest, ClaimResponse
from src.jev_client import JevClient
from src.logger import setup_logger


logger = setup_logger(__name__)


class ClaimProcessingService:
    """Service for processing insurance claims with Jev categorization"""

    def __init__(self, jev_client: JevClient):
        self.jev_client = jev_client
        self.results_dir = Path(__file__).parent.parent / "results"
        self.results_dir.mkdir(exist_ok=True)
        logger.info("Initialized ClaimProcessingService")

    def process_claim(self, claim_id: str, customer_message: str, customer_id: str) -> ClaimResponse:
        """
        Process an insurance claim through Jev categorization.

        Args:
            claim_id: Unique claim identifier
            customer_message: Customer's complaint/inquiry
            customer_id: Customer identifier

        Returns:
            ClaimResponse with categorization results
        """
        logger.info(f"Processing claim {claim_id} for customer {customer_id}")

        # Create request
        request = ClaimRequest(
            claim_id=claim_id,
            customer_message=customer_message,
            customer_id=customer_id
        )

        # Categorize with Jev
        response = self.jev_client.categorize_claim(request)

        # Save results
        self._save_results(claim_id, request, response)

        return response

    def _save_results(self, claim_id: str, request: ClaimRequest, response: ClaimResponse) -> None:
        """Save processing results to JSON file"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "claim_id": claim_id,
            "request": {
                "claim_id": request.claim_id,
                "customer_id": request.customer_id,
                "customer_message": request.customer_message
            },
            "response": response.model_dump()
        }

        output_file = self.results_dir / f"claim_{claim_id}.json"

        try:
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2)
            logger.info(f"Saved results to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save results: {str(e)}")

    def get_results(self, claim_id: str) -> dict:
        """Retrieve saved results for a claim"""
        output_file = self.results_dir / f"claim_{claim_id}.json"

        if not output_file.exists():
            logger.warning(f"Results file not found for claim {claim_id}")
            return None

        try:
            with open(output_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read results: {str(e)}")
            return None
