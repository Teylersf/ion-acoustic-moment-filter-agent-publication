# Finite spatial filtering and the printed momentum decomposition

This is a bounded independent check of Li, Liu and Loureiro, JPP 92, E20 (2026), DOI 10.1017/S002237782510113X, using the verified 30-page journal PDF, SHA256 0ad1cbf795a58958b6889bebdff355fd463fb343aadef84e12e9261e100d7fa0. The earlier arXiv v1 contains the same definitions under different numbering. This note does not reconstruct a source numerical analysis, quantify a plotted discrepancy or reject its reconnection/heating conclusions.

## 1. What averaging is actually specified

Journal Section 4.4.2, pp.14-15, defines D, T, I and V in Eqs. (4.2)-(4.5). Appendix D, p.23, first writes a formal mean-plus-fluctuation decomposition Q = <Q> + delta Q and presents Eq. (D2) as an equality. It subsequently specifies a two-dimensional spatial average implemented with a Savitzky-Golay filter. Thus the reported numerical operator is a finite spatial filter, not an explicitly specified ensemble expectation.

The paper gives a qualitative reason for the selected scale: remove the fastest-growing ion-acoustic fluctuations and reduce noise. This is evidence of an intended separation of scales, and should be acknowledged. It is not an explicit assertion of Reynolds factorization identities or a quantitative error bound for replacing finite-filter covariances by products of residuals. The mean/fluctuation description calls the means quasi-stationary, but temporal slowness alone does not imply the needed spatial product identities.

There is an important alternative convention. An unpublished routine could subtract the mean at the evaluation center from every point in that center's window, defining delta_x f(r) = f(x+r)-Gf(x), rather than constructing the pointwise field residual f(y)-Gf(y). For any normalized weights, including Savitzky-Golay weights, the weighted product of those window-centered residuals equals G(nf)(x)-Gn(x)Gf(x) exactly. The source provides no numerical code that distinguishes these implementations. The calculations below test the literal pointwise-field residual reading; they do not prove that the hidden routine used that reading. This is an operator-definition and reproduction gap, not evidence by itself of an incorrect hidden implementation.

A high-resolution view of final Fig.10, p.15, gives k_max approximately 0.22 d_e0^(-1) in all three lower panels. The caption calls k_max the reciprocal of the window length. No polynomial degree, exact number of window points, tensor-product versus full two-dimensional fit, boundary treatment or derivative implementation is specified in the inspected article/source package. The approximate physical length would be 4.55 d_e0 under that stated reciprocal convention. Tables 1-2 would place that length near 40.5 grid spacings for the two colder-ion runs and 54.5 for the equal-temperature run. These rounded values do not determine the actual point count: a window can be described by point count or endpoint span, and the plotted number is approximate. The 41/55-point examples below are explicitly illustrative, not an identification of the source filter.

## 2. Exact identity for an arbitrary fixed linear filter

Let G be a normalized linear spatial operator, fixed in time. Define

$$
N=G n,\qquad U=G u,\qquad F=G E,\qquad H=G B,\qquad
f'=f-Gf,
$$

with N positive at the point of evaluation. Vector field products are componentwise where appropriate. The exact density-field covariance is

$$
C_{nf}=G(nf)-N\,Gf.
$$

The source residual-product expression instead uses

$$
R_{nf}=G(n'f').
$$

Expansion of the product, without using any Reynolds assumption, gives

$$
C_{nf}=R_{nf}+K_{nf},
$$

$$
K_{nf}=
\underbrace{G(N\,Gf)-N\,Gf}_{\text{Leonard term}}
+\underbrace{G(Nf')+G(n'Gf)}_{\text{cross terms}}.
$$

These are algebraic terms, not a new physical closure. A finite filter generally does not make them vanish. In particular, G f' = Gf - G^2 f need not be zero. Merely writing f = Gf + f' is always possible and does not establish a Reynolds decomposition. Idempotence alone would also not guarantee the required mean-product factorization for an arbitrary spatial projection.

Under the different window-centered convention, define R_center(x) = sum_r w_r[n(x+r)-N(x)][f(x+r)-Gf(x)]. Normalization sum_r w_r=1 gives R_center=C_nf directly. No Leonard/cross correction is then missing from a D or V computed with that covariance. This positive alternative is verified for every synthetic filter below.

For the electric force, exact filtering and division by the filtered density require

$$
D_{\rm exact}
=-\frac{G(nE)-NF}{N}
=D_{\rm printed}-\frac{K_{nE}}{N},
\qquad
D_{\rm printed}=-\frac{R_{nE}}{N}.
$$

No factor of charge is inserted into D: this follows the source's electric-field units after division of momentum by qN. The denominator throughout is N = Gn, not raw n and not an average of the ratio.

For the temporal momentum term, time-independent G commutes with the time derivative. Therefore

$$
V_{\rm exact}
=\frac{m}{qN}\partial_t\left[G(nu)-NU\right]
=V_{\rm printed}+\frac{m}{qN}\partial_tK_{nu},
\qquad
V_{\rm printed}=\frac{m}{qN}\partial_tR_{nu}.
$$

The factor 1/N is outside the derivative, exactly as in the printed definition. The charge q retains its sign, so the added V term changes sign between otherwise identical positive- and negative-charge controls.

## 3. Two other printed terms already retain the full products

It would be incorrect to describe all four anomalous terms as missing finite-filter products. Source Eq. (4.3) defines

$$
T_{\rm printed}=-\frac{G[n(u\times B)]}{Nc}
+\frac{U\times H}{c}.
$$

This is already an exact difference of the full magnetic product and the chosen resolved product, for arbitrary G.

