import matplotlib.pyplot as plt
import matplotlib as mpl 
import matplotlib.pylab as pl
import numpy as np
from pathlib import Path

mpl.rcParams['font.family'] = "Times"
tfont = {'fontname':'Times'}

script_dir = Path(__file__).parent
base_dir = script_dir.parent

PFfile = base_dir / 'ContrastingSamples_config_outputs/VF18_PF.txt' 
streamsFile_8 = base_dir / 'ContrastingSamples_config_outputs/VF18_PF_10st.txt'
streamsFile_32 = base_dir / 'ContrastingSamples_config_outputs/VF18_PF_34st.txt'
streamsFile_64 = base_dir / 'ContrastingSamples_config_outputs/VF18_PF_64st.txt' 
#b = 5

def readtwocolFile(file_name):
    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split()
            x.append(float(p[0]))
            y.append(float(p[1]))
    return x, y

x,y = readtwocolFile(PFfile)
x8,y8 = readtwocolFile(streamsFile_8)
x32,y32 = readtwocolFile(streamsFile_32)
x64,y64 = readtwocolFile(streamsFile_64)

colors = pl.cm.cubehelix(np.linspace(0,1,5))

fig, ax  = plt.subplots(1,1,sharex=True,figsize=(5, 4))
plt.xticks(np.arange(0,181,20))
plt.grid(which='major', alpha=0.4)
plt.yscale('log')
plt.plot((np.rad2deg(np.arccos(x))),y, color = colors[3],label=r'True $\beta$', linewidth=4, alpha=0.75)
plt.plot((np.rad2deg(np.arccos(x64))),y64,color = colors[2],linestyle = '--',label='64',linewidth=1.5)
plt.plot((np.rad2deg(np.arccos(x32))),y32,color = colors[1],linestyle = 'dotted',label='34',linewidth=1.5)
plt.plot((np.rad2deg(np.arccos(x8))),y8,color = colors[0],linestyle = '-.',label='16',linewidth=1.5)
plt.legend()
plt.xlabel(r'Scattering Angle [$^\circ$]',size=12)
plt.ylabel(r'$\beta$ [m$^{-1}$ sr$^{-1}$]',size=12)
plt.grid('on')
#plt.title('Phase Function Approximations',size=15)
ax.annotate(
'(a)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize='medium', verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
fig.savefig('OCPF.pdf',bbox_inches="tight",dpi=600)