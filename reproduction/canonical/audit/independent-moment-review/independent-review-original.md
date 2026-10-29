# Independent scientific review of the ion-acoustic reconnection paper

## Coverage and bounded verdict

Read the complete 30-page journal version, JPP 92(1), E20 (2026), DOI
10.1017/S002237782510113X, and the complete 28-page arXiv:2505.08983v1,
including captions, footnotes, appendices and references. Critical final
equations were also checked visually on pp.3,14-15,19-20 and23-24. The journal
is the target of the conclusions below. No original PIC input program,
field array, particle trajectory or execution was reconstructed.

There is one firm source-level derivation problem in Appendix B: the
temperature estimate uses a division by a divergence that the stated
steady-state assumptions set to zero. A second substantive issue concerns
the precise interpretation of the Savitzky-Golay mean/fluctuation operator.
The literal filtered-field interpretation does not give the asserted exact
momentum budget, but a different window-centered covariance interpretation
can repair it. The unavailable implementation prevents assigning that
particular computational error to the authors. Neither finding alone
disproves the reported measured heating or small anomalies.

The main Maxwellian dispersion and normalization checks are positive.
Approximate finite-mass thresholds, mildly relativistic proper velocities,
finite-width arguments and causal heating language need qualifications;
they do not by themselves supply demonstrated errors in the final PIC data.

## 1. Positive dispersion, frame and normalization controls

With v_th=sqrt(T/m), the sqrt(2) in the plasma-dispersion argument and the
Debye susceptibility in final Eq.(2.4), p.3, have the usual consistent
Maxwellian normalization. In particular, if Z denotes the Landau-continued
plasma function, the paper's Z_p+i Z_Delta equals zeta Z(zeta). Four
real/complex arguments in the independent calculator confirm that identity.
Reading omega as complex gives a consistent dispersion relation; its p and
omega notation does not establish that the original solver dropped growth.

For constant nonrelativistic drifts, shifting both species by U_i transforms
omega to omega-k U_i without changing the relative drift. Three complex
frequency controls confirm this dielectric identity. Final Eq.(4.1), p.10,
therefore has the correct uniform-flow Doppler sign. The final Fig.6 caption
and p.11 discussion acknowledge geometric, magnetic, electromagnetic and
nonlinear limits. The preprint's earlier MHD-mode interpretation in its
Eqs.(4.1)-(4.5), pp.9-11, is replaced in the journal; it is not a final-paper
error to report again.

The Harris balance and omega_pe/Omega_ce=2 imply
T_e/(m_e c^2)=1/[8(1+T_i/T_e)]. This reproduces the final Table2 thermal
speeds/debye ratios 0.350,0.337,0.250. The listed grids reproduce the quoted
Debye resolution, and the two-dimensional electromagnetic CFL numbers are
below one. No factor-of-two discrepancy is demonstrated there.

Independent real-marginality calculations of the same homogeneous drifting
Maxwellians give U_d/c_s=0.681520 at T_i/T_e=0.02 and 1.354021 at0.1 for
m_i/m_e=100, agreeing with the paper's 0.68 and1.36. For the cold finite-k
case, k lambda_De(local)=1.27554. Explicitly converting the prescribed
n_b=0.2 n0 to initial-density Debye units gives
k lambda_De0/(2pi)=0.090788, matching its reported0.09. This is a useful
positive density-normalization control, not evidence of a failed Fig.1.

The same marginal controls at mass ratio1836 give 0.724051 and2.412126,
respectively. Thus an exact finite-mass threshold is not mass independent.
Appendix A's mass-free expression is an approximation using an approximate
critical drift, not a replacement for solving Eq.(2.4). Its qualitative cold
finite-k trend can persist while thresholds change. The paper explicitly
labels its broader mass-ratio extrapolation speculative, so these controls
do not disprove that speculation or quantify a change in PIC saturation.

## 2. Firm Appendix B derivation gap: division by zero

Final pp.19-20 assume steady state and uniform density near the x-point;
Eq.(B4) also sets the in-plane ion velocity to zero there. The continuity
equation consequently requires

    d = partial_x u_ix + partial_y u_iy = 0.

