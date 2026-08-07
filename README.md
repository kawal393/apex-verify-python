# apex-verify

APEX PSI SDK — Cryptographic verification for Python.

## Installation

```bash
pip install apex-verify
```

## Quick Start

```python
from apex_verify import seal, verify

# Seal content
receipt = seal("Important document", metadata={"author": "Alice"})
print(receipt.hash)

# Verify receipt
result = verify(receipt)
print(result.valid)  # True
```

## API

### Class-based usage

```python
from apex_verify import ApexPSI

client = ApexPSI(
    api_base="https://sovereign-ai.services/api",
    api_key="your-api-key",  # optional
)

# Seal
receipt = client.seal("Document content", metadata={"author": "Alice"})

# Verify
result = client.verify(receipt)

# Anchor to Bitcoin
anchor = client.anchor(receipt)

# Generate citation
citation = client.cite(receipt, format="apa")

# Audit chain
report = client.audit([receipt1, receipt2], check_anchoring=True)
```

### Convenience functions

```python
from apex_verify import seal, verify, anchor, cite, audit

receipt = seal("content", metadata={"key": "value"})
result = verify(receipt)
anchor = anchor(receipt)
citation = cite(receipt, format="apa")
report = audit([receipt1, receipt2])
```

## Configuration

```python
client = ApexPSI(
    api_base="https://sovereign-ai.services/api",  # default
    api_key="your-api-key",  # optional
)
```

## Links

- **Website:** https://sovereign-ai.services
- **Documentation:** https://sovereign-ai.services/mcp
- **MCP Server:** @apex/psi-mcp-server
- **GitHub:** https://github.com/apex-psi/sdk-python

## License

MIT
