# Computational methods and limits

Author: Taylor Kalin.

The producer performs exact rational calculations and draws two synthetic
figures. It does not import an independent verification program. Its source
locators refer to the final journal edition of Li, Liu and Loureiro,
[10.1017/S002237782510113X](https://doi.org/10.1017/S002237782510113X), rather
than to equations removed or renumbered from the preprint.

## Fixed spatial filter

For normalized weights w, define Gf(x)=sum_r w_r f(x+r). The producer derives
each centered Savitzky–Golay kernel from exact polynomial least squares. With
integer offsets r and degree p, its Gram matrix is M_jk=sum_r r^(j+k).
Solving M a=(1,0,...,0) in rational arithmetic gives w_r=sum_j a_j r^j.
Reproduction moments through degree p and kernel symmetry are checked exactly.
The four declared synthetic window/degree pairs are (5,2), (7,3), (9,2) and
(5,4). They are not a recovery of the actual source operator.

Set N=Gn, F=Gf, n'=n-Gn and f'=f-Gf. The calculations distinguish

```text
C = G(n f) - N F
R = G(n' f')
W = sum_r w_r [n(x+r)-N(x)] [f(x+r)-F(x)]
```

W=C follows from normalization for these window-centered residuals. In general,
R need not equal C. Direct expansion gives C=R+K, with

```text
K = [G((Gn)(Gf))-(Gn)(Gf)] + G((Gn) f') + G(n' (Gf)).
```

The three terms are reported separately. Negative SG weights are allowed, so
these weighted covariances need not be nonnegative probability variances.
Every synthetic density and its central filtered value are positive. Constant
density/field controls, a five-point degree-four identity kernel, and a true
broadcast finite ensemble mean are retained as positive controls.

The exact five-point degree-two kernel is (-3,12,17,12,-3)/35. At x=0,
n=2+x² and f=x² give C=W=-72/35 and R=0. A weaker density variation,
n=2+x²/100, gives C=-18/875. For n=3+(-1)^x and f=(-1)^x, C=W=1056/1225
while R=2304/1225. Figure1 uses the unscaled quadratic and alternating cases;
all values are arbitrary dimensionless examples, not measured source fields.
A separable two-dimensional SG covariance on fields constant in y gives the
same values. This is one applicable 2D operator, not an identification of the
source's unspecified 2D fit.

Source Eqs.(4.2),(4.5) and(D2), pp.14–15 and23, motivate the normalized force
checks. The electric correction uses D_exact=-C_nE/N; no additional charge
factor belongs in D. An instantaneous temporal example uses E=B=u=0,
du/dt=f and div(P)=-m n f. It checks V_exact=m C_nf/(q N), with m=1 and both
charge signs. The denominator lies outside the time derivative. Residuals
recorded in CSV are explicitly left minus right of the normalized momentum
identity. These scalar force-balance controls are not full kinetic/Maxwell
solutions. The source's full-product T and I definitions are not replaced or
described as having the same residual-product issue.

The paper leaves actual kernel coefficients, degree, boundaries and residual
implementation unresolved. A window-centered implementation could already
produce the exact covariance. These examples therefore do not establish an
error in an unavailable postprocessing program, a revised anomalous amplitude
or a changed reconnection rate. No ideal brick-wall response is inferred from
a nominal window length.

## Normalized moment subsystem

For source B5c/d and B6c, p.20, define

```text
d = partial_x u_ix + partial_y u_iy
S = partial_x T_i,xz + partial_y T_i,yz
Qzz = partial_x q_i,zzx + partial_y q_i,zzy.
```

All witnesses fix n=m=e=1. This avoids assuming an unverified general-density
elimination of the literal printed prefactors. The two evaluated equations are

```text
Qzz + (Tzz+u_z²)d + 2u_z S = 2E_z u_z
E_z = S + u_z d.
```

Subtracting twice u_z times the momentum equation yields
Qzz+(Tzz-u_z²)d=0 without division. Nonzero d permits B6c's temperature ratio.
At d=0 it says only Qzz=0 and leaves Tzz undetermined by this subsystem.
Source B10b uses the divided estimate to motivate its temperature scaling;
B13, p.21, explicitly states the steady uniform-density incompressibility
condition. At a steady two-dimensional stagnation point, continuity also
requires d=0.

To expose the limiting order, choose u_z=2, E_z=3 and set
S=3-2d, Qzz=(4-Tzz)d. Seven positive rational temperature parameters,
1/4,1,2,4,13/3,7,10, are used. For each temperature, d takes both signs of
2^(-k), k=0,...,18, and zero. All 273 states satisfy the literal normalized
B5c/d subsystem exactly. The 266 nonzero-d cases recover their selected Tzz
when division is legitimate. At the seven zero-divergence endpoints, Qzz=0
and S=3 are the same while temperatures differ; B6c is recorded as undefined.
The Tzz=4 family is the zero-Qzz nonzero-divisor positive control.

Every finite-d path intentionally fails exact steady uniform-density
continuity, whose residual is reported. These are compatibility paths of a
moment subsystem, not complete steady distributions, full xx/yy/zz closures,
temperature predictions or solutions of the source simulation. No inference
about a measured variance, irreversible heating or the physical impossibility
of electric-field-related heating is made. The withdrawn Appendix E candidate
is not an error finding.

## Outputs

The data directory contains exact kernel weights, 20 covariance cases,
40 temporal charge controls, 273 moment states, source locators and a JSON
summary. All algebra remains Fraction-based; conversion to floating point is
restricted to plotting and explicitly labeled CSV display weights. The summary
binds its producer, artifact bytes and plotting environment. The producer
requires no source PDF, recovered field array, GPU, private path or network
after installation. Exact bytes across arbitrary library/font environments are
not promised.
