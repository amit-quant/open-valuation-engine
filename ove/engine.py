import math
from scipy.stats import norm

class EuropeanOption:
    """
    Represents a standard European Option contract with intrinsic financial attributes.
    """
    def __init__(self, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type="call"):
        self.S = float(underlying_price)
        self.K = float(strike_price)
        self.T = float(time_to_maturity)
        self.r = float(risk_free_rate)
        self.sigma = float(volatility)
        self.option_type = option_type.lower()  # "call" or "put"

class ValuationEngine:
    """
    Advanced engine responsible for computing cross-asset option values and risk parameters (Greeks).
    """
    def __init__(self, precision=4):
        self.precision = precision

    def calculate_d1_d2(self, option: EuropeanOption):
        """Computes the d1 and d2 components of the Black-Scholes formula."""
        d1 = (math.log(option.S / option.K) + (option.r + 0.5 * option.sigma ** 2) * option.T) / (option.sigma * math.sqrt(option.T))
        d2 = d1 - option.sigma * math.sqrt(option.T)
        return d1, d2

    def price(self, option: EuropeanOption) -> float:
        """Calculates the present value (PV) of a European Call or Put Option."""
        d1, d2 = self.calculate_d1_d2(option)
        if option.option_type == "call":
            pv = option.S * norm.cdf(d1) - option.K * math.exp(-option.r * option.T) * norm.cdf(d2)
        elif option.option_type == "put":
            pv = option.K * math.exp(-option.r * option.T) * norm.cdf(-d2) - option.S * norm.cdf(-d1)
        else:
            raise ValueError("Invalid option type. Must be 'call' or 'put'.")
        return round(pv, self.precision)

    def delta(self, option: EuropeanOption) -> float:
        """Calculates Delta (sensitivity to underlying price changes)."""
        d1, _ = self.calculate_d1_d2(option)
        if option.option_type == "call":
            val = norm.cdf(d1)
        else:
            val = norm.cdf(d1) - 1.0
        return round(val, self.precision)

    def gamma(self, option: EuropeanOption) -> float:
        """Calculates Gamma (acceleration rate of Delta per point shift in underlying)."""
        d1, _ = self.calculate_d1_d2(option)
        val = norm.pdf(d1) / (option.S * option.sigma * math.sqrt(option.T))
        return round(val, self.precision)

    def vega(self, option: EuropeanOption) -> float:
        """Calculates Vega (sensitivity to a 1% absolute shift in volatility)."""
        d1, _ = self.calculate_d1_d2(option)
        val = option.S * norm.pdf(d1) * math.sqrt(option.T) * 0.01
        return round(val, self.precision)

    def theta(self, option: EuropeanOption) -> float:
        """Calculates Theta (time decay per single calendar day change)."""
        d1, d2 = self.calculate_d1_d2(option)
        term1 = -(option.S * norm.pdf(d1) * option.sigma) / (2 * math.sqrt(option.T))
        
        if option.option_type == "call":
            term2 = option.r * option.K * math.exp(-option.r * option.T) * norm.cdf(d2)
            val = (term1 - term2) / 365.0
        else:
            term2 = option.r * option.K * math.exp(-option.r * option.T) * norm.cdf(-d2)
            val = (term1 + term2) / 365.0
        return round(val, self.precision)

if __name__ == "__main__":
    test_put = EuropeanOption(
        underlying_price=150.0, strike_price=145.0, time_to_maturity=0.25, 
        risk_free_rate=0.05, volatility=0.20, option_type="put"
    )
    
    engine = ValuationEngine()
    print("--- Advanced Valuation Engine Test Run (Put Option) ---")
    print(f"Theoretical Put Price: ${engine.price(test_put)}")
    print(f"Put Delta:            {engine.delta(test_put)}")
    print(f"Put Gamma:            {engine.gamma(test_put)}")
    print(f"Put Vega (1% shift):  {engine.vega(test_put)}")
    print(f"Put Theta (per day):  {engine.theta(test_put)}")
