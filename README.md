### Open Valuation Engine (OVE)

An open-source, microservices-ready quantitative finance engine for pricing and validating Exchange-Traded Derivatives (ETD) and Over-the-Counter (OTC) financial instruments. 

Built for financial engineers, middle-office automated workflows, and valuation control teams who require independent price verification (IPV) without vendor lock-in. 

### 🚀 Key Features

* **Multi-Asset Pricing:** Built-in support for European/American Options, Equity Swaps, and Fixed Income instruments.
* **Valuation Control Pipelines:** Automated Independent Price Verification (IPV) workflows designed to flag variance against external broker quotes.
* **Pluggable Market Data:** Abstracted data layer to consume reference data and yield curves from open feeds or enterprise market terminals.
* **High-Performance Quant Models:** Utilizes industry-standard analytical formulas and Monte Carlo simulations under the hood.

### 🏗️ Architecture Overview

The system bridges financial mathematics with modern, scalable software engineering: 

[ Market Data API / CSV ] ──> [ Data Ingestion & Cleansing ] 
                                           │
                                           ▼
[ Quantitative Models ] ────> [ Core Valuation Engine ] ──> [ IPV Report / JSON ]
(Black-Scholes / MC)

### 📊 Quick Start (Python)

### 1. Prerequisites

Ensure you have Python 3.10+ installed. Clone the repository and install dependencies: 

bash

git clone https://github.com/your-username/open-valuation-engine.git
cd open-valuation-engine
pip install -r requirements.txt

Use code with caution.

### 2. Basic Option Pricing Example

Calculate the theoretical value and Greeks of a European Call Option: 

python

from ove.models.equity import EuropeanOption
from ove.engine import ValuationEngine

# Define the contract details
option = EuropeanOption(
    underlying_price=150.0,
    strike_price=145.0,
    time_to_maturity=0.25,  # 3 months
    risk_free_rate=0.05,    # 5%
    volatility=0.20         # 20%
)

# Initialize the engine
engine = ValuationEngine()
result = engine.calculate_present_value(option)

print(f"Present Value: {result.pv:.4f}")
print(f"Delta: {result.greeks.delta:.4f}")
print(f"Gamma: {result.greeks.gamma:.4f}")

Use code with caution.

### 🧮 Core Mathematics

The analytical valuation of European equity options is derived using the standard Black-Scholes-Merton differential equations. The fair price for a Call Option (C) is computed as: 

C=S0N(d1)−Ke−rTN(d2)cap C equals cap S sub 0 cap N open paren d sub 1 close paren minus cap K e raised to the negative r cap T power cap N open paren d sub 2 close paren
𝐶=𝑆0𝑁(𝑑1)−𝐾𝑒−𝑟𝑇𝑁(𝑑2)
 

Where: 

* 𝑑1

=ln(𝑆0/𝐾)+(𝑟+𝜎2/2)𝑇𝜎𝑇√
* 𝑑2

=𝑑1

−𝜎

𝑇√
* N(x) represents the standard normal cumulative distribution function.

### 🤝 Contributing

We welcome contributions from quantitative analysts, risk managers, and software developers! 

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

### 📄 License

Distributed under the MIT License. See LICENSE for more information.
