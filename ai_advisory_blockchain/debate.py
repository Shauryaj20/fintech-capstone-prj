import os
from stock_universe import STOCK_UNIVERSE

def run_debate(ticker):
    """Simulates a 3-agent debate for a given stock ticker."""
    mock_llm_status = os.getenv("MOCK_LLM", "1")
    
    if ticker not in STOCK_UNIVERSE:
        print(f"Error: {ticker} not found in STOCK_UNIVERSE.")
        return
        
    data = STOCK_UNIVERSE[ticker]
    beta = data["beta"]
    exp_return = data["analyst_expected_return"]
    std_dev = data["std_dev"]
    
    print(f"--- Multi-Agent Debate Demo: {ticker} ---")
    
    if mock_llm_status == "1" or mock_llm_status == "":
        # 1. Bull Agent (Focuses on upside and return vs beta)
        bull_argument = (f"BULL AGENT: With an analyst expected return of {exp_return:.1%} "
                         f"against a beta of {beta:.2f}, {ticker} offers attractive risk-adjusted upside. "
                         f"This is a strong opportunity for capital appreciation.")
        
        # 2. Bear Agent (Focuses on standard deviation and downside risk)
        bear_argument = (f"BEAR AGENT: The risk profile is simply too aggressive. {ticker} carries a substantial "
                         f"standard deviation of {std_dev:.1%}, exposing investors to severe "
                         f"drawdowns if macroeconomic conditions deteriorate.")
        
        # 3. Synthesizer Agent (2-3 sentence balanced summary)
        synthesizer_summary = (f"SYNTHESIZER: The debate highlights a classic high-risk, high-reward tradeoff for {ticker}. "
                               f"While the bull correctly identifies the lucrative {exp_return:.1%} expected return, the bear's "
                               f"concern regarding the {std_dev:.1%} volatility is highly relevant. Investors must carefully weigh their "
                               f"individual risk tolerance against this beta of {beta:.2f} before allocating capital.")
                               
        print(bull_argument)
        print("\n" + bear_argument)
        print("\n" + synthesizer_summary)
        
    else:
        # Note: If MOCK_LLM=0, implement the live API call logic here
        print(f"[LLM_API_ACTIVE] Generative debate responses for {ticker} go here.")

if __name__ == "__main__":
    print(f"Initializing Agentic Debate Team... (MOCK_LLM = {os.getenv('MOCK_LLM', '1')})\n")
    
    # We select ticker PAYTECH for the demonstration
    run_debate("PAYTECH")
