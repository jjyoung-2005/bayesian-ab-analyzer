import numpy as np
import streamlit as st

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


def decision_engine(results, min_lift):
    b_beats_a = results["Probability that B beats A"]
    lift = results["Expected Lift"]

    if lift >= min_lift:
        if b_beats_a > 0.95:
            return "Ship It!"
        elif b_beats_a >= 0.80:
            return "Run it longer."
        else:
            return "Abandon it"
    else:  
        if b_beats_a > 0.95:
            return "Investigate further"
        else:
            return "Abandon it"


st.title("Bayesian UX Experiment Analyzer")
st.subheader("Make confident shipping decisions from A/B test data")

st.divider()
st.header("Experiment Inputs")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Control (A)")
    control_successes = st.number_input("Successes", min_value=1, value=100, key= "control_successes")
    control_trials = st.number_input("Trials", min_value=1, value=1000, key="control_trials")

with col2:
    st.subheader("Variant (B)")
    variant_successes = st.number_input("Successes", min_value=1, value=120, key="variant_successes")
    variant_trials = st.number_input("Trials", min_value=1, value=1000, key="variant_trials")

st.divider()
min_lift = st.slider("Minimum meaningful lift (%)", min_value=1, max_value=20, value=5) / 100

if st.button("Analyze"):
    results = bayesian_ab(control_successes, control_trials, variant_successes, variant_trials)
    decision = decision_engine(results, min_lift)
    
    st.divider()
    st.header("Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Probability B beats A", f"{results['Probability that B beats A']:.1%}")
    
    with col2:
        st.metric("Expected Lift", f"{results['Expected Lift']:.1%}")
    
    with col3:
        st.metric("Decision", decision)
    
    st.divider()
    st.subheader("Credible Intervals")
    st.write(f"Control (A): {results['Control Interval'][0]:.3f} – {results['Control Interval'][1]:.3f}")
    st.write(f"Variant (B): {results['Variant Interval'][0]:.3f} – {results['Variant Interval'][1]:.3f}")
