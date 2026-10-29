"""Independent bounded controls for the journal's definitions; no PIC rerun."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import math
import platform

import numpy as np
import scipy
from scipy.optimize import brentq, minimize_scalar
from scipy.special import dawsn, erfi, wofz

HERE=Path(__file__).resolve().parent


def SG(fun,x=0):
    # Exact centered five-point quadratic Savitzky-Golay least-squares filter.
    return sum((w*fun(x+k) for k,w in zip(range(-2,3),map(F,[-3,12,17,12,-3]))),F(0))/35


def Z(z):
    return 1j*math.sqrt(math.pi)*wofz(z)


def dielectric(omega,k,ue,ui,tau,mu):
    ve=1.;vi=math.sqrt(tau/mu)
    ze=(omega-k*ue)/(math.sqrt(2)*k*ve)
    zi=(omega-k*ui)/(math.sqrt(2)*k*vi)
    return 1+(1+ze*Z(ze))/k**2+(1+zi*Z(zi))/(tau*k*k)


def marginal_cold_branch(tau,mu):
    # At real marginal frequency, write zi=v_phase/(sqrt2 vi),
    # ze=-y. The exact imaginary part gives y exp(-y^2)=zi exp(-zi^2)/tau.
    # The lower-y branch is the only one relevant to the sub-electron-thermal
    # threshold here; the other y>=1/sqrt2 branch has Ud>=ve.
    peak=1/math.sqrt(2*math.e)
    lower=brentq(lambda x:x*math.exp(-x*x)/tau-peak,1.,10.)
    def y(x):
        target=x*math.exp(-x*x)/tau
        return brentq(lambda yy:yy*math.exp(-yy*yy)-target,0.,1/math.sqrt(2),xtol=1e-15)
    def k2(x):
        yy=y(x)
        return -(1-2*yy*dawsn(yy)+(1-2*x*dawsn(x))/tau)
    upper=brentq(k2,lower+1e-9,20.)
    def drift(x):
        return math.sqrt(2*tau/mu)*x+math.sqrt(2)*y(x)
    result=minimize_scalar(drift,bounds=(lower+1e-8,upper),method='bounded',options={'xatol':1e-13})
    # Explicitly compare the permitted boundary, which is the long-wave
    # threshold for the warmer control rather than an interior minimum.
    x=min([float(result.x),upper],key=drift)
    U=drift(x);cs=math.sqrt((1+3*tau)/mu)
    assert U<1  # excludes the unexamined upper-y electron-thermal branch
    kk=max(0.,k2(x));phase=math.sqrt(2*tau/mu)*x
    ze=-y(x)
    susceptibility=1+ze*Z(ze)+(1+x*Z(x))/tau
    # These normalized fields use local lambda_De. The separately shown
    # n_b/n0=.2 conversion is explicit, not inferred as the figure's convention.
    return {'Ti_over_Te':tau,'mass_ratio':mu,'Ud_over_vth_e':U,
        'Ud_over_cs':U/cs,'phase_over_vth_e':phase,'zi':x,'minus_ze':y(x),
        'k_lambda_De_local':math.sqrt(kk),
        'k_lambda_De_initial_over_2pi_if_density_is_point2':math.sqrt(kk/5)/(2*math.pi),
        'marginal_ion_acoustic_branch':'lower electron-resonance branch; exact Maxwellian marginal susceptibility',
        'finite_k':bool(kk>1e-10),
        'absolute_k_squared_epsilon_marginality_residual':abs(kk+susceptibility),
        'absolute_dielectric_residual':abs(dielectric(phase*math.sqrt(kk),math.sqrt(kk),U,0,tau,mu)) if kk>1e-10 else None}


def main():
    if not __debug__:
        raise RuntimeError('Run without -O so checks remain enabled')
    # Positive normalization controls from the stated Harris equilibrium.
    normalization=[]
    for tau,Nx,Ny,Ly,dt in [(.02,2848,2136,24,.0786),(.1,2848,2136,24,.0786),(1.,3840,1920,16,.0583)]:
        ve=math.sqrt(1/(8*(1+tau)))
        dx=320/Nx;dy=Ly*10/Ny
        normalization.append({'Ti_over_Te':tau,'vth_e_over_c':ve,'lambda_De_over_de0':ve,
            'dx_over_lambda_De':dx/ve,'dy_over_lambda_De':dy/ve,
            'electromagnetic_CFL_2D':dt*math.sqrt(dx**-2+dy**-2),
            'wavelength_over_de0_at_k_normalized_point05':20*ve,
            'wavelengths_within_5de0_FWHM_at_that_typical_k':5/(20*ve)})
        assert dt*math.sqrt(dx**-2+dy**-2)<1
    # Check the analytic plasma function, including a complex-frequency point.
    function_checks=[]
    for z in [.2+0j,1.3+.4j,-.8+.2j,2.-.1j]:
        split=math.sqrt(math.pi)*z*np.exp(-z*z)*(1j-erfi(z))
        error=abs(split-z*Z(z))
        assert error<2e-14
        function_checks.append({'z':[z.real,z.imag],'absolute_error':error})
    frames=[]
    for omega,k,ud,ui in [(.025+.003j,.8,.07,.01),(.04+.001j,1.2,.1,-.015),(.008+.002j,.5,.06,.02)]:
        moving=dielectric(omega,k,ud+ui,ui,.02,100)
        rest=dielectric(omega-k*ui,k,ud,0,.02,100)
        error=abs(moving-rest)
        assert error<2e-12
        frames.append({'omega':[omega.real,omega.imag],'k':k,'ion_drift':ui,'relative_drift':ud,'dielectric_frame_identity_absolute_error':error})
    # A purely local, exact-rational finite-filter counterexample. The full
    # polynomial fields are defined beyond every nested filter stencil.
    n=lambda x:F(2)+F(x*x,100)
    E=lambda x:F(x*x)
    delta_n=lambda x:n(x)-SG(n,x)
    delta_E=lambda x:E(x)-SG(E,x)
    covariance=SG(lambda x:n(x)*E(x))-SG(n)*SG(E)
    residual_product=SG(lambda x:delta_n(x)*delta_E(x))
    assert covariance==-F(18,875) and residual_product==0
    # Static first-moment balance q*n*E=P': choose P'=nE and u=B=0.
    # Pointwise momentum is exactly zero. With q=m=1 the displayed D2
    # leaves this nonzero electric/pressure residual after the SG filter.
    pressure_gradient=lambda x:n(x)*E(x)
    exact_force=SG(lambda x:n(x)*E(x))/SG(n)-SG(pressure_gradient)/SG(n)
    published_force=SG(E)+residual_product/SG(n)-SG(pressure_gradient)/SG(n)
    assert exact_force==0 and published_force==F(9,875)
    # Positive controls: a constant field gives exact equality; a true
    # global Reynolds mean also makes the standard covariance identity valid.
    constant=lambda x:F(3)
    assert SG(lambda x:n(x)*constant(x))-SG(n)*SG(constant)==0
    f=[F(1),F(2),F(4)];g=[F(3),F(-1),F(2)]
    mean=lambda v:sum(v,F(0))/len(v)
    assert mean([x*y for x,y in zip(f,g)])-mean(f)*mean(g)==mean([(x-mean(f))*(y-mean(g)) for x,y in zip(f,g)])
    filter_witness={'filter':'centered five-point quadratic Savitzky-Golay','weights':['-3/35','12/35','17/35','12/35','-3/35'],
        'fields':'n(x)=2+x^2/100; E(x)=x^2 at integer stencil locations; u=B=0; Pprime=nE',
        'location':0,'G_n':str(SG(n)),'G_E':str(SG(E)),
        'exact_filtered_covariance':str(covariance),'filtered_residual_product':str(residual_product),
        'true_filtered_momentum_force_residual':str(exact_force),
        'displayed_D2_force_residual_using_residual_product':str(published_force),
        'positive_controls':['Constant field identity passes.','Global Reynolds-mean covariance identity passes.'],
        'alternative_exact_interpretation':'Residuals defined relative to each evaluation window center, deltaQ_x(r)=Q(x+r)-GQ(x), recover exact weighted local covariance. This is distinct from filtering the pointwise residual field Q-GQ.',
        'limits':'A valid SG filter is enough to refute a general Reynolds identity, but original discrete coefficients/polynomial order and PIC fields were not recovered. Disclosed cutoff/window labels do not establish an exact discrete kernel. No magnitude or sign of the reported physical anomaly is inferred.'}
    # Continuity and the source zz subsystem can both hold without fixing Tzz.
    subsystem=[]
    for Tzz in (F(1),F(7)):
        n0,m,q=F(1),F(1),F(1);uz=F(2);div=F(1)-F(1);grad=F(3);Ez=F(3);heat=F(0)
        lhs=heat+n0*((Tzz+m*uz*uz)*div+2*uz*grad)
        rhs=2*q*n0*Ez*uz
        assert div==0 and lhs==rhs and q*Ez==grad+m*uz*div
        subsystem.append({'Tzz':str(Tzz),'bulk_uz':str(uz),'mass':str(m),'div_u':str(div),
            'zz_heat_flux_divergence':str(heat),'offdiagonal_temperature_divergence':str(grad),'Ez':str(Ez),
            'B5c_left':str(lhs),'B5c_right':str(rhs),'B5d_pass':True,
            'B6c_division_defined':False,'Tzz_equals_mass_times_uz_squared':Tzz==m*uz*uz})
    thresholds=[marginal_cold_branch(tau,mu) for tau in (.02,.1) for mu in (100.,1836.)]
    for row in thresholds:
        assert row['absolute_k_squared_epsilon_marginality_residual']<2e-12
        if row['absolute_dielectric_residual'] is not None:
            assert row['absolute_dielectric_residual']<2e-9
    # E2 has lambda/di >= X/R_exists. The printed E3 is precisely the
    # stronger bound obtained at lambda=de, not a forced algebraic error:
    # "any scale" may mean every scale rather than existence at one scale.
    band=[]
    for mu in (100.,1836.):
        exists_rhs=mu**2*math.sqrt(8)  # normalize me,n,beta,epsilon*lambda0 to1
        all_rhs=exists_rhs/math.sqrt(mu)
        printed_rhs=mu**1.5*math.sqrt(8)
        assert math.isclose(all_rhs,printed_rhs,rel_tol=2e-15)
        X=math.sqrt(all_rhs*exists_rhs)
        cutoff=X/exists_rhs
        assert 1/math.sqrt(mu)<cutoff<1
        band.append({'mass_ratio':mu,'de_over_di':1/math.sqrt(mu),
            'printed_E3_RHS_over_some_scale_RHS':printed_rhs/exists_rhs,
            'printed_E3_equals_every_scale_condition':True,
            'intermediate_example_lambda_critical_over_di':cutoff,
            'intermediate_example_some_but_not_every_scale_passes':True})
    result={'schema_version':1,'all_checks_passed':True,'scope':'Definitions, analytic moment/filter counterchecks and uniform Maxwellian marginal controls; no source curves/PIC rerun or reconstructed fields.',
        'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'runtime':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
        'normalization_positive_controls':normalization,'plasma_function_identity_checks':function_checks,
        'nonrelativistic_Doppler_positive_controls':frames,'spatial_filter_counterexample':filter_witness,
        'steady_xpoint_zz_subsystem_controls':subsystem,'finite_mass_ratio_marginal_controls':thresholds,
        'Appendix_E_scale_quantifier_positive_controls':band,
        'Appendix_E_mass_factor_error_candidate':{
            'status':'withdrawn_as_error',
            'reason':'Printed E3 is exactly E2 evaluated at the lower electron-inertial edge de, giving a sufficient condition for every scale in (de,di). Evaluating at di instead gives existence of some scale. The phrase any scale admits the universal interpretation; no definite mass-factor algebra error is established.',
            'retained_scope':'Positive quantifier clarification only; the assumed KAW scale interval must still be stated.'},
        'Appendix_B_edge_gradient_scope':{
            'source_locators':'Journal pp19-20 B4-B6c, p21 B12-B14 and p22 B17-B18',
            'finding':'B17 differentiates and evaluates at the sheet edge delta a temperature relation inferred only at the X-point. This requires an extra spatial closure/extrapolation, even apart from the zero-divisor problem in B6c.',
            'limits':'No measured Tyy temperature or physical heating mechanism is refuted. At the edge the source retains nonzero inflow and magnetic terms, absent from its X-point reduction.'},
        'limits':['Moment subsystem witnesses do not assert a physical full zero-heat-flux steady solution; the source already acknowledges xx/yy closure failure.',
            'Finite-mass marginal controls concern homogeneous drifting Maxwellians, not an inhomogeneous reconnection eigenmode.',
            'The quoted typical wavelength does not fit a5de FWHM in the two cold cases, but higher marginal k and a wider effective mode support are not excluded.',
            'The journal replaces the preprint MHD comparison with Doppler Eq4.1; preprint-only MHD claims are not attributed to the final article.'],
        'new_PIC_simulations':0}
    out=HERE/'source-identity-checks.json';out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'all_checks_passed':True,'SG_exact_covariance':str(covariance),'SG_residual_product':str(residual_product),'filter_budget_defect':str(published_force),'thresholds':thresholds,'receipt_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))


if __name__=='__main__':main()
