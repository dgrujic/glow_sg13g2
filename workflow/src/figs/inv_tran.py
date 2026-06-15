
from plotSettings import *
import matplotlib.ticker as ticker
import subprocess

def runNgspice(netlist):
    try:
        res = subprocess.run( ["ngspice", "-b"], input=netlist, text=True, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        print("ngspice exited with " + str(err.returncode))
        print(err.stdout)
        print(err.stderr)
        exit(1)
    except FileNotFoundError:
        print("ngspice not found")
        exit(1)
    return res

def format_result(res, wpwn):
    tmp = res.split()
    # Rise time
    ntr, tr = tmp[0].split('=')
    tr = str(round(float(tr)*1e12, 1))
    # Fall time
    ntf, tf = tmp[1].split('=')
    tf = str(round(float(tf)*1e12, 1))
    # Delay H->L
    ntphl, tphl = tmp[2].split('=')
    tphl = str(round(float(tphl)*1e12, 1))
    # Delay L->H
    ntplh, tplh = tmp[3].split('=')
    tplh = str(round(float(tplh)*1e12, 1))
    
    res =  "| WP/WN | tr   | tf   | tphl | tplh |\n"
    res += "|:-----:|:----:|:----:|:----:|:----:|\n"
    res += "| " + wpwn + " | " + tr + " | " + tf + " | " + tphl + " | " + tplh + " |\n"
    return res        

netlist = """
.lib $PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.param WP_over_WN=1.5
.param WN=1e-6

VSUP VDD 0 1.2
VIN IN 0 pulse(1.2 0 1n 100p 100p 2n 4n 1)
XN0 OUT IN 0 0 sg13_lv_nmos w={WN} l=130n
XP0 OUT IN VDD VDD sg13_lv_pmos w={WP_over_WN*WN} l=130n
C1 OUT 0 20f

.control
    alterparam WP_over_WN=1.5
    reset
    tran 10p 5n
    meas tran rise_time TRIG V(out) VAL=0.24 RISE=1 TARG V(out) VAL=0.96 RISE=1
    meas tran fall_time TRIG V(out) VAL=0.96 FALL=1 TARG V(out) VAL=0.24 FALL=1
    meas tran tphl TRIG V(in) VAL=0.6 RISE=1 TARG V(out) VAL=0.6 FALL=1
    meas tran tplh TRIG V(in) VAL=0.6 FALL=1 TARG V(out) VAL=0.6 RISE=1
    echo "#!#!1 tr=$&rise_time tf=$&fall_time tphl=$&tphl tplh=$&tplh"
    wrdata inv_tran_1p5.txt v(out) i(vsup)
    alterparam WP_over_WN=0.5
    reset
    tran 10p 5n
    meas tran rise_time TRIG V(out) VAL=0.24 RISE=1 TARG V(out) VAL=0.96 RISE=1
    meas tran fall_time TRIG V(out) VAL=0.96 FALL=1 TARG V(out) VAL=0.24 FALL=1
    meas tran tphl TRIG V(in) VAL=0.6 RISE=1 TARG V(out) VAL=0.6 FALL=1
    meas tran tplh TRIG V(in) VAL=0.6 FALL=1 TARG V(out) VAL=0.6 RISE=1
    echo "#!#!2 tr=$&rise_time tf=$&fall_time tphl=$&tphl tplh=$&tplh"
    wrdata inv_tran_0p5.txt v(out) i(vsup)
    alterparam WP_over_WN=4.5
    reset
    tran 10p 5n
    meas tran rise_time TRIG V(out) VAL=0.24 RISE=1 TARG V(out) VAL=0.96 RISE=1
    meas tran fall_time TRIG V(out) VAL=0.96 FALL=1 TARG V(out) VAL=0.24 FALL=1
    meas tran tphl TRIG V(in) VAL=0.6 RISE=1 TARG V(out) VAL=0.6 FALL=1
    meas tran tplh TRIG V(in) VAL=0.6 FALL=1 TARG V(out) VAL=0.6 RISE=1    
    echo "#!#!3 tr=$&rise_time tf=$&fall_time tphl=$&tphl tplh=$&tplh"    
    wrdata inv_tran_4p5.txt v(out) i(vsup)
.endc
"""

res = runNgspice(netlist)
res_str = res.stdout

for line in res_str.split("\n"):
    line = line.strip()
    if line.startswith("#!#!1"):
        res_1p5 = line[5:]
    if line.startswith("#!#!2"):
        res_0p5 = line[5:]
    if line.startswith("#!#!3"):
        res_4p5 = line[5:]

print(format_result(res_0p5, "0.5"))
print(format_result(res_1p5, "1.5"))
print(format_result(res_4p5, "4.5"))

data = np.loadtxt('inv_tran_1p5.txt')
t1p5 = data[:, 0] * 1e9
v_out_1p5 = data[:, 1]
i_sup_1p5 = data[:, 3]

data = np.loadtxt('inv_tran_0p5.txt')
t0p5 = data[:, 0] * 1e9
v_out_0p5 = data[:, 1]
i_sup_0p5 = data[:, 3]

data = np.loadtxt('inv_tran_4p5.txt')
t4p5 = data[:, 0] * 1e9
v_out_4p5 = data[:, 1]
i_sup_4p5 = data[:, 3]

# Remove data files
subprocess.run( ['rm', 'inv_tran_0p5.txt'] )
subprocess.run( ['rm', 'inv_tran_1p5.txt'] )
subprocess.run( ['rm', 'inv_tran_4p5.txt'] )

plot(t0p5, v_out_0p5, 'b', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=0.5$")
plot(t1p5, v_out_1p5, 'g', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=1.5$")
plot(t4p5, v_out_4p5, 'r', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=4.5$")

legend(loc="upper right")
xlabel(r"$t~\mr{[ns]}$")
ylabel(r"$V_\mr{out}~\mr{[V]}$")

xlim(0,5)
grid()

tight_layout()

savefig("inv_tran.svg", transparent=False)

figure()

plot(t0p5, -1e6*i_sup_0p5, 'b', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=0.5$")
plot(t1p5, -1e6*i_sup_1p5, 'g', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=1.5$")
plot(t4p5, -1e6*i_sup_4p5, 'r', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=4.5$")

ax = gca()
axins = ax.inset_axes([0.5, 0.32, 0.35, 0.35])
axins.plot(t0p5, -1e6*i_sup_0p5, 'b')
axins.plot(t1p5, -1e6*i_sup_1p5, 'g')
axins.plot(t4p5, -1e6*i_sup_4p5, 'r')

x1, x2, y1, y2 = 3.0, 3.4, -100, 50
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)

axins.grid()

legend(loc="upper right")
xlabel(r"$t~\mr{[ns]}$")
ylabel(r"$I_\mr{DD}~\mr{[\mu A]}$")

xlim(0,5)
grid()

tight_layout()

savefig("inv_tran_idd.svg", transparent=False)


