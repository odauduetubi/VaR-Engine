# VAR Engine
<img width="1836" height="615" alt="dash" src="https://github.com/user-attachments/assets/52cb46ae-631d-4f69-944a-067aff923d54" />

## Table of Content
1. [About the project](#about-the-project)
2. [VaR (Value at Risk)](#var)
    * [Test for normality](#test-for-normality)
3. [How to run the app](#how-to-run-the-app)
## About the project
This project builds a professional grade quantitative risk engine for measuring and managing portfolio risk using statistical and simulation based methods. It addresses one of the most fundamental questions in finance that is "How much can one lose tomorrow, and how bad can it get in a worst-case scenario?".
Applied to a diversified $1,000,000 multi-asset portfolio spanning equities (AAPL, MSFT), financials (JPM), commodities (GLD), and fixed income (TLT), the engine implements three progressively sophisticated Value at Risk (VaR) methodologies, namely; 
- Historical Simulation
- Parametric (Gaussian)
- Monte Carlo with Cholesky decomposition
  
and extends to GARCH(1,1) volatility modelling to capture real world volatility clustering absent in standard Geometric Brownian Motion (GBM) assumptions.
The project follows a rigorous analytical workflow, statistical testing first establishes that asset returns violate the normality assumption underlying standard risk models (Jarque-Bera tests reject normality for all assets, with excess kurtosis ranging from 3.07 to 12.94), motivating the need for more sophisticated approaches. Model integrity is then formally validated through walk-forward backtesting using the Kupiec Proportion of Failures test which is a regulatory standard under Basel III/IV. The backtest reveals violation clustering around the COVID-19 crash (March 2020) and the Federal Reserve rate hiking cycle (2022), confirming that static historical VaR suffers from regime blindness and motivating the GARCH extension. Portfolio allocation is further optimised via Markowitz Efficient Frontier analysis and Maximum Sharpe Ratio optimisation across 5,000 simulated portfolios. All findings are accessible through an interactive Streamlit dashboard enabling dynamic risk metric computation across user defined assets, weights, and confidence levels.

## VaR (Value at Risk)

### Test for normality
Performing several tests such as JB test. The Jarque-Bera tests reject normality for all assets at the 1% significance level. Excess kurtosis ranging from 3.07 (GLD) to 12.94 (JPM) confirms significant fat tails across the portfolio, while negative skewness in four of five assets indicates asymmetric downside risk. These findings invalidate the normality assumption underlying parametric VaR and motivate the use of Monte Carlo simulation with empirically calibrated return distributions

## How to run the app
1. Click the "Fork" button on GitHub to copy this repository to your account.
2. Clone your fork locally:
   ```
   git clone https://github.com/<your-username>/<your-forked-repo>.git
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```
