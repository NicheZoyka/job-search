"""Constants shared across modules."""
import os

DEFAULT_MODEL = os.environ.get("CVM_MODEL", "claude-sonnet-5-5")
API_URL = "https://api.anthropic.com/v1/messages"
PRIORITIES = ["Critical", "High", "Medium", "Low"]
WEIGHTS = {"Critical": 5, "High": 3, "Medium": 2, "Low": 1}
SYMBOL = {"Yes": "✔", "Partial": "~", "No": "✘"}
