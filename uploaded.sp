* EQUIVALENT CIRCUIT FOR VECTOR FITTED S-MATRIX
* Created using scikit-rf vectorFitting.py

.SUBCKT s_equivalent p1

* Port network for port 1
R_ref_1 p1 a1 50.0
H_b_1 a1 0 V_c_1 14.142135623730951
* Differential incident wave a sources for transfer from port 1
H_p_1 nt_p_1 nts_p_1 H_b_1 3.5355339059327378
E_p_1 nts_p_1 0 p1 0 0.07071067811865475
E_n_1 0 nt_n_1 nt_p_1 0 1
* Current sensor on center node for transfer to port 1
V_c_1 nt_c_1 0 0
* Transfer network from port 1 to port 1
R1_1 nt_n_1 nt_c_1 1.0202019997593725
X1 nt_p_1 nt_c_1 rcl_vccs_admittance res=nan cap=0.0 ind=inf gm=nan
X2 nt_n_1 nt_c_1 rcl_vccs_admittance res=317.44376853032026 cap=1.9302676355171343e-06 ind=0.050603086887182035 gm=0.0051420296188369324
.ENDS s_equivalent

.SUBCKT rcl_vccs_admittance n_pos n_neg res=1e3 cap=1e-9 ind=100e-12 gm=1e-3
L1 n_pos 1 {ind}
C1 1 2 {cap}
R1 2 n_neg {res}
G1 n_pos n_neg 1 2 {gm}
.ENDS rcl_vccs_admittance

.SUBCKT rl_admittance n_pos n_neg res=1e3 ind=100e-12
L1 n_pos 1 {ind}
R1 1 n_neg {res}
.ENDS rl_admittance

