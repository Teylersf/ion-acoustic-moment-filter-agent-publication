"""Original exact scalar examples for filter and moment-subsystem identities.

All algebra uses Fraction. Floating point is used only to draw two figures.
No original PIC data, source filter, full kinetic state or steady solution is
reconstructed. No independent verifier is imported or executed.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = {
    "title": "Role of ion acoustic instability in magnetic reconnection",
    "authors": ["D. Li", "Z. Liu", "N. F. Loureiro"],
    "journal": "Journal of Plasma Physics 92(1), E20 (2026)",
    "doi": "10.1017/S002237782510113X",
    "arxiv": "2505.08983v1",
    "journal_PDF_SHA256": "0ad1cbf795a58958b6889bebdff355fd463fb343aadef84e12e9261e100d7fa0",
    "hash_semantics": "Previously verified source provenance; this offline producer does not read or rehash the source PDF.",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def exact_linear_solve(matrix, right):
    """Gauss-Jordan elimination in Q; no numerical fit or external solver."""
    n = len(right)
    a = [[F(x) for x in row] + [F(value)] for row, value in zip(matrix, right)]
    assert len(a) == n and all(len(row) == n + 1 for row in a)
    for column in range(n):
        pivot = next((row for row in range(column, n) if a[row][column]), None)
        if pivot is None:
            raise ValueError("Singular exact fit")
        a[column], a[pivot] = a[pivot], a[column]
        factor = a[column][column]
        a[column] = [x / factor for x in a[column]]
        for row in range(n):
            if row != column:
                scale = a[row][column]
                a[row] = [x - scale * y for x, y in zip(a[row], a[column])]
    return [row[-1] for row in a]


def sg_kernel(window, degree):
    """Centered least-squares polynomial evaluation, derived in exact Q."""
    if window < 1 or window % 2 != 1 or not 0 <= degree < window:
        raise ValueError("Odd window and degree smaller than window required")
    offsets = list(range(-(window // 2), window // 2 + 1))
    gram = [[sum(F(x) ** (j + k) for x in offsets) for k in range(degree + 1)]
            for j in range(degree + 1)]
    dual = exact_linear_solve(gram, [1] + [0] * degree)
    weights = [sum(dual[k] * F(x) ** k for k in range(degree + 1)) for x in offsets]
    for order in range(degree + 1):
        assert sum(w * F(x) ** order for x, w in zip(offsets, weights)) == (1 if order == 0 else 0)
    assert weights == list(reversed(weights))
    return list(zip(offsets, weights))


def apply(kernel, field, center=0):
    return sum((weight * field(center + offset) for offset, weight in kernel), F(0))


def covariance_case(kernel, density, field):
    N = apply(kernel, density)
    mean = apply(kernel, field)
    assert N > 0
    filtered_n = lambda x: apply(kernel, density, x)
    filtered_f = lambda x: apply(kernel, field, x)
    residual_n = lambda x: density(x) - filtered_n(x)
    residual_f = lambda x: field(x) - filtered_f(x)
    full = apply(kernel, lambda x: density(x) * field(x)) - N * mean
    pointwise = apply(kernel, lambda x: residual_n(x) * residual_f(x))
    centered = apply(kernel, lambda x: (density(x) - N) * (field(x) - mean))
    leonard = apply(kernel, lambda x: filtered_n(x) * filtered_f(x)) - N * mean
    cross_nf = apply(kernel, lambda x: filtered_n(x) * residual_f(x))
    cross_fn = apply(kernel, lambda x: residual_n(x) * filtered_f(x))
    missing = leonard + cross_nf + cross_fn
    assert centered == full and full == pointwise + missing
    # Static electric/pressure force balance, u=B=0, div(P)=q*n*f.
    exact_D = -full / N
    residual_D = -pointwise / N
    electric_rhs_exact = mean - exact_D - apply(kernel, lambda x: density(x) * field(x)) / N
    electric_rhs_pointwise = mean - residual_D - apply(kernel, lambda x: density(x) * field(x)) / N
    assert electric_rhs_exact == 0 and -electric_rhs_pointwise == missing / N
    return dict(N=N, filtered_field=mean, full_covariance=full,
                pointwise_residual_product=pointwise, window_centered_product=centered,
                Leonard=leonard, cross_N_fprime=cross_nf, cross_nprime_F=cross_fn,
                missing_K=missing, exact_D=exact_D, pointwise_D=residual_D,
                D2_electric_left_minus_right_exact=-electric_rhs_exact,
                D2_electric_left_minus_right_pointwise=-electric_rhs_pointwise)


def synthetic_filter_cases():
    fields = {
        "quadratic": (lambda x: F(2 + x * x), lambda x: F(x * x)),
        "weak_quadratic": (lambda x: F(2) + F(x * x, 100), lambda x: F(x * x)),
        "alternating": (lambda x: F(3) + F(1 if x % 2 == 0 else -1), lambda x: F(1 if x % 2 == 0 else -1)),
        "constant_density": (lambda x: F(3), lambda x: F(x * x)),
        "constant_field": (lambda x: F(2 + x * x), lambda x: F(2)),
    }
    kernel_rows, case_rows, temporal_rows = [], [], []
    for window, degree in [(5, 2), (7, 3), (9, 2), (5, 4)]:
        kernel = sg_kernel(window, degree)
        kernel_rows.extend(dict(window=window, degree=degree, offset=x, weight=str(w), weight_float=float(w)) for x, w in kernel)
        if (window, degree) == (5, 2):
            assert [w for _, w in kernel] == [F(x, 35) for x in [-3, 12, 17, 12, -3]]
        for label, (density, field) in fields.items():
            r = covariance_case(kernel, density, field)
            assert all(density(x) > 0 for x in range(-window + 1, window))
            # One possible separable2D SG operator on fields independent of y.
            N2 = sum(wx * wy * density(x) for x, wx in kernel for y, wy in kernel)
            F2 = sum(wx * wy * field(x) for x, wx in kernel for y, wy in kernel)
            covariance2 = sum(wx * wy * density(x) * field(x) for x, wx in kernel for y, wy in kernel) - N2 * F2
            centered2 = sum(wx * wy * (density(x) - N2) * (field(x) - F2) for x, wx in kernel for y, wy in kernel)
            assert covariance2 == centered2 == r["full_covariance"]
            case_rows.append(dict(window=window, degree=degree, field_case=label,
                                  **{k: str(v) for k, v in r.items()},
                                  separable2D_covariance=str(covariance2)))
            # Instantaneous temporal control: u=E=B=0, du/dt=f,
            # div(P)=-m*n*f. The charge sign is retained; m=1 here.
            for charge in [F(1), F(-1)]:
                exact_V = r["full_covariance"] / (charge * r["N"])
                residual_V = r["pointwise_residual_product"] / (charge * r["N"])
                pressure_rhs = apply(kernel, lambda x: density(x) * field(x)) / (charge * r["N"])
                resolved_lhs = r["filtered_field"] / charge
                residual_exact = resolved_lhs + exact_V - pressure_rhs
                residual_pointwise = resolved_lhs + residual_V - pressure_rhs
                assert residual_exact == 0
                assert residual_pointwise == -r["missing_K"] / (charge * r["N"])
                temporal_rows.append(dict(window=window, degree=degree, field_case=label,
                    charge=str(charge), exact_V=str(exact_V), pointwise_V=str(residual_V),
                    D2_temporal_left_minus_right_exact=str(residual_exact),
                    D2_temporal_left_minus_right_pointwise=str(residual_pointwise)))
    selected = {(r["window"], r["degree"], r["field_case"]): r for r in case_rows}
    assert F(selected[5, 2, "quadratic"]["full_covariance"]) == -F(72, 35)
    assert F(selected[5, 2, "weak_quadratic"]["full_covariance"]) == -F(18, 875)
    assert F(selected[5, 2, "alternating"]["full_covariance"]) == F(1056, 1225)
    assert F(selected[5, 2, "alternating"]["pointwise_residual_product"]) == F(2304, 1225)
    for r in case_rows:
        if r["field_case"].startswith("constant") or (r["window"], r["degree"]) == (5, 4):
            assert F(r["full_covariance"]) == F(r["pointwise_residual_product"]) == 0
    # A genuine broadcast finite ensemble average is a separate positive control.
    n, f = [F(1), F(2), F(4)], [F(0), F(2), F(-1)]
    N, mean = sum(n) / 3, sum(f) / 3
    ensemble = sum(a * b for a, b in zip(n, f)) / 3 - N * mean
    ensemble_residual = sum((a - N) * (b - mean) for a, b in zip(n, f)) / 3
    assert ensemble == ensemble_residual
    return kernel_rows, case_rows, temporal_rows, str(ensemble)


def moment_families():
    """Literal printed B5c/d evaluated ONLY at normalized n=m=e=1."""
    u, E = F(2), F(3)
    temperatures = [F(1, 4), F(1), F(2), F(4), F(13, 3), F(7), F(10)]
    divergences = [sign * F(1, 2 ** k) for sign in [1, -1] for k in range(19)] + [F(0)]
    rows = []
    for temperature in temperatures:
        for d in divergences:
            off_diagonal_gradient = E - u * d
            heat_flux_divergence = (u * u - temperature) * d
            B5c = heat_flux_divergence + (temperature + u * u) * d + 2 * u * off_diagonal_gradient - 2 * E * u
            B5d = E - off_diagonal_gradient - u * d
            assert B5c == B5d == 0
            if d:
                estimator = u * u - heat_flux_divergence / d
                assert estimator == temperature
            else:
                estimator = None
                assert heat_flux_divergence == 0 and off_diagonal_gradient == E
            rows.append(dict(n="1", m="1", e="1", u_z=str(u), E_z=str(E),
                T_zz=str(temperature), d=str(d), offdiagonal_temperature_gradient=str(off_diagonal_gradient),
                Qzz_heat_flux_divergence=str(heat_flux_divergence),
                B5c_residual=str(B5c), B5d_residual=str(B5d),
                B6c_defined=d != 0, B6c_value=str(estimator) if estimator is not None else "undefined",
                steady_uniform_continuity_residual=str(d),
                meets_steady_uniform_continuity=d == 0,
                complete_steady_or_kinetic_solution_claimed=False))
    assert len(rows) == 273
    zero_rows = [r for r in rows if F(r["d"]) == 0]
    assert len(zero_rows) == 7 and len({r["T_zz"] for r in zero_rows}) == 7
    return rows


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_figures(output, cases, moments):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
        "axes.titlesize": 12, "xtick.labelsize": 11, "ytick.labelsize": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "figure.dpi": 150, "savefig.dpi": 210, "axes.grid": True, "grid.alpha": 0.2})
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.1), layout="constrained")
    for ax, label, title in zip(axes, ["quadratic", "alternating"],
            ["(a) Quadratic fields\n$n=2+x^2,\\ f=x^2$", "(b) Alternating fields\n$n=3+(-1)^x,\\ f=(-1)^x$"]):
        r = next(r for r in cases if r["window"] == 5 and r["degree"] == 2 and r["field_case"] == label)
        values = [F(r[k]) for k in ["full_covariance", "pointwise_residual_product", "window_centered_product"]]
        bars = ax.bar(range(3), [float(v) for v in values], width=0.63,
                      color=["#164e63", "#b45309", "#2d7d70"])
        bars[2].set_hatch("///")
        ax.axhline(0, color="#475569", lw=0.8)
        ax.set_xticks(range(3), ["Full\ncovariance", "Pointwise\nresiduals", "Window-\ncentered"])
        ax.set(title=title, ylabel="Weighted covariance (synthetic units)")
        ax.set_ylim((-2.8, 0.65) if label == "quadratic" else (-0.15, 2.45))
        for i, v in enumerate(values):
            math_label = str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"
            ax.annotate("$" + math_label + "$", (i, float(v)), xytext=(0, 8 if v >= 0 else -21),
                        textcoords="offset points", ha="center", fontsize=11)
    fig.suptitle("Illustrative SG(5,2), evaluated at the window center", fontsize=13)
    fig.savefig(output / "figures/filter-covariance.png")
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.0), layout="constrained")
    for t, color in [(F(1), "#164e63"), (F(4), "#64748b"), (F(7), "#b45309")]:
        rows = [r for r in moments if F(r["T_zz"]) == t and F(r["d"]) > 0]
        x = [float(F(r["d"])) for r in rows]
        style = "--" if t == 4 else "-"
        axes[0].plot(x, [float(F(r["Qzz_heat_flux_divergence"])) for r in rows], style,
                     color=color, lw=2, label=rf"$T_{{zz}}={t}$")
        axes[1].plot(x, [float(F(r["B6c_value"])) for r in rows], style, color=color, lw=2,
                     label=rf"$T_{{zz}}={t}$")
    for ax in axes:
        ax.set_xscale("log")
        ax.invert_xaxis()
        ax.set_xlabel(r"Positive divergence parameter $d\to0$")
    axes[0].set_yscale("symlog", linthresh=1e-4)
    axes[0].set(title="(a) All heat-flux divergences approach zero", ylabel=r"Heat-flux divergence $Q_{zz}$ (synthetic units)")
    axes[0].legend(fontsize=11, loc="upper right")
    axes[1].set(title="(b) Nonzero-d ratios retain distinct temperatures", ylabel=r"$u_z^2-Q_{zz}/d$", ylim=(0, 8.2))
    axes[1].legend(fontsize=11, loc="center right")
    fig.suptitle("Normalized B5c/d subsystem; finite-d paths are not full steady solutions", fontsize=12)
    fig.savefig(output / "figures/moment-compatibility.png")
    plt.close(fig)
    return dict(numpy=np.__version__, matplotlib=matplotlib.__version__)


def main():
    if sys.flags.optimize:
        raise RuntimeError("Run ordinary Python; -O disables exact algebra guards")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=ROOT)
    output = parser.parse_args().output_root.resolve()
    for directory in ["data", "figures"]:
        (output / directory).mkdir(parents=True, exist_ok=True)
    kernels, cases, temporal, ensemble = synthetic_filter_cases()
    moments = moment_families()
    for name, rows in [("sg-kernels.csv", kernels), ("sg-covariances.csv", cases),
                       ("sg-temporal-controls.csv", temporal), ("moment-families.csv", moments)]:
        write_csv(output / "data" / name, rows)
    versions = make_figures(output, cases, moments)
    locators = {"source": SOURCE, "source_formulas_not_reconstructed_code": True,
        "journal_locators": {
            "B5c": "p.20: raw zz moment at the X-point; literal normalized n=m=e=1 subsystem used here",
            "B5d": "p.20: z momentum at the X-point",
            "B6c": "p.20: temperature ratio divides by d=partial_x u_ix+partial_y u_iy",
            "B10b": "p.20: quantitative zero-heat-flux temperature estimate that cites B6c",
            "B13": "p.21: steady uniform-density continuity imposes divergence zero",
            "4.2_and_4.5": "pp.14–15: anomalous drag and temporal flow terms",
            "D2": "p.23: normalized averaged momentum identity and finite spatial SG description"},
        "normalization_limit": "B5c/d controls fix n=m=e=1. No general-density cancellation is asserted for the literal printed prefactors.",
        "filter_limit": "All windows, degrees and fields are synthetic. The actual source kernel, degree, edge handling and residual convention remain unresolved.",
        "excluded_claim": "Appendix E error candidate was withdrawn and is not an error finding in this package."}
    (output / "data/producer-source-locators.json").write_text(json.dumps(locators, indent=2) + "\n", encoding="utf-8")
    artifacts = ["data/sg-kernels.csv", "data/sg-covariances.csv", "data/sg-temporal-controls.csv",
                 "data/moment-families.csv", "data/producer-source-locators.json",
                 "figures/filter-covariance.png", "figures/moment-compatibility.png"]
    result = {"schema_version": 1, "status": "pass", "author": "Taylor Kalin",
        "scope": "Original exact synthetic filter identities and normalized B5 moment-subsystem compatibility controls; no PIC, actual filter recovery or full steady solution.",
        "producer_sha256": digest(Path(__file__).read_bytes()),
        "environment": {"python": platform.python_version(), **versions},
        "exact_arithmetic": "fractions.Fraction for all kernels, moments, covariances, force residuals and compatibility checks; float used only for figures",
        "filter_controls": {"kernels": 4, "cases": len(cases), "temporal_charge_controls": len(temporal),
            "all_covariance_and_window_centered_products_exact": True,
            "all_Leonard_cross_decompositions_exact": True,
            "all_exact_filtered_force_budgets_close": True,
            "separable2D_constant_y_covariance_verified": True,
            "ensemble_covariance_and_residual_product": ensemble,
            "SG_negative_weight_note": "A normalized SG weighted covariance need not be a nonnegative probabilistic variance.",
            "actual_source_filter_recovered": False},
        "moment_controls": {"normalization": "n=m=e=1, u_z=2, E_z=3", "states": len(moments),
            "finite_d_states": sum(F(r["d"]) != 0 for r in moments), "d0_witnesses": 7,
            "all_literal_B5c_B5d_residuals_zero": True, "B6c_recovered_only_for_nonzero_d": True,
            "finite_d_satisfies_full_steady_uniform_continuity": False,
            "d0_determines_Tzz": False,
            "family_formula": "S_xz_yz = E_z-u_z*d; Qzz = (u_z^2-Tzz)*d; Tzz is any selected positive parameter",
            "d0_interpretation": "All selected temperatures have Qzz=0 and S=3 at d=0, but B6c is undefined. These are subsystem witnesses, not complete physical steady states."},
        "figures": 2,
        "artifacts": [{"path": name, "bytes": (output / name).stat().st_size,
                       "sha256": digest((output / name).read_bytes())} for name in artifacts],
        "limits": ["No numerical source field, particle distribution, SG operator or original code was obtained/reconstructed.",
                   "Window-centered residual products are an exact alternative definition, not proof of the convention actually used by the authors.",
                   "Finite-d families intentionally do not satisfy exact steady uniform-density continuity; only their d0 endpoint does.",
                   "No corrected reconnection rate, anomalous-force magnitude, heating or instability result is inferred.",
                   "No general-n manipulation of the literal B5 prefactors is asserted; normalized witnesses avoid that separate ambiguity.",
                   "Appendix E is not claimed erroneous."]}
    (output / "data/producer-results.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "SG_kernels": 4, "SG_cases": len(cases),
                      "temporal_charge_controls": len(temporal), "moment_states": len(moments),
                      "d0_witnesses": 7, "figures": 2, "source_operator_recovered": False}))


if __name__ == "__main__":
    main()