Even without uniform density, exact steady continuity at this two-dimensional
stagnation point gives the same result. The paper explicitly uses steady
uniform-density continuity again as incompressibility in Eq.(B13), p.21.

Combining the printed zz raw-moment equation (B5c) and z momentum equation
(B5d), **without division**, gives

    div(q_izz) + n_i (T_i,zz - m_i u_iz^2) d = 0.

For d=0 this states only div(q_izz)=0. It does not determine T_i,zz. Equation
(B6c), p.20, instead divides by d; its zero-heat-flux use to derive (B10b)
is a 0/0 step under the assumptions just made. Two exact rational witnesses
in the calculator satisfy continuity and the B5c/B5d zz subsystem with the
same u_iz=2, m=n=e=1, E_z=3, off-diagonal temperature divergence3 and zero
zz heat-flux divergence, while T_i,zz can be1 or7. Neither need equal4.

These witnesses are expressly a moment-subsystem check, not a claim of a
complete physical steady zero-heat-flux solution. The authors themselves
recognize that their xx/yy zero-heat-flux closure fails, on p.21. That
acknowledgment is credited; it does not supply a missing nonzero divisor for
the zz estimate. A quasi-steady calculation could retain density/pressure
time derivatives or heat flux, but their limiting orders would have to be
specified before inferring a temperature from that ratio.

The central temperature is a velocity variance, whereas m u_iz^2 is a bulk
drift-energy scale. An electric field can ultimately cause thermal heating
through inhomogeneous dynamics or mixing, but bulk acceleration alone does
not determine that variance. Thus the measured Fig.8/9 temperatures and an
E_z-related heating mechanism are not refuted. The particular quantitative
justification (B10b) is not established by the printed derivation.

There is a separate spatial-closure step in (B17), p.22: the paper writes
the edge gradient partial_y T_i,zz|delta as approximately
2 m_i u_iz,delta partial_y u_iz|delta, citing (B6c). Even if (B6c) had been
valid at the X-point, an identity at one point cannot be differentiated and
continued to the sheet edge without a neighborhood closure. The X-point
reduction uses u_iy=0 and B=0, whereas the edge equations (B12) explicitly
retain inflow advection and B_x terms. Thus (B17) needs an additional
assumption beyond the printed X-point derivation. This does not refute the
physical T_i,yy heating or its measured values; it limits the claimed
derivation of the quantitative range (B18).

Corresponding preprint locators are AppendixB pp.18-20. This issue persists
in the final article; it is not a complaint about a removed preprint claim.

## 3. Spatial-filter covariance: exact gap and an explicit counterargument

Final Eqs.(4.2),(4.5), pp.14-15, use filtered products of fluctuations for
drag and the fluctuating-flow term. AppendixD/D2, p.23, says the mean is a
two-dimensional spatial Savitzky-Golay filter. Let G be a fixed normalized
linear spatial filter and interpret the displayed field decomposition in
the usual pointwise way, delta f=f-Gf. Then in general

    G(delta f delta g) != G(fg)-(Gf)(Gg).

For example, take the exact five-point quadratic Savitzky-Golay weights
(-3,12,17,12,-3)/35. Set n(x)=2+x^2/100 and E(x)=x^2 on the extended integer
stencil. This filter reproduces each quadratic, so delta n=delta E=0.
At the stencil center, nevertheless,

    G(nE)-(Gn)(GE) = -18/875,     G(delta n delta E)=0.

This is an exact rational calculation, not roundoff. Set u=B=0, q=1, and
P'=nE. The unfiltered first-moment force balance is zero. A positive pressure
can be chosen throughout the finite nested stencil, for example
P=100+(2/3)x^3+x^5/500 for integer x between-4 and4. The exact filtered
electric and pressure forces still cancel. Substituting the fluctuation
product in displayed D2 instead leaves a residual9/875 at the center.
A one-dimensional field independent of y supplies the same counterexample
to an applicable separable two-dimensional SG filter.

Under that interpretation, an exact repair is to use

    D* = -[G(nE)-(Gn)(GE)]/(Gn),
    V* = m/[q(Gn)] partial_t [G(nu)-(Gn)(Gu)].

