"""
Central configuration. Every experimental variable stays here.

No API key -> aauthentication is Application Default Credentials(ADC)
`gcloud auth application-default login`

"""

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
TRACES_DIR = PROJECT_ROOT / "traces"
CASES_DIR = PROJECT_ROOT / "evals" / "cases"
CASSETTE_DIR = PROJECT_ROOT / "cassettes"  

"""
In Python testing, a cassette is a flat file (usually in YAML or JSON format) 
that stores recorded HTTP requests and responses

"""

# Vertex AI project - aiplatform.googleapis.com
GCP_PROJECT = "eval-pipeline-gapstars"
GCP_LOCATION = "us-central1"

# Model config
MODEL = "gemini-2.5-pro"
THINKING_BUDGET = 2048    # tokens reserved for reasoning; 0 disables thinking
MAX_OUTPUT_TOKENS = 4096

# Agent behaviour 
MAX_TURNS = 8             # hard ceiling on loop iterations
REFUND_LIMIT = 50.00      # the policy boundary 

# Evaluation
RUNS_PER_CASE = 5     # > 1 is the entire point

# Pricing (USD per million tokens, gemini-2.5-pro, prompts <=200k)
# Thinking tokens are billed as the output tokens
PRICE_INPUT_PER_MTOK = 1.25
PRICE_OUTPUT_PER_MTOK = 10.00

def estimate_cost(input_tokens: int, output_tokens: int, thought_tokens: int=0) -> float:
    """Convert token counts to dollars."""
    return (
        input_tokens / 1_000_000 * PRICE_INPUT_PER_MTOK
        + (output_tokens + thought_tokens) / 1_000_000 * PRICE_INPUT_PER_MTOK
    )
