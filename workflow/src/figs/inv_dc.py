
from plotSettings import *
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

netlist = """
.lib $PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.param WP_over_WN=1.5
.param WN=1e-6

VSUP VDD 0 1.2
VIN IN 0 0
XN0 OUT IN 0 0 sg13_lv_nmos w={WN} l=130n
XP0 OUT IN VDD VDD sg13_lv_pmos w={WP_over_WN*WN} l=130n

.control
    alterparam WP_over_WN=1.5
    reset
    dc VIN 0 1.2 0.01
    wrdata inv_dc_1p5.txt v(out) i(vsup)
    alterparam WP_over_WN=0.5
    reset
    dc VIN 0 1.2 0.01
    wrdata inv_dc_0p5.txt v(out) i(vsup)
    alterparam WP_over_WN=4.5
    reset
    dc VIN 0 1.2 0.01
    wrdata inv_dc_4p5.txt v(out) i(vsup)
.endc
"""

runNgspice(netlist)

data = np.loadtxt('inv_dc_1p5.txt')
v_in_1p5 = data[:, 0]
v_out_1p5 = data[:, 1]
i_sup_1p5 = data[:, 3]

data = np.loadtxt('inv_dc_0p5.txt')
v_in_0p5 = data[:, 0]
v_out_0p5 = data[:, 1]
i_sup_0p5 = data[:, 3]

data = np.loadtxt('inv_dc_4p5.txt')
v_in_4p5 = data[:, 0]
v_out_4p5 = data[:, 1]
i_sup_4p5 = data[:, 3]

# Remove data files
subprocess.run( ['rm', 'inv_dc_0p5.txt'] )
subprocess.run( ['rm', 'inv_dc_1p5.txt'] )
subprocess.run( ['rm', 'inv_dc_4p5.txt'] )

plot(v_in_0p5, v_out_0p5, 'b', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=0.5$")
plot(v_in_1p5, v_out_1p5, 'g', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=1.5$")
plot(v_in_4p5, v_out_4p5, 'r', linewidth=1.5, aa=True, label=r"$W_\mr{p}/W_\mr{n}=4.5$")

grid(which='both')
legend(loc="upper right")
xlabel(r"$V_\mr{in}~\mr{[V]}$")
ylabel(r"$V_\mr{out}~\mr{[V]}$")

r_axis = gca().twinx()
r_axis.plot(v_in_0p5, -i_sup_0p5*1e6, 'b--', linewidth=1.5, aa=True)
r_axis.plot(v_in_1p5, -i_sup_1p5*1e6, 'g--', linewidth=1.5, aa=True)
r_axis.plot(v_in_4p5, -i_sup_4p5*1e6, 'r--', linewidth=1.5, aa=True)

r_axis.set_ylabel(r"$I_\mr{DD}~\mr{[\mu A]}$")

tight_layout()

#show()

savefig("inv_dc.svg", transparent=False)
