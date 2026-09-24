import math
from scipy.stats import norm
from ove.engine import EuropeanOption, ValuationEngine

class ImpliedVolatilitySolver:
    def __init__(self, max_iterations=100, tolerance=1e-6):
        self.max_iter = max_iterations
        self.tolerance = tolerance
        self.engine = ValuationEngine()

    def calculate_vega(self, option: EuropeanOption) -> float:
        """Calculates Vega analytically to use as the derivative in Newton-Raphson."""
        try:
            d1 = (math.log(option.S / option.K) + (option.r + 0.5 * option.sigma ** 2) * option.T) / (option.sigma * math.sqrt(option.T))
            vega = option.S * math.sqrt(option.T) * norm.pdf(d1)
            return max(vega, 1e-4) # Guardrail against dividing by absolute zero
        except Exception:
            return 1e-4

    def solve_iv(self, market_price: float, option: EuropeanOption) -> float:
        """Backs out implied volatility using the Newton-Raphson root-finding algorithm."""
        # Baseline initial seed guess (20% volatility)
        sigma_guess = 0.20
        option.sigma = sigma_guess

        for i in range(self.max_iter):
            # 1. Compute current theoretical price based on guess
            theoretical_price = self.engine.price(option)
            price_error = theoretical_price - market_price

            # 2. Check if convergence criteria is satisfied
            if abs(price_error) < self.tolerance:
                return round(sigma_guess, 4)

            # 3. Calculate Vega (slope derivative) for Newton-Raphson step
            vega = self.calculate_vega(option)

            # 4. Update the guess: x_new = x_old - f(x)/f'(x)
            sigma_guess = sigma_guess - (price_error / (vega * 100 if theoretical_price > 1 else vega))
            
            # Guardrails to keep volatility realistically bounded between 1% and 500%
            sigma_guess = max(min(sigma_guess, 5.0), 0.01)
            option.sigma = sigma_guess

        return round(sigma_guess, 4)
