# VAR Engine
<img width="1836" height="615" alt="dash" src="https://github.com/user-attachments/assets/52cb46ae-631d-4f69-944a-067aff923d54" />

## Table of Content
1. [About the project](#about-the-project)
2. [Some Analysis](#some-analysis)
    * [Test for normality](#test-for-normality)
    * [Kupiec Test](#kupiec-test)
    * [Backtesting](#backtesting)
    * [GARCH(1,1)](#garch(1,1))
3. [How to run the app](#how-to-run-the-app)
4. [Related Topics to Explore](#related-topics-to-explore)
5. [Author](#author)
## About the project
This project builds a professional grade quantitative risk engine for measuring and managing portfolio risk using statistical and simulation based methods. It addresses one of the most fundamental questions in finance that is "How much can one lose tomorrow, and how bad can it get in a worst-case scenario?".
Applied to a diversified $1,000,000 multi-asset portfolio spanning equities (AAPL, MSFT), financials (JPM), commodities (GLD), and fixed income (TLT), the engine implements three progressively sophisticated Value at Risk (VaR) methodologies, namely; 
- Historical Simulation
- Parametric (Gaussian)
- Monte Carlo with Cholesky decomposition
  
and extends to GARCH(1,1) volatility modelling to capture real world volatility clustering absent in standard Geometric Brownian Motion (GBM) assumptions.
The project follows a rigorous analytical workflow, statistical testing first establishes that asset returns violate the normality assumption underlying standard risk models (Jarque-Bera tests reject normality for all assets, with excess kurtosis ranging from 3.07 to 12.94), motivating the need for more sophisticated approaches. Model integrity is then formally validated through walk-forward backtesting using the Kupiec Proportion of Failures test which is a regulatory standard under Basel III/IV. The backtest reveals violation clustering around the COVID-19 crash (March 2020) and the Federal Reserve rate hiking cycle (2022), confirming that static historical VaR suffers from regime blindness and motivating the GARCH extension. Portfolio allocation is further optimised via Markowitz Efficient Frontier analysis and Maximum Sharpe Ratio optimisation across 5,000 simulated portfolios. All findings are accessible through an interactive Streamlit dashboard enabling dynamic risk metric computation across user defined assets, weights, and confidence levels.

## Some Analysis

### Test for normality
Performing several tests such as JB test. The Jarque-Bera tests reject normality for all assets at the 1% significance level. Excess kurtosis ranging from 3.07 (GLD) to 12.94 (JPM) confirms significant fat tails across the portfolio, while negative skewness in four of five assets indicates asymmetric downside risk. These findings invalidate the normality assumption underlying parametric VaR and motivate the use of Monte Carlo simulation with empirically calibrated return distributions

### Kupiec Test
The Kupiec Proportion of Failures test rejected the Historical VaR model at the 1% significance level (Likelihood Ratio, LR=10.72, p=0.0011), with an observed violation rate of 2.19% against an expected rate of 1.00%. Violation clustering around the COVID-19 crash (March 2020) and the 2022 rate shock confirms that static historical VaR underestimates tail risk during regime changes, this failure motivates us to do the Generalised Autoregressive Conditional Heteroskedasticity (GARCH) volatility extension, which dynamically adjusts the VaR estimate in response to changing market conditions.

### Backtesting
<img width="1361" height="625" alt="Screenshot from 2026-03-10 14-21-55" src="https://github.com/user-attachments/assets/a9641610-6a34-4298-a05d-6e8b5d2a974b" />
The backtest chart reveals that all 22 VaR violations cluster around two distinct market stress regimes 
   -the COVID-19 crash of March 2020 (days 40-80) and 
   -the Federal Reserve rate hiking cycle of 2022 (days 550-650). 

This violation clustering confirms that Historical VaR suffers from regime blindness, that is; the 252-day rolling window reacts to volatility only after it has materialised, consistently underestimating risk at the precise moments it matters most. This structural weakness directly motivates the GARCH(1,1) extension, which dynamically adjusts volatility estimates in response to current market conditions rather than relying on a static historical window.

### GARCH(1,1)
From the analysis we made, GARCH(1,1) volatility forecasts are materially lower than the 5-year historical volatility for equity positions (approximately 50% lower for JPM), this reflects calmer market conditions prevailing at the end of the sample period. This demonstrates GARCH's core advantage over static historical VaR: it dynamically adjusts risk estimates in response to current market regimes rather than treating all historical periods equally. During stress periods GARCH would raise volatility estimates rapidly, providing earlier warning than a 252-day rolling window.


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

## Related Topics to Explore
- [VaR(Value at Risk)](https://en.wikipedia.org/wiki/Value_at_risk)
- [GARCH (Generalised Autoregressive Conditional Heteroskedasticity)](https://www.geeksforgeeks.org/artificial-intelligence/generalized-autoregressive-conditional-heteroskedasticity/)
- [Geometric Brownian Motion](https://en.wikipedia.org/wiki/Geometric_Brownian_motion)

## Author
Odaudu Etubi
