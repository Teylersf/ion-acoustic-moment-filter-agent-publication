# Continuity and spatial averaging in ion-acoustic reconnection diagnostics

Author: Taylor Kalin.

This computational study checks a normalized ion-temperature moment subsystem
and finite-filter identities associated with Li, Liu and Loureiro,
*Role of ion acoustic instability in magnetic reconnection*, JPP 92, E20,
[10.1017/S002237782510113X](https://doi.org/10.1017/S002237782510113X).
This release contains the computational evidence, independent checks and source
concordance. The manuscript is maintained separately from this computational
snapshot.

```text
python -m pip install -r requirements.txt
python reproduction/run_audit.py
```

The independent programs use a separately recorded Python 3.13.7 environment.
See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for all three commands, both runtime
specifications and the distinction between exact algebra and image encoding.
The independent scientific reviews and their original receipts are included in
`audit/`; the normalized-density addendum supersedes the earlier arbitrary-density
prose without changing the original records.

The producer uses exact rational arithmetic for its algebra and floating point
only to draw two original figures. Its recorded plotting environment is bundled
Python 3.12.14, NumPy 2.3.5 and Matplotlib 3.11.2. It runs offline after dependencies
are installed and requires no GPU, private path, original PDF or source data.
Use ordinary Python; optimized mode is rejected. `--output-root` can select a
separate output folder. JSON records exact artifact hashes and the environment;
CSV rational strings retain the exact values. Figure encoding and fonts can vary
across environments.

- `figures/filter-covariance.png` compares full covariance, filtered pointwise
  residual products and the exact window-centered positive control.
- `figures/moment-compatibility.png` shows normalized finite-divergence
  moment-subsystem families approaching the same zero-divergence heat-flux
  condition with different temperatures.
- `data/producer-results.json` records controls, artifact hashes and limits.
- `data/producer-source-locators.json` identifies the source equations and the
  normalization used here. Independent source provenance is maintained separately.

Every SG example is synthetic. No actual source kernel, polynomial degree,
boundary handling or residual convention is recovered. SG weights can be negative;
the weighted covariance is not a nonnegative probability variance. Window-centered
residual products reproduce the exact covariance for the examples and constitute
an explicit alternative interpretation that could resolve the identity issue.
The source's hidden implementation is unresolved.

All B5 counterexamples fix n=m=e=1, u_z=2 and E_z=3. They test only the printed
zz-moment/z-momentum subsystem. Nonzero-divergence paths violate exact steady
uniform-density continuity and are not complete steady solutions. Their endpoints
have zero divergence and zero zz heat-flux divergence while retaining arbitrary
selected positive Tzz. The divided B6c expression is then undefined. These checks
do not refute measured ion heating or establish a corrected reconnection rate.
The withdrawn Appendix E candidate is not an error finding.

Code is licensed under the [MIT license](LICENSE-CODE). Original manuscript text,
figures and explanatory documentation are licensed under
[CC BY 4.0](LICENSE-MANUSCRIPT). Third-party material retains its own rights.