Similarly, Eq. (4.4) defines

$$
I_{\rm printed}=\frac{m}{qN}
\left[G\nabla\cdot(nuu)-\nabla\cdot(NUU)\right].
$$

As written, this is already an exact transport difference. One need not commute G with a spatial derivative to establish this identity. The printed pressure term also retains G(div P), rather than assuming div(GP). Both are useful positive controls on the scope of the finding.

With the source's T and I left intact, the exact normalized momentum equation is its Eq. (D2) with D_exact and V_exact substituted. Equivalently, if L_print and R_print denote the complete printed left and right sides, an underlying field satisfying the primitive momentum balance obeys

$$
L_{\rm print}-R_{\rm print}
=\frac{K_{nE}}{N}
-\frac{m}{qN}\partial_tK_{nu}.
$$

Neither omitted term can generically be absorbed into the printed T or I, because those definitions already use their full magnetic/transport products.

## 4. Exact rational counterexamples and positive controls

The companion standard-library program derives centered Savitzky-Golay coefficients directly from unweighted local polynomial least squares. It verifies polynomial-reproduction moments and uses exact fractions; no floating-point tolerance is needed for an equality assertion. It runs four declared examples: window/degree pairs (5,2), (7,3), (41,2), (55,2). A tensor-product two-dimensional extension on fields constant in the second coordinate gives the same results. None is claimed to reproduce the source's unknown operator.

The five-point quadratic coefficients are

$$
\frac1{35}(-3,12,17,12,-3).
$$

For the synthetic, positive density n(x)=2+x^2 and electric field E(x)=x^2, evaluated at x=0, this filter reproduces each field exactly, so both residuals vanish. Yet their product contains x^4, which is not reproduced:

$$
N=2,\qquad R_{nE}=0,\qquad
C_{nE}=K_{nE}=-72/35.
$$

Consequently, D_printed=0 while D_exact=36/35. The discrepancy is entirely the Leonard term; cross terms vanish in this control.

The window-centered residual product instead gives -72/35, exactly the full covariance, for this same example. Thus the synthetic data distinguish residual conventions but do not identify which convention the source program implemented.

This can also test the complete normalized momentum identity without pretending to construct a PIC plasma. At a static instant, take u=B=0 and an analytic pressure gradient div P = q n E. The primitive momentum equation is then balanced pointwise. Filtering that balance gives zero residual with D_exact and a nonzero residual with D_printed. On a finite interval an additive pressure constant can keep the synthetic pressure positive. These arbitrary dimensionless fields establish an algebraic counterexample, not a measured anomalous resistivity or a self-consistent kinetic/Maxwell solution.

A separate instantaneous control sets E=B=u=0, du/dt=x^2 and div P=-m n x^2. This isolates V while balancing the primitive momentum equation at that instant. For m=q=1, V_printed=0 and V_exact=-36/35; q=-1 reverses the latter sign. All eight charge controls across the four filters close with the exact covariance and fail with the residual-only expression.

A non-polynomial control uses n=3+(-1)^x and E=(-1)^x. It has positive raw and filtered density. For the same five-point filter,

$$
C_{nE}=1056/1225,\qquad
R_{nE}=2304/1225,\qquad K_{nE}=-1248/1225.
$$

Here both the Leonard and cross contributions are nonzero. The alternating-mode transfer is -13/35, and G^2 E - GE = 624/1225 at the center, explicitly demonstrating that the filtered residual need not have zero mean.

The following controls pass exactly:

- Constant density or constant electric field gives zero covariance and zero residual-product covariance.
- The interpolatory five-point degree-four identity operator has no residual or covariance.
- A genuine finite ensemble average, broadcast over its sample space, satisfies the Reynolds factorization and yields identical full and residual-product covariances.
- The printed full-product T and I definitions recover their corresponding filtered primitive terms.

An ensemble expectation is therefore a valid setting for the familiar formulas; the counterexample is not a rejection of Reynolds averaging.

## 5. Derivatives and boundaries

For a translation-invariant interior convolution and a centered finite-difference derivative, the two operators commute. An exact rational control verifies this positive result. The missing K terms persist even in this favorable case: they are not a boundary artifact.

A separate illustrative edge operator fits a local quadratic to the first or last five points and evaluates it at an edge point. Its position-dependent matrix does not commute with the chosen finite-difference derivative near boundaries, although the sufficiently interior comparison agrees. This is not evidence that the source used that edge mode or suffered its commutator. If an implementation replaces G(div P) by div(GP), or similarly rearranges the printed I term, such commutators must be assessed for that actual implementation. If G itself changes with time, a further time-filter commutator is needed; no such time dependence is presumed here.

## 6. Supported conclusion and unresolved magnitude

The source clearly declares finite spatial Savitzky-Golay filtering and a qualitative scale-selection rationale. It does not provide a quantitative scale-separation estimate that makes the printed residual-only D and V exact. For a generic such filter, its claimed exact momentum decomposition requires K terms or an explicitly justified approximation.

This last statement is conditional on pointwise field residuals. A window-centered implementation would recover the exact covariances without those corrections. Since the operator and code details needed to distinguish them are unavailable, the source-specific supported conclusion is an unresolved definition/reproduction gap. It is not proof that the authors' numerical routine or plotted anomalous terms are incorrect.

This is a verified distinction between two mathematical quantities. It does not establish the size, sign or domain average of the difference in Fig.10, prove a changed reconnection rate, or refute ion heating. Those questions need the actual density/electric/velocity data, exact filter coefficients and window/order/edge choices, time differencing, and a readback of the implemented definitions. The published request-based data route is a limitation on checking that magnitude, not a reason to infer an adverse numerical result.
