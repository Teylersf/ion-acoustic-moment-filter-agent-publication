# Source editions, independent checks and scope

This computational study concerns Dion Li, Zhuo Liu and Nuno F. Loureiro, *Role of ion acoustic instability in magnetic reconnection*. The principal source is the final *Journal of Plasma Physics* **92**(1), E20 (2026), DOI [10.1017/S002237782510113X](https://doi.org/10.1017/S002237782510113X). The separately inspected preprint is [arXiv:2505.08983v1](https://arxiv.org/abs/2505.08983v1). This document is provenance and scope documentation, not the study manuscript.

## Verified source identities

| Edition | Pages | Bytes | SHA-256 |
|:---|---:|---:|:---|
| Supplied preprint and official versioned arXiv v1 PDF | 28 | 19,506,372 | ec0dab848877c079b103cb9f22f5efafddda3b7576a4955695bb12b19f2ffd60 |
| Official journal PDF | 30 | 18,816,710 | 0ad1cbf795a58958b6889bebdff355fd463fb343aadef84e12e9261e100d7fa0 |
| Local institutional copy, including an MIT report cover | 31 | 18,787,323 | 68162730eb647c578025e0697393eaeeb77d68c419c399a70c933222908d5587 |

The supplied PDF is byte-identical to [the official arXiv v1 PDF](https://arxiv.org/pdf/2505.08983v1). The official history listed only v1, submitted 13 May 2025 at 21:53:31 UTC, when checked on 29 October 2026. The journal was received 14 May 2025, revised 29 October 2025, accepted 25 November 2025 and published online 27 February 2026. Its year is 2026, despite the 2025 preprint filename.

The [official journal article](https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/role-of-ion-acoustic-instability-in-magnetic-reconnection/F7B49872B868515590E66A9DE494DB62) and [official journal PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/F7B49872B868515590E66A9DE494DB62/S002237782510113Xa.pdf/role-of-ion-acoustic-instability-in-magnetic-reconnection.pdf) were retrieved normally with HTTP 200. No human challenge or credential access was needed.

The institutional copy adds a PSFC/JA-25-49 cover. All 30 body pages have text matching the journal after Unicode normalization and removal of whitespace; 29 of the 30 decoded page-content streams also match exactly. This is not a claim of whole-PDF byte identity or complete resource equivalence, and the cover date is not another scientific edition.

Both official editions identify CC BY 4.0. Source PDFs, the source archive, publisher HTML, extracted article text and original figure images are not bundled as this study's original work. Any original-source file basenames in provenance records identify cached external evidence, not required bundled inputs. Attributed third-party material retains its rights.

## Complete reading and material final revisions

Both complete sources were read: all 28 preprint pages and all 30 journal pages, including appendices, footnotes, captions and references. The two internal independent reviews also report complete reading. These are AI-assisted internal checks, not independent human peer review. Selected critical equations and figures were inspected visually.

The journal makes scientific changes beyond repagination. Its Eq. (4.1), p.10, gives the uniform-flow Doppler shift

$$
\omega_{\rm DS}=\omega_{\rm Vlasov}\pm k u_{x,i,\max}.
$$

This replaces the preprint's MHD-compressional-mode comparison, Eqs. (4.1)-(4.5), pp.9-11, and revises Fig.6. The uniform nonrelativistic Doppler sign is a positive control in the independent calculator. The old MHD overlays are not alleged as errors in the final article.

The final article additionally justifies drifting Maxwellians at instability onset (p.3), clarifies the threshold-curve evaluation time (Fig.3, p.8), discusses near-X-point longitudinal limits of the linear comparison (p.11), limits the stated KP spectral agreement and discusses an electron plateau (p.12), qualifies out-of-plane IAI with a 3-D caveat (p.14), and explicitly labels its mass-ratio extrapolation speculative (p.17 and footnote 6). Its inflow-instability discussion is narrowed and expanded in Appendix C, pp.22-23. These changes and limitations are credited.

| Topic | Preprint locator | Final journal locator |
|:---|:---|:---|
| Maxwellian response | Eqs. (2.1)-(2.6), pp.2-3 | Eqs. (2.1)-(2.6), p.3 |
| Harris initialization and tables | Eqs. (3.1)-(3.2), p.4; tables pp.5-6 | Eqs. (3.1)-(3.2), p.5; tables p.6 |
| Anomalous terms | Eqs. (4.6)-(4.9), p.14 | Eqs. (4.2)-(4.4), p.14; (4.5), p.15 |
| X-point moment reduction | Eqs. (B4)-(B10), pp.18-19 | Eqs. (B4)-(B5a), p.19; (B5b)-(B10), p.20 |
| Continuity and edge inference | Eqs. (B13)-(B18), p.20 | Eqs. (B13)-(B15), p.21; (B16)-(B18), p.22 |
| Filtered momentum budget | Appendix D, pp.21-22 | Appendix D, Eq. (D2), p.23; procedure pp.23-24 |
| Solar-wind scale estimates | Eqs. (E1)-(E5), pp.22-23 | Eqs. (E1)-(E3), p.24; (E4)-(E5), p.25 |

## Retained moment finding and its limits

The final source assumes steady state and uniform density near the X-point and sets its in-plane velocity to zero. Continuity therefore sets

$$
d=\partial_xu_{ix}+\partial_yu_{iy}=0.
$$

The same steady uniform-density continuity is explicitly invoked as Eq. (B13), p.21. The source's printed density prefactors must not be silently repaired: the cross term in (B5c) lacks an additional density multiplier, while (B5d) uses the temperature divergence directly. The literal subsystem elimination below is therefore restricted to normalized n_i=m_i=e=1. Eliminating the off-diagonal temperature divergence between (B5c) and (B5d), without division, then gives

$$
H+(T_{i,zz}-u_{iz}^{2})d=0,
\qquad H=\partial_xq_{i,zzx}+\partial_yq_{i,zzy}.
$$

For d=0 this normalized subsystem requires H=0, rather than determining the temperature. Independently of that normalization, the displayed (B6c) divides by d, which is zero under the stated steady assumptions. Its subsequent zero-heat-flux use does not establish the quantitative estimate (B10b). The independent exact witnesses use n_i=m_i=e=1 and satisfy this moment subsystem and continuity with different positive temperatures; they are not complete kinetic or steady zero-heat-flux plasma solutions. The explicit density-convention addendum preserves the original note and distinguishes this normalized check from an unsupported arbitrary-density identity.

The source already acknowledges the failure of its xx/yy zero-heat-flux closure on p.21. That acknowledgment is credited. The finding does not refute its measured temperatures in Figs.8-9 or establish that an electric field cannot participate in thermal heating.

A separate qualification concerns (B17), p.22: differentiating and extending an X-point-only relation to the sheet edge needs a neighborhood closure. Edge equations retain advection and magnetic terms absent from the X-point reduction. This limits the displayed derivation of the range in (B18), rather than disproving measured inflow-direction heating.

## Filter convention: explicit counterargument retained

The final source defines a two-dimensional spatial Savitzky-Golay mean and fluctuation decomposition in Appendix D. It gives a qualitative scale-selection rationale and Fig.10's approximate reciprocal-window label, 0.22 d_e0^(-1). The polynomial order, exact point-count window, complete two-dimensional construction, edge treatment and discrete residual implementation were not recovered.

With a literal pointwise field residual f'=f-Gf, the full covariance

$$
G(nf)-(Gn)(Gf)
$$

generally differs from G(n'f'). The independent rational witnesses demonstrate the extra Leonard/cross terms and their effects on the printed drag and time-dependent covariance identities. The printed T and I definitions already retain full filtered products and remain positive controls.

There is a crucial alternative: subtract the same center mean throughout each evaluation window,

$$
\delta_x f(r)=f(x+r)-Gf(x).
$$

The weighted local product then equals the full covariance exactly for normalized weights, including Savitzky-Golay weights. The copied filter program explicitly verifies this alternative. Since source code is unavailable, the actual residual convention cannot be inferred. The source-specific issue is an operator-definition and reproduction gap, not proof that the hidden routine, Fig.10 amplitudes, reconnection rate or heating conclusions are wrong.

Interior derivative commutation is a positive control. An illustrative edge commutator is not attributed to the source's unspecified edge mode.

## Withdrawn and excluded candidates

The Appendix E mass-factor candidate is **withdrawn as an error**. If (E2) is written lambda/d_i >= X/R_some, existence of some scale below d_i requires X<R_some. A sufficient condition at every scale above d_e instead uses X<=R_some(d_e/d_i). Since d_e/d_i=sqrt(m_e/m_i), the latter recovers the mass factor printed in (E3). The phrase “at any scale” admits that universal interpretation. This is a positive quantifier clarification, not an alleged algebraic error. The independent JSON explicitly records withdrawn_as_error.

Maxwellian normalization, homogeneous-frame Doppler transformations and Harris/grid/CFL values also pass their bounded controls. A typical wavelength versus FWHM comparison, mildly relativistic proper velocities and exact finite-mass thresholds require qualifications; they do not establish errors in the original PIC data. None is promoted into a refutation of observed IAI, ion heating, irreversible entropy production or global reconnection dynamics.

## Independent components and execution provenance

Original notes and programs were copied byte for byte into:

- audit/independent-filter-review/
- audit/independent-moment-review/

Each directory preserves an original-run JSON under a distinct name. The moment review additionally preserves its exact original note as independent-review-original.md; its final independent-review.md and DENSITY_CONVENTION_ADDENDUM.md explicitly restrict the elimination to the normalized subsystem after checking the printed prefactors. The programs remain exact, unadapted copies and require no source PDFs or external accounts. They were actually run with C:/Python313/python.exe: the filter program uses the standard library, and the moment/dispersion program uses the recorded NumPy and SciPy environment. Both exit successfully with zero stderr. Their new run outputs match the original scratch receipts byte for byte in this recorded environment. Original producer hashes were not rewritten and scratch originals were not modified.

The detailed copy/run proof is audit/independent-review-copy-verification.json. source-provenance.json records source URLs, edition dates/hashes, original component hashes, exact-copy status and interpretation boundaries. No claim of bitwise reproducibility across arbitrary environments follows from this local equality.

## Availability and correction context

The arXiv source archive contains seventeen regular files: eleven figure PDFs and six manuscript/bibliography/class/support files. No runnable numerical analysis, simulation input deck or underlying PIC arrays were found in that package.

Both editions direct requests for supporting data to the corresponding author (preprint p.17; journal p.18). The OSIRIS 4.0 acknowledgment is not a case-specific code deposit. No public case-specific data/code/supplement link was identified in the inspected records, and no corresponding-author contact was made.

The original bounded correction check found no target-specific notice in the checked Crossref update fields and four targeted searches. This is not exhaustive proof of absence. The erratum for the different paper *A two-dimensional numerical study of ion-acoustic turbulence* is excluded from this paper's correction record.
