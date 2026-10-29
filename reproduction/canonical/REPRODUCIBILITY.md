# Reproduction of the computational snapshot

Author: Taylor Kalin.

The three programs run offline without source PDFs, reconstructed simulation
fields, GPU access or a network service. Use ordinary Python, without `-O`.
Run the commands below from the repository root, replacing the interpreter
placeholders with the appropriate environment's Python executable.

| Program | Recorded runtime | Dependencies |
| --- | --- | --- |
| Original producer, `reproduction/run_audit.py` | CPython 3.12.14 | NumPy 2.3.5, Matplotlib 3.11.2 |
| Independent filter check, `audit/independent-filter-review/check_filter_identities.py` | CPython 3.13.7 | Python standard library, including exact fractions |
| Independent moment and dispersion check, `audit/independent-moment-review/verify_source_identities.py` | CPython 3.13.7 | NumPy 2.2.1, SciPy 1.17.1 |

Install `requirements.txt` in the producer environment and
`requirements-verifiers.txt` in the independent-check environment. The filter
program itself does not import NumPy or SciPy. Its recorded Python version is
retained to reproduce its environment field byte for byte.

```text
<producer-python> -m pip install -r requirements.txt
<checker-python> -m pip install -r requirements-verifiers.txt
<producer-python> reproduction/run_audit.py
<checker-python> audit/independent-filter-review/check_filter_identities.py
<checker-python> audit/independent-moment-review/verify_source_identities.py
```

The producer regenerates eight files in `data/` and `figures/`; its optional
`--output-root` argument can direct those products to another folder. Each
independent program writes its own current JSON beside its script. Original-run
JSONs, original review notes and the explicit normalized-density correction are
retained separately. The producer does not import either independent program.

The computational manifest lists the byte size and SHA-256 of every bundled
file except the manifest itself. A clean archive test reruns all three programs
with their recorded runtimes and compares the entire extracted file inventory
and every file's bytes. The resulting release proof is maintained separately
from the computational snapshot to avoid a circular hash dependency.

Exact rational identities are portable across ordinary Python implementations.
Bitwise reproduction of the recorded results additionally depends on the stated
runtime versions; figure encoding and fonts can differ elsewhere. The examples
are synthetic algebra and subsystem controls, not a reconstruction of the
authors' filter, full kinetic model, simulation inputs or measured diagnostics.
All moment witnesses use `n = m = e = 1`. The density addendum takes precedence
over the original general-density prose. The Appendix E candidate was withdrawn
as an error and is retained only as a positive quantifier clarification.
