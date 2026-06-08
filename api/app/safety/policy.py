from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    category: str
    reason: str


# MVP guardrail: intentionally simple and conservative.
# Replace or augment with open-source classifiers, prompt-injection checks,
# output moderation, red-team tests, and human review before public release.
VIOLENCE_TERMS = {
    "kill", "murder", "stab", "shoot", "bomb", "weaponize", "assassinate",
    "torture", "massacre", "harm someone", "make explosives"
}

SEXUAL_TERMS = {
    "explicit sex", "porn", "nude", "erotic", "sexual image", "deepfake nude",
    "non-consensual sexual", "minor sexual"
}


def evaluate_prompt(text: str) -> SafetyDecision:
    normalized = text.lower()

    if any(term in normalized for term in SEXUAL_TERMS):
        return SafetyDecision(
            allowed=False,
            category="sexual_content",
            reason="The request appears to ask for sexual or explicit generated content, which is blocked for this project.",
        )

    if any(term in normalized for term in VIOLENCE_TERMS):
        return SafetyDecision(
            allowed=False,
            category="violent_content",
            reason="The request appears to ask for violent or harmful generated content, which is blocked for this project.",
        )

    return SafetyDecision(allowed=True, category="safe", reason="No blocked category detected by MVP policy.")