For a fixed time-independent filter these preserve the averaged momentum
identity with the already difference-of-products definitions of T and I.
The exact constant-field and genuine global Reynolds-mean controls pass.
Finite SG filters also have a frequency response rather than an automatic
brick-wall cutoff at the reciprocal window length; attenuation should be
reported instead of inferred solely from a nominal cutoff.

**Important alternative interpretation:** define residuals separately for
each evaluation window, delta f_x(r)=f(x+r)-Gf(x), using the same central
mean throughout that window. Then their weighted local product *does* equal
G(fg)-(Gf)(Gg). This differs from applying G to the product of two pointwise
residual fields. The paper does not provide enough discrete implementation
detail to determine which was actually used. Its cutoff labels are not an
exact kernel/polyorder/boundary specification. Therefore the witness proves
that the formal filtered-field identity is not automatic, and motivates an
operator definition/budget-closure test. It does **not** prove that hidden
postprocessing violated the budget or that published anomalous amplitudes
must become large after correction. A methods clarification and executable
filter/budget check are needed before making those numerical claims.

Corresponding preprint definitions are Eqs.(4.6),(4.9), p.14, and AppendixD
pp.21-22. Their journal renumbering is respected here.

## 4. Qualifications not promoted to decisive errors

**Appendix E mass-factor candidate withdrawn.** An initial suspicion that
E3 loses a mass-ratio factor is not a demonstrated error. Write E2, p.24,
as lambda/d_i >= X/R_some, with X=sqrt(T_e) T_i. Existence of *some*
lambda<d_i requires X<R_some. A sufficient condition at *every* scale
between d_e and d_i instead requires X<=R_some d_e/d_i. Since
d_e/d_i=sqrt(m_e/m_i), the latter is exactly the printed E3, including its
m_i^(3/2)/m_e factor. The phrase "at any scale" admits that universal
interpretation. Two mass-ratio controls verify this identity and examples
that permit some but not every scale. This is a positive quantifier
clarification, not an error finding. The assumed kinetic-Alfven scale
interval and quantifier should be kept explicit. E4 also follows from its
preceding scalings under those assumptions.

- The cold-ion critical-drift exception is already stated in the final
  footnote on p.4. The phrase “of order the sound speed” is not an exact
  lower bound across every temperature or mass ratio.
- At a proper velocity u_x=0.7c with no transverse component, the stated
  Lorentz factor1.22 is correct; the ordinary velocity is about0.573c.
  Using a nonrelativistic dispersion is an acknowledged approximation,
  potentially material to precision but not a proven failure of onset.
- At the specific typical k=0.05(2pi/lambda_De) quoted on p.23, wavelength
  is20 lambda_De. Table2 gives6.74de and7.00de for the two cold cases,
  rather than a complete wavelength within the stated5de FWHM. But their
  footnote7 allows higher marginal k, and FWHM is not the full mode support.
  This is a local numerical qualification, not proof that inflow IAI cannot
  exist or that a finite current layer has a hard wavelength exclusion.
- A rise of a central second moment supports kinetic temperature broadening;
  it does not on its own prove irreversible entropy production or isolate
  a unique heating mechanism. The source does not supply that stronger
  entropy claim, and it explicitly separates out-of-plane heating from IAI.
- Vanishing mean anomalous force need not imply vanishing mean work because
  velocity-force correlations can remain. The source also compares direct
  reconnection-rate histories, so force averaging alone must not be treated
  as the entire numerical evidence. No raw budget was available to assess
  causal effect sizes or a revised global reconnection rate.

## Reproducible controls and decision boundary

`verify_source_identities.py` and `source-identity-checks.json` contain the
normalization, analytic plasma-function, uniform-frame, finite-mass marginal,
exact rational SG, zz-subsystem and Appendix E quantifier checks. The JSON
explicitly marks the initial Appendix E mass-factor candidate withdrawn.
Python/NumPy/SciPy versions and
the verifier SHA are recorded. There are no PIC reruns or recovered source
fields. The full article and its data-availability statement are primary
context, not a claim that data were acquired by request.

A bounded correction to AppendixB's quantitative derivation is warranted
mathematically. The filter issue is conditional on an implementation
interpretation and should be presented with its exact-covariance repair and
alternative, not as proven corruption of the source calculations. A broad
paper claiming that the observed IAI, ion heating or weak global anomaly
has been disproved would be unsupported by this review.
