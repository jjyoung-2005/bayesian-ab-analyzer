# Bayesian UX Experiment Analyzer

#### Stop guessing. Start shipping. A Bayesian A/B test analyzer that tells you what your experiment data actually means.

**[Live Demo](https://bayesian-ab-analyzer-apucbenvinorzh8dk6k8yu.streamlit.app/)**

## The Problem

Most A/B test tools tell you *if* your variant won. They don't tell you *what to do about it*.

Product teams routinely ship losers and abandon winners. The goal for this tool is to fix that problem by combining Bayesian inference with a behavioral decision engine that gives clear recommendations.

## Features

- **Bayesian posterior estimation** that doesn't need extra p-values and arbitrary significance thresholds
- **Probability that B beats A** computed from 100,000 Monte Carlo simulations
- **Expected lift** expressed as a relative percentage
- **Posterior distribution plot** showing overlapping Beta curves for visual interpretation
- **Decision engine** that maps results to one of four actional outcomes based on statistis and significance
- **Adjustable minimum lift threshold** so teams can define what "meaningful" looks like for their specific context

## The Decision Engine

The app doesn't just output a probability. It also tells you what to do next. Based on the probability that B beats A and the minimum lift threshold, it returns one of four decisions shown in the table below.

| Decision | Meaning |
|---|---|
| **Ship It** | High confidence, meaningful lift -- variant is a clear winner |
| **Run Longer** | Promising signal but not enough data yet to be confident |
| **Abandon It** | Variant isn't winning or the lift is too small to matter |
| **Investigate Further** | Statistically clean result but lift is below practical threshold -- the most dangerous outcome |

The "Investigate Further" case is the most interesting because it catches the trap where a variant wins but the probability in real-life is negligible, which is a common mistake in product experiments.

## Tech Stack
- **Python**: core code
- **NumPy**: Provides Monte Carlo sampling and posterior estimation
- **SciPy**: Beta distribution for visualization
- **Matplotlib**: Distribution plot
- **Streamlit**: UI for deployment

## How to Run

```bash
git clone https://github.com/jjyoung-2005/bayesian-ab-analyzer.git
cd bayesian-ab-analyzer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## How It Works

### Bayesian Core

Each variant's conversion rate is modeled as a Beta distribution. Given successes `s` and trials `n`, the posterior is:

```
Beta(alpha = s, beta = n - s)
```

100,000 samples are pulled with the Monte Carlo simulation. The probability that B beats A is the fraction of simulated worlds where the variant sample exceeds the control sample:

```
prob_b_beats_a = np.mean(variant_samples > control_samples)
```

Expected lift is the average relative improvement across simulations:

```
expected_lift = np.mean((variant_samples - control_samples) / control_samples)
```

### Decision Engine

The Decision Engine takes the Bayesian outputs and a lift threshold and maps them to one of four outcomes to help with next steps. Lift is evaluated first - if it falls below the threshold the result is either "Abandon It" or "Investigate Further".

### Background

I wanted to do this project because it combines my two areas of study -- Data Science and Psychology. Bayesian A/B testing is a fundamental problem of decision making under uncertainty, and most failures are due to behavior. For example, stopping tests too early, following noise, and confusing statistical confidence with real-world impact. This tool is built to reduce those failures for product and UX teams who need clear answers.

