"""
APEX PSI SDK
Cryptographic verification for Python
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


DEFAULT_API_BASE = "https://sovereign-ai.services/api"


@dataclass
class Receipt:
    """Cryptographic receipt from sealing content"""
    hash: str
    signature: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None
    content: Optional[str] = None


@dataclass
class VerificationResult:
    """Result of verifying a receipt"""
    valid: bool
    details: Dict[str, Any]


@dataclass
class AnchorProof:
    """Proof of Bitcoin anchoring via OpenTimestamps"""
    receipt_hash: str
    bitcoin_tx_id: Optional[str] = None
    ots_file: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class CitationResult:
    """Citation generated from a receipt"""
    citation: str
    format: str


@dataclass
class AuditFinding:
    """Single finding from an audit"""
    type: str
    severity: str
    message: str
    receipt_index: Optional[int] = None


@dataclass
class AuditReport:
    """Report from auditing a chain of receipts"""
    total_receipts: int
    findings: List[AuditFinding]
    valid: bool


class ApexPSI:
    """APEX PSI client for cryptographic verification"""
    
    def __init__(self, api_base: str = DEFAULT_API_BASE, api_key: Optional[str] = None):
        self.api_base = api_base
        self.api_key = api_key
    
    def _api_call(self, endpoint: str, method: str = "GET", json: Optional[Dict] = None) -> Dict:
        """Make an API call to APEX PSI"""
        url = f"{self.api_base}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        response = requests.request(method, url, headers=headers, json=json)
        response.raise_for_status()
        
        return response.json()
    
    def seal(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Receipt:
        """
        Seal content with a cryptographic receipt
        
        Args:
            content: The content to seal
            metadata: Optional metadata to include in the receipt
        
        Returns:
            Receipt object with hash, signature, and timestamp
        """
        result = self._api_call("/seal", "POST", {
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        return Receipt(
            hash=result["hash"],
            signature=result["signature"],
            timestamp=result["timestamp"],
            metadata=result.get("metadata"),
            content=result.get("content"),
        )
    
    def verify(self, receipt: Receipt, content: Optional[str] = None) -> VerificationResult:
        """
        Verify a receipt is authentic
        
        Args:
            receipt: The receipt to verify
            content: Optional content to verify against the receipt
        
        Returns:
            VerificationResult with valid flag and details
        """
        receipt_dict = {
            "hash": receipt.hash,
            "signature": receipt.signature,
            "timestamp": receipt.timestamp,
            "metadata": receipt.metadata,
        }
        
        result = self._api_call("/verify", "POST", {
            "receipt": receipt_dict,
            "content": content,
        })
        
        return VerificationResult(
            valid=result["valid"],
            details=result.get("details", {}),
        )
    
    def anchor(self, receipt: Receipt) -> AnchorProof:
        """
        Anchor a receipt to Bitcoin via OpenTimestamps
        
        Args:
            receipt: The receipt to anchor
        
        Returns:
            AnchorProof with Bitcoin transaction data
        """
        receipt_dict = {
            "hash": receipt.hash,
            "signature": receipt.signature,
            "timestamp": receipt.timestamp,
        }
        
        result = self._api_call("/anchor", "POST", {
            "receipt": receipt_dict,
        })
        
        return AnchorProof(
            receipt_hash=result["receipt_hash"],
            bitcoin_tx_id=result.get("bitcoin_tx_id"),
            ots_file=result.get("ots_file"),
            timestamp=result.get("timestamp"),
        )
    
    def cite(self, receipt: Receipt, format: str = "apa") -> CitationResult:
        """
        Generate a citation for a receipt
        
        Args:
            receipt: The receipt to cite
            format: Citation format (apa, bibtex, mla)
        
        Returns:
            CitationResult with citation string and format
        """
        receipt_dict = {
            "hash": receipt.hash,
            "signature": receipt.signature,
            "timestamp": receipt.timestamp,
            "metadata": receipt.metadata,
        }
        
        result = self._api_call("/cite", "POST", {
            "receipt": receipt_dict,
            "format": format,
        })
        
        return CitationResult(
            citation=result["citation"],
            format=result["format"],
        )
    
    def audit(self, receipts: List[Receipt], check_anchoring: bool = False) -> AuditReport:
        """
        Audit a chain of receipts
        
        Args:
            receipts: List of receipts to audit
            check_anchoring: Whether to verify Bitcoin anchoring
        
        Returns:
            AuditReport with findings and validity
        """
        receipts_list = [
            {
                "hash": r.hash,
                "signature": r.signature,
                "timestamp": r.timestamp,
                "metadata": r.metadata,
            }
            for r in receipts
        ]
        
        result = self._api_call("/audit", "POST", {
            "receipts": receipts_list,
            "check_anchoring": check_anchoring,
        })
        
        findings = [
            AuditFinding(
                type=f["type"],
                severity=f["severity"],
                message=f["message"],
                receipt_index=f.get("receipt_index"),
            )
            for f in result.get("findings", [])
        ]
        
        return AuditReport(
            total_receipts=result["total_receipts"],
            findings=findings,
            valid=result["valid"],
        )


# Convenience functions
def seal(content: str, metadata: Optional[Dict[str, Any]] = None, **kwargs) -> Receipt:
    """Convenience function to seal content"""
    client = ApexPSI(**kwargs)
    return client.seal(content, metadata)


def verify(receipt: Receipt, content: Optional[str] = None, **kwargs) -> VerificationResult:
    """Convenience function to verify a receipt"""
    client = ApexPSI(**kwargs)
    return client.verify(receipt, content)


def anchor(receipt: Receipt, **kwargs) -> AnchorProof:
    """Convenience function to anchor a receipt"""
    client = ApexPSI(**kwargs)
    return client.anchor(receipt)


def cite(receipt: Receipt, format: str = "apa", **kwargs) -> CitationResult:
    """Convenience function to cite a receipt"""
    client = ApexPSI(**kwargs)
    return client.cite(receipt, format)


def audit(receipts: List[Receipt], check_anchoring: bool = False, **kwargs) -> AuditReport:
    """Convenience function to audit receipts"""
    client = ApexPSI(**kwargs)
    return client.audit(receipts, check_anchoring)
