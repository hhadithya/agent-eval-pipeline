"""Verfiy ADC, the vertex project and the model work"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))   # import config

from google import genai 
from google.genai import types

import config

client = genai.Client(
    vertexai=True, project=config.GCP_PROJECT, location=config.GCP_LOCATION
)

response = client.models.generate_content(
    model=config.MODEL,
    contents="Reply with exactly: pipeline ready",
    config=types.GenerateContentConfig(max_output_tokens=64)
)

candidate = response.candidates[0]
print("finish_reason:", candidate.finish_reason)

for part in candidate.content.parts:
    if part.text:
        print("text", part.text)

usage = response.usage_metadata
thoughts = getattr(usage, "thoughts_token_count", None) or 0
cost = config.estimate_cost(usage.prompt_token_count, usage.candidates_token_count, thoughts)

print(
    f"tokens: in={usage.prompt_token_count} out={usage.candidates_token_count} "
    f"thoughts={thoughts} cost${cost: .5f}"
)