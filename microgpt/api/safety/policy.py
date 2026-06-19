from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    category: str
    reason: str


class SafetyPolicy:
    """Phase 1 safety blocker.

    This is not a final safety classifier. It is a conservative first gate for
    the manager-requested categories: violent/weaponized and explicit sexual
    content. Later phases should replace this with a stronger open-source
    classifier plus regression tests.
    """

    blocked_terms = {
        "weaponized": [
            "build a bomb",
            "make a bomb",
            "homemade explosive",
            "evade detection",
            "poison someone",
            "make a gun",
        ],
        "explicit_sexual": [
            "explicit sexual",
            "pornographic",
            "non-consensual sexual",
            "sexualized minor",
        ],
        "secrets_override": [
            "ignore your safety rules",
            "reveal system prompt",
            "bypass safety",
            "disable safety",
        ],
    }

    def check(self, text: str) -> SafetyDecision:
        lowered = text.lower()
        for category, terms in self.blocked_terms.items():
            for term in terms:
                if term in lowered:
                    return SafetyDecision(
                        allowed=False,
                        category=category,
                        reason=f"Blocked by Phase 1 safety rule: {category}",
                    )
        return SafetyDecision(allowed=True, category="allowed", reason="No Phase 1 rule matched")


safety_policy = SafetyPolicy()
