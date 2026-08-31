"""Rule extractor: convert natural-language descriptions into BidRule dicts
using the GitHub Models API (gpt-4o-mini via Azure OpenAI compatible endpoint).
"""

from __future__ import annotations

import json
import os

GITHUB_MODELS_BASE = "https://models.inference.ai.azure.com"
GITHUB_MODELS_MODEL = "gpt-4o-mini"

_SYSTEM_PROMPT = """\
You are a bridge bidding expert helping encode bidding rules as structured JSON.

You will receive a natural-language description of a bridge call, the call itself,
and the auction context pattern.  Respond with a single JSON object (no markdown
fences) representing a BidRule with these fields:

{
  "call": "<call string, e.g. 1H, 2NT, P, X>",
  "priority": <float, higher means this rule fires before lower-priority ones>,
  "shows": "<one-sentence description of what the call shows>",
  "requires": {
    "hcp": [<min>, <max>],           // optional; omit if not constrained
    "suits": {                        // optional suit-length constraints
      "H": [<min>, <max>],
      "S": [<min>, <max>],
      "D": [<min>, <max>],
      "C": [<min>, <max>]
    },
    "features": ["<feature_name>"]    // optional boolean features
  },
  "establishes": {                    // optional
    "forcing": "<non_forcing|one_round|invitational|game_forcing|sign_off>"
  },
  "alertable": <true|false>
}

Examples of feature names: "balanced", "stopper_C", "stopper_D", "stopper_H",
"stopper_S", "self_sufficient_S", "self_sufficient_H".

Suit-length arrays are [min_cards, max_cards] inclusive, e.g. [5, 13] means
at least 5 cards in that suit.

Keep priority between 1.0 and 100.0.  Higher values should be used for more
specific or exceptional rules.  Default is 10.0.

Return ONLY the JSON object, nothing else.
"""


async def extract_rule_from_text(
    description: str,
    call: str,
    context_pattern: str,
) -> dict:
    """Call GitHub Models (gpt-4o-mini) to extract a BidRule dict from natural language.

    Returns a BidRule-shaped dict or {"error": "..."} if the API is unavailable.
    """
    github_token = os.environ.get("GITHUB_TOKEN", "")
    if not github_token:
        return {"error": "GitHub Models not available: GITHUB_TOKEN is not set"}

    try:
        from openai import AsyncOpenAI
    except ImportError:
        return {"error": "GitHub Models not available: openai package is not installed"}

    client = AsyncOpenAI(base_url=GITHUB_MODELS_BASE, api_key=github_token)

    user_message = (
        f"Call: {call}\n"
        f"Auction context pattern: {context_pattern}\n"
        f"Description: {description}\n\n"
        "Return the BidRule JSON."
    )

    try:
        response = await client.chat.completions.create(
            model=GITHUB_MODELS_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.0,
            max_tokens=512,
        )
        raw = response.choices[0].message.content or ""
        raw = raw.strip()
        # Strip markdown fences if the model wraps the response.
        if raw.startswith("```"):
            lines = raw.split("\n")
            # Remove first and last fence lines.
            inner = [l for l in lines if not l.startswith("```")]
            raw = "\n".join(inner)
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        return {"error": f"Model returned non-JSON response: {exc}"}
    except Exception as exc:
        return {"error": f"GitHub Models API error: {exc}"}
