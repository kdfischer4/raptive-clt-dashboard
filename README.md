# Central Limit Theorem Explorer

An interactive Streamlit dashboard that demonstrates the **Central Limit Theorem (CLT)** with exponential, uniform, and binomial populations.

## What the app demonstrates

For independent observations with population mean $\mu$ and standard deviation $\sigma$, the distribution of the sample mean approaches a normal distribution as the sample size $n$ grows:

$$
\bar{X} \approx \mathcal{N}\left(\mu, \frac{\sigma}{\sqrt{n}}\right).
$$

Use the controls to change the population, sample size, and number of simulations. The dashboard compares:

- the population distribution and the distribution of simulated sample means;
- the theoretical mean and the simulated mean of sample means; and
- the theoretical standard error $\sigma / \sqrt{n}$ and its simulated counterpart.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## How it works

1. **Choose a population.** Each distribution has controls for its parameters and closed-form theoretical moments.
2. **Simulate repeated samples.** NumPy creates an array with one independent sample per row.
3. **Compute sample means.** Taking the mean across each row produces the empirical sampling distribution.
4. **Compare theory with simulation.** The app overlays the CLT normal approximation and reports theoretical and simulated summary statistics.

The population chart uses a separate sample of 50,000 observations so its appearance remains stable when the number of CLT simulations changes. A configurable random seed makes every view reproducible.

## Interview discussion points

- The CLT concerns the **sampling distribution of the mean**, not whether the original population is normal.
- Larger samples reduce standard error at the rate $1 / \sqrt{n}$.
- A skewed exponential population generally requires a larger sample size before its sample means look normal.
- More simulated samples make the empirical histogram and statistics more stable, but do not change the theoretical standard error.
- The binomial option is discrete, while its sample mean can take increasingly fine-grained values as $n$ grows.

## Deploy on Streamlit Community Cloud

1. Push this repository to a public GitHub repository.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), create an app from the repository.
3. Select `app.py` as the entry point and deploy.

No secrets or external data sources are required.
