import os
from dataclasses import dataclass


@dataclass(frozen=True)
class MaturityDecision:
    allowed: bool
    status: str
    reason: str


def check_maturity_gate() -> MaturityDecision:
    maturity = os.getenv("MICROGPT_PROJECT_MATURITY", "internal").lower()
    allow_public = os.getenv("MICROGPT_ALLOW_PUBLIC_ACCESS", "false").lower() == "true"

    if maturity in {"research", "internal", "alpha"} and not allow_public:
        return MaturityDecision(
            allowed=True,
            status=maturity,
            reason="Internal authenticated access is allowed; public access remains disabled until safety review.",
        )

    if maturity in {"beta", "public"} and allow_public:
        return MaturityDecision(
            allowed=True,
            status=maturity,
            reason="Public access is enabled by configuration after maturity review.",
        )

    return MaturityDecision(
        allowed=False,
        status=maturity,
        reason="Access blocked by maturity gate configuration.",
    )
