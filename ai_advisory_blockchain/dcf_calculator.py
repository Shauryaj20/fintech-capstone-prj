import pandas as pd
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN

def calculate_dcf():
    print("="*50)
    print("DCF VALUATION MODEL")
    print("="*50)

    # 1. State Assumptions & Inputs
    # Base FCFF inputs(INR)
    ebit = 500000
    tax_rate = 0.25
    da = 50000
    capex = 70000
    delta_nwc = 30000

    # FCFF = EBIT * (1 - tax rate) + D&A - CapEx - Change in NWC
    base_fcff = (ebit * (1 - tax_rate)) + da - capex - delta_nwc
    print(f"Base FCFF Computed: ₹{base_fcff:,.2f}")

    # 2. Compute WACC
    # Select PAYINFRA beta = 1.10
    beta = STOCK_UNIVERSE["PAYINFRA"]["beta"]
    cost_of_equity = RISK_FREE_RATE + beta * (MARKET_RETURN - RISK_FREE_RATE)
    
    # Debt assumptions: 9% pre-tax cost of debt, 70/30 Equity/Debt split
    cost_of_debt_pre_tax = 0.09
    cost_of_debt_after_tax = cost_of_debt_pre_tax * (1 - tax_rate)
    
    weight_equity = 0.70
    weight_debt = 0.30
    
    wacc = (weight_equity * cost_of_equity) + (weight_debt * cost_of_debt_after_tax)
    print(f"Computed WACC: {wacc:.2%}")

    # 3. Growth Rates & DCF Projection
    high_growth_rate = 0.12 # 12% growth for first 5 years
    terminal_growth = 0.05  # 5% terminal growth 
    
    # Sanity check: ensure terminal growth is at least 3pp below base WACC
    assert wacc - terminal_growth >= 0.03, "Terminal growth must be at least 3pp below WACC."
    print(f"Terminal Growth Rate: {terminal_growth:.2%} (Passes safety constraint)")

    def run_dcf(discount_rate, tg_rate):
        """Helper to run the 5-year DCF + Terminal Value."""
        pv_fcfs = 0
        current_fcff = base_fcff
        
        # Project 5 years
        for year in range(1, 6):
            current_fcff *= (1 + high_growth_rate)
            pv_fcfs += current_fcff / ((1 + discount_rate) ** year)
            
        # Terminal Value = Year 5 FCF * (1 + g) / (WACC - g)
        terminal_value = (current_fcff * (1 + tg_rate)) / (discount_rate - tg_rate)
        pv_tv = terminal_value / ((1 + discount_rate) ** 5)
        
        return pv_fcfs + pv_tv

    base_enterprise_value = run_dcf(wacc, terminal_growth)
    print(f"\nBASE ENTERPRISE VALUE: ₹{base_enterprise_value:,.2f}")

    # 4. Sensitivity Table (3x3 Grid)
    print("\n" + "-"*50)
    print("SENSITIVITY ANALYSIS (WACC vs Terminal Growth)")
    print("-"*50)
    
    wacc_adjustments = [-0.01, 0.0, 0.01]
    tg_adjustments = [-0.01, 0.0, 0.01]
    
    grid = {}
    for w_adj in wacc_adjustments:
        adj_wacc = wacc + w_adj
        row = {}
        for t_adj in tg_adjustments:
            adj_tg = terminal_growth + t_adj
            row[f"TG {adj_tg:.1%}"] = run_dcf(adj_wacc, adj_tg)
        grid[f"WACC {adj_wacc:.2%}"] = row
        
    sensitivity_df = pd.DataFrame.from_dict(grid, orient='index')
    # Formatting for display
    print(sensitivity_df.map(lambda x: f"₹{x:,.0f}"))    

    # Worst case self-check
    worst_case_wacc = wacc - 0.01
    worst_case_tg = terminal_growth + 0.01
    spread = worst_case_wacc - worst_case_tg
    print(f"\nSafety Check: Worst-case cell spread (WACC - g) is {spread:.2%}")

    # 5. EV/EBITDA Cross-Check
    print("\n" + "-"*50)
    print("EV / EBITDA CROSS-CHECK")
    print("-"*50)
    
    # EBITDA = EBIT + D&A
    ebitda = ebit + da
    illustrative_multiple = 10.0
    ev_ebitda_valuation = ebitda * illustrative_multiple
    
    print(f"Illustrative EBITDA: ₹{ebitda:,.2f}")
    print(f"Applied Multiple: {illustrative_multiple}x")
    print(f"Multiple-based Enterprise Value: ₹{ev_ebitda_valuation:,.2f}")
    
    # The written comparison is printed directly to terminal
    print("\nComparison Commentary:")
    print(f"The DCF yields a higher base enterprise value (₹{base_enterprise_value:,.0f}) compared to the EV/EBITDA multiple approach (₹{ev_ebitda_valuation:,.0f}). This variance is expected because the DCF explicitly credits the business line for its aggressive 12% high-growth phase over the next 5 years. Conversely, a static 10x EBITDA multiple acts as a generic industry anchor that may underestimate near-term disruptive growth potential.")

if __name__ == "__main__":
    calculate_dcf()
