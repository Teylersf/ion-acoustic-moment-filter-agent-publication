"""Exact rational witnesses for finite-filter versus Reynolds covariances.

All fields and filters below are declared synthetic examples. No source data,
source program, external library, network, simulation or paper editing is used.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parent


def solve(matrix, rhs):
    a = [[F(x) for x in row] + [F(v)] for row, v in zip(matrix, rhs)]
    n = len(a)
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][k]
        a[k] = [x / scale for x in a[k]]
        for i in range(n):
            if i != k:
                factor = a[i][k]
                a[i] = [x - factor*y for x, y in zip(a[i], a[k])]
    return [row[-1] for row in a]


def local_weights(offsets, degree):
    """Unweighted polynomial least-squares estimate at coordinate zero."""
    gram = [[sum(F(x)**(i+j) for x in offsets)
             for j in range(degree+1)] for i in range(degree+1)]
    c = solve(gram, [1] + [0]*degree)
    return [sum(c[j]*F(x)**j for j in range(degree+1)) for x in offsets]


def centered_filter(window, degree):
    assert window > degree >= 0 and window % 2 == 1
    offsets = list(range(-(window//2), window//2+1))
    weights = local_weights(offsets, degree)
    for j in range(degree+1):
        assert sum(w*F(x)**j for x, w in zip(offsets, weights)) == (1 if j == 0 else 0)
    def filtered(field):
        @lru_cache(None)
        def apply(x):
            return sum(w*field(x+j) for j, w in zip(offsets, weights))
        return apply
    return offsets, weights, filtered


def covariance_record(n, field, G, point=0):
    N, mean = G(n), G(field)
    dn = lambda x: n(x)-N(x)
    df = lambda x: field(x)-mean(x)
    direct = G(lambda x: n(x)*field(x))(point)-N(point)*mean(point)
    residual_product = G(lambda x: dn(x)*df(x))(point)
    leonard = G(lambda x: N(x)*mean(x))(point)-N(point)*mean(point)
    cross1 = G(lambda x: N(x)*df(x))(point)
    cross2 = G(lambda x: dn(x)*mean(x))(point)
    missing = leonard+cross1+cross2
    assert direct == residual_product+missing
    assert N(point) > 0
    return dict(N=N(point), mean_field=mean(point), exact_covariance=direct,
                filtered_residual_product=residual_product, Leonard=leonard,
                cross_mean_density_residual_field=cross1,
                cross_residual_density_mean_field=cross2, missing_K=missing,
                D_exact=-direct/N(point), D_printed=-residual_product/N(point))


def main():
    filters = []
    moments = []
    for window, degree in [(5, 2), (7, 3), (41, 2), (55, 2)]:
        offsets, weights, G = centered_filter(window, degree)
        if window == 5:
            assert weights == [F(-3,35), F(12,35), F(17,35), F(12,35), F(-3,35)]
        # Quadratic fields are reproduced separately, but their product is not.
        n = lambda x: F(2+x*x)
        e = lambda x: F(x*x)
        row = covariance_record(n, e, G)
        centered_residual_product = sum(
            w*(n(x)-row["N"])*(e(x)-row["mean_field"])
            for x,w in zip(offsets,weights))
        assert centered_residual_product == row["exact_covariance"]
        row["window_centered_residual_product"] = centered_residual_product
        row["window_centered_covariance_exact"] = True
        assert row["filtered_residual_product"] == 0
        assert row["cross_mean_density_residual_field"] == 0
        assert row["cross_residual_density_mean_field"] == 0
        assert row["missing_K"] == row["Leonard"] != 0
        assert row["D_printed"] == 0 and row["D_exact"] != 0
        if window == 5:
            assert row["exact_covariance"] == F(-72,35)
            assert row["D_exact"] == F(36,35)
        # Static instant: u=B=0 and pressure gradient=nE balances raw momentum.
        gne = G(lambda x: n(x)*e(x))(0)
        static_exact_residual = -(row["mean_field"]-row["D_exact"]-gne/row["N"])
        static_printed_residual = -(row["mean_field"]-row["D_printed"]-gne/row["N"])
        assert static_exact_residual == 0
        assert static_printed_residual == row["missing_K"]/row["N"] != 0
        # Separate unsteady instant: E=B=u(t=0)=0, du/dt=e, gradP=-m*n*e.
        velocities = []
        for charge in [1, -1]:
            factor = F(1, charge)
            v_exact = factor*row["exact_covariance"]/row["N"]
            v_printed = factor*row["filtered_residual_product"]/row["N"]
            exact_residual = factor*row["mean_field"]+v_exact-factor*gne/row["N"]
            printed_residual = factor*row["mean_field"]+v_printed-factor*gne/row["N"]
            assert exact_residual == 0 and printed_residual != 0
            velocities.append(dict(mass=1, charge=charge, V_exact=v_exact,
                                   V_printed=v_printed, exact_balance_residual=exact_residual,
                                   printed_balance_residual=printed_residual))
        # A tensor-product 2D SG filter on y-independent fields gives the same witness.
        twod = sum(wx*wy*n(x)*e(x)
                   for x, wx in zip(offsets, weights) for y, wy in zip(offsets, weights))
        assert twod == gne
        filters.append(dict(window_points=window, polynomial_degree=degree,
                            offsets=offsets, weights=weights, fields="n=2+x^2, E=x^2",
                            covariance=row, static_exact_balance_residual=static_exact_residual,
                            static_printed_balance_residual=static_printed_residual,
                            velocity_instant_controls=velocities,
                            y_independent_tensor_product_2D_agrees=True))
        moments.append(dict(window=window, degree=degree,
                            reproduced_moments=list(range(degree+1)),
                            fourth_moment=sum(w*F(x)**4 for x,w in zip(offsets,weights))))

    _, _, G = centered_filter(5, 2)
    alternating = lambda x: F(1 if x % 2 == 0 else -1)
    n = lambda x: 3+alternating(x)
    cross_case = covariance_record(n, alternating, G)
    assert cross_case["exact_covariance"] == F(1056,1225)
    assert cross_case["filtered_residual_product"] == F(2304,1225)
    assert cross_case["missing_K"] == F(-1248,1225)
    assert cross_case["Leonard"] != 0
    assert (cross_case["cross_mean_density_residual_field"]
            + cross_case["cross_residual_density_mean_field"]) != 0
    h = G(alternating)(0)
    nonidempotence = G(G(alternating))(0)-G(alternating)(0)
    filtered_residual_mean = G(lambda x: alternating(x)-G(alternating)(x))(0)
    assert h == F(-13,35) and nonidempotence == F(624,1225)
    assert filtered_residual_mean == -nonidempotence != 0
    cross_case.update(alternating_mode_transfer=h,
                      G_squared_E_minus_G_E=nonidempotence,
                      G_of_residual_E=filtered_residual_mean)

    # Constants and the identity filter are positive controls.
    constant_controls = []
    for density, field in [
        (lambda x: F(3), lambda x: F(x**4)+alternating(x)),
        (lambda x: F(3)+alternating(x), lambda x: F(7)),
    ]:
        row = covariance_record(density, field, G)
        assert row["exact_covariance"] == row["filtered_residual_product"] == 0
        constant_controls.append(row)
    _, identity_weights, identity = centered_filter(5, 4)
    assert identity_weights == [0, 0, 1, 0, 0]
    identity_case = covariance_record(n, alternating, identity)
    assert identity_case["exact_covariance"] == identity_case["filtered_residual_product"] == 0

    # True ensemble averaging: resolved means are constants on the sample space.
    densities = list(map(F, [1, 2, 4, 5]))
    fields = list(map(F, [-3, 2, 0, 1]))
    avg = lambda values: sum(values)/len(values)
    N, E = avg(densities), avg(fields)
    ensemble_direct = avg([a*b for a,b in zip(densities,fields)])-N*E
    ensemble_residual = avg([(a-N)*(b-E) for a,b in zip(densities,fields)])
    assert ensemble_direct == ensemble_residual
    ensemble = dict(N=N, E=E, exact_covariance=ensemble_direct,
                    filtered_residual_product=ensemble_residual,
                    idempotent=True, mean_product_closed=True,
                    mean_residual_products_zero=True)

    # Printed T and I retain full products and remain exact by construction.
    n = lambda x: F(4)+alternating(x)
    u = lambda x: F(x*x+1)
    v = lambda x: F(x-1)
    b = lambda x: F(2*x+3)
    c = lambda x: F(x*x-2)
    N = G(n)(0)
    cross = lambda x: u(x)*b(x)-v(x)*c(x)
    mean_cross = G(u)(0)*G(b)(0)-G(v)(0)*G(c)(0)
    T = -G(lambda x:n(x)*cross(x))(0)/N+mean_cross
    assert mean_cross-T == G(lambda x:n(x)*cross(x))(0)/N
    diff = lambda f: lambda x: (f(x+1)-f(x-1))/2
    mean_flux = lambda x: G(n)(x)*G(u)(x)**2
    raw_flux = lambda x:n(x)*u(x)**2
    I = (G(diff(raw_flux))(0)-diff(mean_flux)(0))/N
    assert diff(mean_flux)(0)/N+I == G(diff(raw_flux))(0)/N
    full_product_controls = dict(T_identity_exact=True, I_identity_exact=True)

    # Translation-invariant interior filters commute with a centered difference.
    f = lambda x: F(x**7)+alternating(x)
    interior_commutator = G(diff(f))(0)-diff(G(f))(0)
    assert interior_commutator == 0
    # An illustrative polynomial-fit edge treatment is position dependent.
    points = list(range(9))
    values = [F(x**4)+(1 if x%2 == 0 else -1) for x in points]
    matrix = []
    for i in points:
        start = max(0,min(i-2,len(points)-5))
        indices = list(range(start,start+5))
        weights = local_weights([j-i for j in indices],2)
        matrix.append([weights[indices.index(j)] if j in indices else F(0) for j in points])
    apply = lambda vals:[sum(w*v for w,v in zip(row,vals)) for row in matrix]
    derivative = lambda vals:[vals[1]-vals[0]]+[(vals[j+1]-vals[j-1])/2
                        for j in range(1,len(vals)-1)]+[vals[-1]-vals[-2]]
    gd,dg = apply(derivative(values)),derivative(apply(values))
    edge_commutator = [a-b for a,b in zip(gd,dg)]
    assert any(edge_commutator) and edge_commutator[4] == 0

    result = dict(
        schema_version=1, status="pass",
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        environment=dict(python=platform.python_version(),implementation=platform.python_implementation(),
                         dependencies="Python standard library; exact fractions"),
        source=dict(arxiv="2505.08983v1",journal_DOI="10.1017/S002237782510113X",
                    journal_PDF_SHA256="0ad1cbf795a58958b6889bebdff355fd463fb343aadef84e12e9261e100d7fa0",
                    definitions="Journal Eqs. (4.2)-(4.5), pp. 14-15; Appendix D, p. 23.",
                    final_Fig10_filter_label="kmax approximately 0.22 de0^-1",
                    polynomial_order_reported=False,exact_window_point_count_reported=False,
                    two_dimensional_spatial_filter_reported=True,
                    tensor_product_or_full_2D_polynomial_implementation_reported=False,
                    boundary_mode_reported=False,
                    actual_pointwise_or_window_centered_residual_code_unknown=True,
                    numerical_witness_is_source_filter_reconstruction=False),
        synthetic_filters=filters,SG_reproduction_controls=moments,
        nonzero_cross_term_case=cross_case,constant_controls=constant_controls,
        identity_filter_positive_control=identity_case,ensemble_Reynolds_positive_control=ensemble,
        full_filtered_product_positive_controls=full_product_controls,
        derivative_controls=dict(interior_centered_convolution_commutator=interior_commutator,
                    illustrative_edge_mode="Local quadratic fits to first/last five points; centered difference inside and one-sided endpoint differences.",
                    illustrative_edge_commutator=edge_commutator,actual_source_edge_mode_unknown=True),
        limits=[
            "Fields are dimensionless synthetic algebra controls, not PIC data or measured source terms.",
            "The discrepancy witness uses pointwise field residuals f-Gf. A window-centered residual f(x+r)-Gf(x) gives the exact covariance and is a viable hidden implementation.",
            "The 41/55-point examples are illustrative choices, not inferred author window lengths or polynomial orders.",
            "A y-independent tensor-product 2D control is one declared implementation, not identification of the author's 2D filter.",
            "An actual finite-filter discrepancy in plotted values cannot be quantified without data and the exact filtering implementation.",
            "Scale separation may justify approximation; no quantitative error bound is established here.",
            "No source paper, queue, repository, publication or external account is mutated."])
    def encode(value):
        if isinstance(value,F):return {"exact":str(value),"float":float(value)}
        if isinstance(value,list):return [encode(x) for x in value]
        if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
        return value
    output=ROOT/"filter-identity-checks.json"
    output.write_text(json.dumps(encode(result),indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(dict(status="pass",synthetic_SG_filters=len(filters),
                          isolated_V_charge_controls=2*len(filters),nonzero_cross_witnesses=1,
                          constant_controls=len(constant_controls),Reynolds_ensemble_controls=1,
                          identity_controls=1,full_product_controls=2,
                          interior_and_edge_derivative_controls=2,
                          report_sha256=hashlib.sha256(output.read_bytes()).hexdigest())))


if __name__=="__main__":
    main()
