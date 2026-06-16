import numpy as np

def bayesian_ab(control_successes, control_trials, variant_successes, variant_trials, n_samples=100000):
    control_samples = np.random.beta(control_successes, control_trials - control_successes, size=n_samples)
    variant_samples = np.random.beta(variant_successes, variant_trials - variant_successes, size=n_samples)
    
    prob_b_beats_a = np.mean(variant_samples > control_samples)
    expected_lift = np.mean((variant_samples-control_samples)/control_samples)
    variant_interval = np.percentile(variant_samples, [2.5, 97.5])
    control_interval = np.percentile(control_samples, [2.5, 97.5])
    return {
        "Probability that B beats A": prob_b_beats_a,
        "Expected Lift": expected_lift,
        "Control Interval": control_interval,
        "Variant Interval": variant_interval,
        "Control Samples": control_samples,
        "Variant Samples": variant_samples
        }

result = bayesian_ab(420, 1000, 480, 1000)
print(result["Probability that B beats A"])
print(result["Expected Lift"])

def decision_engine(results, min_lift):
    b_beats_a = results["Probability that B beats A"]
    lift = results["Expected Lift"]

    if b_beats_a > 0.95 and lift > min_lift:
        return "Ship It!"
    elif b_beats_a >= 0.80 and b_beats_a <= 0.95 and lift >= min_lift:
        return "Run it longer."
    elif b_beats_a < 0.80 and lift < min_lift:
        return "Abandon it"
    elif b_beats_a > 0.95 and lift < min_lift:
        return "Investigate further"
    else:
        raise ValueError("Unexpected input combination")

result = bayesian_ab(420, 1000, 480, 1000)
print(decision_engine(result, 0.05))
