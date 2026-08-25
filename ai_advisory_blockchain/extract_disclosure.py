import os
import json
from disclosure_snippets import DISCLOSURE_SNIPPETS

def extract_signals(snippet: str) -> dict:
    """Extracts risk flags, hedging, and sentiment from disclosure text."""
    mock_llm_status = os.getenv("MOCK_LLM", "1")
    snippet_lower = snippet.lower()
    
    if mock_llm_status == "1" or mock_llm_status == "":
        # MOCK MODE: Rule-based extraction
        risk_flags = []
        
        # 1. Identify Risk Flags
        if "litigation" in snippet_lower:
            risk_flags.append("litigation")
        if "regulat" in snippet_lower: # Catches regulatory, regulator
            risk_flags.append("regulatory")
        if "customer" in snippet_lower:
            risk_flags.append("customer concentration")
            
        # 2. Detect Hedging
        hedging_keywords = ["assuming", "cautiously", "visibility"]
        hedging_detected = any(kw in snippet_lower for kw in hedging_keywords)
        
        # 3. Classify Sentiment
        if "confident" in snippet_lower or "approved" in snippet_lower:
            sentiment = "confident"
        elif hedging_detected:
            sentiment = "cautious"
        else:
            sentiment = "neutral"
            
        return {
            "risk_flags": risk_flags,
            "hedging_detected": hedging_detected,
            "sentiment": sentiment
        }
    else:
        # Note: If MOCK_LLM=0, implement the Groq API/LLM call logic here.
        return {"error": "LLM API not implemented in this baseline"}

if __name__ == "__main__":
    print(f"Initializing Disclosure Extraction... (MOCK_LLM = {os.getenv('MOCK_LLM', '1')})")
    
    for snippet in DISCLOSURE_SNIPPETS:
        print("\n" + "-"*60)
        print(f"TEXT: {snippet}")
        
        extracted_data = extract_signals(snippet)
        
        print("EXTRACTED SIGNALS:")
        print(json.dumps(extracted_data, indent=2))
