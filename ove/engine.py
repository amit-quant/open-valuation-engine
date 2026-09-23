import math
from scipy.stats import norm

class EuropeanOption:
    """
    Represents a standard European Option contract with intrinsic financial attributes.
    """
    def __init__(self, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility):
        self.S = float(underlying_price)
        self.K = float(strike_price)
        self.T = float(time_to_maturity)
        self.r = float(risk_free_rate)
        self.sigma = float(volatility)

class ValuationEngine:
    """
    Core engine responsible for computing option fair values and risk sensitivities (Greeks).
    """
    def __init__(self, precision=4):
        self.precision = precision

    def calculate_d1_d2(self, option: EuropeanOption):
        """Computes the d1 and d2 components of the Black-Scholes formula."""
        d1 = (math.log(option.S / option.K) + (option.r + 0.5 * option.sigma ** 2) * option.T) / (option.sigma * math.sqrt(option.T))
        d2 = d1 - option.sigma * math.sqrt(option.T)
        return d1, d2

    def price_call(self, option: EuropeanOption) -> float:
        """Calculates the present value (PV) of a European Call Option."""
        d1, d2 = self.calculate_d1_d2(option)
        pv = option.S * norm.cdf(d1) - option.K * math.exp(-option.r * option.T) * norm.cdf(d2)
        return round(pv, self.precision)

    def calculate_delta(self, option: EuropeanOption) -> float:
        """Calculates the Delta (sensitivity to underlying asset price shift)."""
        d1, _ = self.calculate_d1_d2(option)
        delta = norm.cdf(d1)
        return round(delta, self.precision)

# Quick verification block to test your engine locally
if __name__ == "__main__":
    # Test Data: Stock at $150, Strike at $145, 3 Months to maturity, 5% Risk-free rate, 20% Volatility
    test_option = EuropeanOption(
        underlying_price=150.0, 
        strike_price=145.0, 
        time_to_maturity=0.25, 
        risk_free_rate=0.05, 
        volatility=0.20
    )
    
    engine = ValuationEngine()
    call_price = engine.price_call(test_option)
    call_delta = engine.calculate_delta(test_option)
    
    print("--- Valuation Engine Test Run ---")
    print(f"Theoretical Call Price: ${call_price}")
    print(f"Call Delta: {call_delta}")
