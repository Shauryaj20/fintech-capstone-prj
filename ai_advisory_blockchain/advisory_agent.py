import os
import math
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES

def get_stock_data(ticker):
    """ACT tool: retrieves stock data from the local universe mock."""
    return STOCK_UNIVERSE.get(ticker, {})

def process_investor_profile(profile):
    """Agent loop: Think, Act, Observe for a single investor."""
    investor_id = profile["investor_id"]
    risk_tolerance = profile["risk_tolerance"]
    
    print(f"\n--- Processing Profile: {investor_id} ({risk_tolerance}) ---")
    
    # 1. THINK
    print("Agent [THINK]: Analyzing risk tolerance to determine allocation strategy...")
    if risk_tolerance == "Conservative":
        tickers = ["PAYBOND", "PAYGOLD", "PAYRETAIL"]
    elif risk_tolerance == "Moderate":
        tickers = ["PAYRETAIL", "PAYINFRA", "PAYGOLD"]
    elif risk_tolerance == "Aggressive":
        tickers = ["PAYTECH", "PAYFIN", "PAYINFRA"]
    else:
        tickers = []
    
    w = 1.0 / 3.0 # Equal weighting
    
    # 2. ACT
    print(f"Agent [ACT]: Executing tool 'get_stock_data' for {tickers}...")
    portfolio_data = []
    for ticker in tickers:
        data = get_stock_data(ticker)
        portfolio_data.append({
            "ticker": ticker,
            "beta": data["beta"],
            "std_dev": data["std_dev"]
        })
    
    # 3. OBSERVE & DECIDE
    print("Agent [OBSERVE]: Computing CAPM return and Portfolio Variance...")
    expected_returns = []
    std_devs = []
    
    for item in portfolio_data:
        # CAPM Expected Return Formula: E(R) = R_f + Beta * (R_m - R_f)
        er = RISK_FREE_RATE + item["beta"] * (MARKET_RETURN - RISK_FREE_RATE)
        expected_returns.append(er)
        std_devs.append(item["std_dev"])
    
    # Compute Weighted Portfolio Expected Return
    port_er = sum(w * er for er in expected_returns)
    
    # Compute Portfolio Variance & Standard Deviation (rho = 0.3)
    rho = 0.3
    var_individual = sum((w ** 2) * (s ** 2) for s in std_devs)
    
    cov_sum = (std_devs[0] * std_devs[1] + 
               std_devs[0] * std_devs[2] + 
               std_devs[1] * std_devs[2])
    
    var_pairwise = 2 * (w * w) * rho * cov_sum
    port_var = var_individual + var_pairwise
    port_std_dev = math.sqrt(port_var)
    
    print(f"Agent [OBSERVE]: Computed Expected Return = {port_er:.2%}, Volatility (Std Dev) = {port_std_dev:.2%}")
    
    # 4. DECIDE / ESCALATION 
    mock_llm_status = os.getenv("MOCK_LLM", "1")
    
    if port_std_dev > 0.20:
        print(f"Agent [DECIDE]: ESCALATED_TO_HUMAN_ADVISOR. Volatility ({port_std_dev:.2%}) exceeds 20% limit.")
        final_decision = "ESCALATED_TO_HUMAN_ADVISOR"
    else:
        print("Agent [DECIDE]: Volatility within safe limits. Finalizing recommendation.")
        final_decision = "APPROVED"
        
    # Generate Narrative depending on LLM configuration
    if mock_llm_status == "1" or mock_llm_status == "":
        narrative = (f"For {risk_tolerance} investor {investor_id}, we recommend an allocation "
                     f"across {tickers} with an expected portfolio return of {port_er:.1%} "
                     f"and volatility of {port_std_dev:.1%}.")
    else:
        # Note: If you choose to do the Groq API , the API call logic goes here!
        narrative = (f"[GROQ_API_ACTIVE] Generative response goes here for {investor_id}.")
        
    print(f"Final Output: [{final_decision}] Narrative: {narrative}")

if __name__ == "__main__":
    print(f"Initializing Advisory Toolkit... (MOCK_LLM = {os.getenv('MOCK_LLM', '1')})")
    for profile in INVESTOR_PROFILES:
        process_investor_profile(profile)