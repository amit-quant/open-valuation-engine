import unittest
from ove.engine import EuropeanOption, ValuationEngine

class TestValuationEngine(unittest.TestCase):
    def setUp(self):
        """Set up standard options with known market benchmarks."""
        self.engine = ValuationEngine(precision=4)
        
        # Benchmark scenario parameters
        self.call_option = EuropeanOption(
            underlying_price=100.0, strike_price=95.0, time_to_maturity=0.5,
            risk_free_rate=0.05, volatility=0.20, option_type="call"
        )
        self.put_option = EuropeanOption(
            underlying_price=100.0, strike_price=95.0, time_to_maturity=0.5,
            risk_free_rate=0.05, volatility=0.20, option_type="put"
        )

    def test_call_valuation(self):
        """Verifies Call price matches expected Black-Scholes analytical values."""
        price = self.engine.price(self.call_option)
        # Expected value is roughly 9.9360 based on Black-Scholes formulas
        self.assertAlmostEqual(price, 9.9360, places=2)

    def test_put_valuation(self):
        """Verifies Put price matches expected analytical values."""
        price = self.engine.price(self.put_option)
        # Expected value is roughly 2.6163
        self.assertAlmostEqual(price, 2.6163, places=2)

    def test_put_call_parity(self):
        """Validates underlying structural integrity via Put-Call Parity: C - P = S - K*e^(-rT)"""
        c = self.engine.price(self.call_option)
        p = self.engine.price(self.put_option)
        
        import math
        discounted_strike = self.call_option.K * math.exp(-self.call_option.r * self.call_option.T)
        left_side = round(c - p, 4)
        right_side = round(self.call_option.S - discounted_strike, 4)
        
        self.assertAlmostEqual(left_side, right_side, places=2)

if __name__ == "__main__":
    unittest.main()
