import glob 
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.pylab as pl
import matplotlib as mpl
import scipy.integrate as int
from pathlib import Path

script_dir = Path(__file__).parent
base_dir = script_dir.parent
base_dir = base_dir.parent
flick_path = Path("/Users/sheacheatham")

mpl.rcParams['font.family'] = "Times"
tfont = {'fontname':'Times'}

testvsf = [flick_path / 'Flick-RT/FFVSF_TEST.txt','/Users/sheacheatham/Flick-RT/FFVSF_TEST.txt']

vsfs = [
    base_dir / "FournierForand/realVSF.txt",
    flick_path / "Flick-RT/HGVSF_TEST.txt",  
    base_dir / "EGY5_TOA/other/realVSF.txt"
]

ab_files = [flick_path / 'Flick-RT/material/marine_particles/iop_tables/ECOSENS_GF21_7_ap_bp.txt',\
flick_path / 'Flick-RT/material/marine_particles/iop_tables/ECOSENS_HF22_D1_ap_bp.txt',\
flick_path / 'Flick-RT/material/marine_particles/iop_tables/PB1819_NARWHAL_s_ap_bp.txt',\
flick_path / 'Flick-RT/material/marine_particles/iop_tables/PB1819_K1_s_ap_bp.txt',\
flick_path / "Flick-RT/material/marine_particles/iop_tables/SD16_VF06_ap_bp.txt"]

PF_files = [flick_path / 'Flick-RT/material/marine_particles/iop_tables/ECOSENS_GF21_7_pf.txt',\
flick_path / 'Flick-RT/material/marine_particles/iop_tables/ECOSENS_HF22_D1_pf.txt',\
flick_path / 'Flick-RT/material/marine_particles/iop_tables/PB1819_NARWHAL_s_pf.txt',\
flick_path / 'Flick-RT/material/marine_particles/iop_tables/PB1819_K1_s_pf.txt',\
flick_path / 'Flick-RT/material/marine_particles/iop_tables/SD16_VF06_pf.txt']

chla_nums = ['3.8','7.5','0.26','2.5'] # GF, HF, K1sb/c, VF06
             
def readAB(file_name):
    abs=[]
    scats=[]
    lambds = []
    with open(file_name, 'r', encoding='latin1') as data:
        i=0
        while i < 25:
            next(data)
            i+=1
        for line in data:
            p = line.split()
            if len(p) > 0:
                abs.append(float(p[1]))
                lambds.append(float(p[0]))
                scats.append(float(p[3]))
            else:
                break
    return lambds, abs, scats

def readPF(file_name):
    print(file_name)
    angle = []
    pf = []
    with open(file_name) as data:
        i=0
        while i < 29:
            next(data)
            i+=1
        for line in data:
            p = line.split()
            if len(p) > 0:
                angle.append(float(p[0]))
                pf.append(float(p[3]))
    return angle, pf


def readTwoCol(file_name):
    print(file_name)
    angles=[]
    vsf=[]
    with open(file_name) as data:
        for line in data:
            p = line.split()
            if len(p) == 0:
                break
            else:
                angle=float(p[0])
                angles.append(angle)
                vsf.append(float(p[1])*0.1)
    return angles, vsf

#lambds, GF_a, GF_b = readAB(ab_files[0])
lambds = []
As = []
Bs = []
angles = []
PFs = []
angles2 = []
VSFs = []

for i in range(0,len(ab_files)):
    lambdas, A, B = readAB(ab_files[i])
    lambds.append(lambdas)
    As.append(A)
    Bs.append(B)
    angle, PF = readPF(PF_files[i])
    angles.append(angle)
    PFs.append(PF)
for j in range(0,len(vsfs)):
    newangle, vsf = readTwoCol(vsfs[j])
    angles2.append(newangle)
    VSFs.append(vsf)

SPMs = [10.5255, 20.13, 3.61,  1.20, 1.13]
for j in range(0,len(As)):
    current_As = As[j]
    current_Bs = Bs[j] 
    for i in range(0,len(As[j])):
        current_As[i] = current_As[i]*SPMs[j]
        current_Bs[i] = current_Bs[i]*SPMs[j]
    As[j] = current_As
    Bs[j] = current_Bs


colors = pl.cm.cubehelix(np.linspace(0,1,11))

fig, ax  = plt.subplots(2,1,sharex=True,figsize=(4, 6))
ax[0].grid(which='major', alpha=0.4)
#plt.yscale('log')
ax[0].plot(lambds[0],As[0], color = colors[3],linestyle = 'dotted',label='Gaupnefjord')#label=str(chla_nums[0]+' mg m$^{-3}$'))#GF21 SPM 10.5255 
ax[0].plot(lambds[1],As[1],color = colors[6],linestyle = '--',label='Hardangerfjord')#label=str(chla_nums[1]+' mg m$^{-3}$'))#HF22 SPM 20.13  g/m3 
#ax[0].plot(lambds[2],As[2],color = colors[2],linestyle = '-.',label='Beauford Sea')#NARWHAL SPM 3.61 g/m3
ax[0].plot(lambds[3],As[3],color = colors[2],linestyle = '-.',label='Beaufort Sea')#label=str(chla_nums[2]+' mg m$^{-3}$'))
ax[0].plot(lambds[4],As[4],color = colors[4],label='Coastal San Diego')#label=str(chla_nums[3]+' mg m$^{-3}$'))#VF17 SPM 0.54 g/m3
ax[0].legend()
#ax[0].set_xlabel(r'Wavelength [nm]',size=12)
ax[0].set_ylabel(r'$a_p$ [m$^{-1}$]',size=12)
ax[0].grid('on')
ax[0].set_xlim([350,750])
ax[0].annotate(
'(a)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize='medium', verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))

ax[1].grid(which='major', alpha=0.4)
ax[1].set_yscale('log')
ax[1].plot(lambds[0],Bs[0], color = colors[3],linestyle = 'dotted',label='Gaupnefjord')
ax[1].plot(lambds[1],Bs[1],color = colors[6],linestyle = '--',label='Hardangerfjord')
#ax[1].plot(lambds[2],Bs[2],color = colors[2],linestyle = '-.',label='Beaufort Sea')
ax[1].plot(lambds[3],Bs[3],color = colors[2],linestyle = '-.',label='Beaufort Sea') #K1b
#ax[1].plot(lambds[3],[10]*len(lambds[3]),color = colors[4],linestyle = 'dotted',label='HG, FF')
ax[1].plot(lambds[4],Bs[4],color = colors[4],label='Coastal San Diego')
#ax[1].legend()
ax[1].set_xlabel(r'Wavelength [nm]',size=14)
ax[1].set_ylabel(r'$b_p$ [m$^{-1}$]',size=14)
#ax[1].legend()
ax[1].grid('on')
#x[1].xlim([350,750])
ax[1].set_xlim([350,750])
ax[1].annotate(
'(b)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize='medium', verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
#fig.savefig('AllABs_OO24.pdf',bbox_inches="tight",dpi=600)

fig2, ax2 = plt.subplots(1,1,sharex=True,figsize=(4,3))
ax2.grid(which='major', alpha=0.4)
plt.yscale('log')
plt.xticks(np.arange(1,181,20))
ax2.plot(angles[0],PFs[0], color = colors[3],linestyle = 'dotted',label='Gaupnefjord')
ax2.plot(angles[1],PFs[1],color = colors[6],linestyle = '--',label='Hardangerfjord')
ax2.plot(angles[3],PFs[3],color = colors[2],linestyle = '-.',label='Beaufort Sea')
#ax2.plot(angles[3],PFs[3],color = colors[4],linestyle = 'dotted',label='S2BS')
ax2.plot(angles[4],PFs[4],color = colors[4],label='Coastal San Diego')
#ax2.plot(np.rad2deg(np.arccos(angles2[0])),VSFs[0],color = colors[1],linestyle = '-.',label='FF')
#ax2.plot(np.rad2deg(np.arccos(angles2[1])),VSFs[1],color = colors[0],linestyle = 'dotted',label='HG')
#ax2.plot(np.rad2deg(np.arccos(angles2[2])),VSFs[2],color = colors[5],linestyle = '--',label='EGY5')
plt.ylabel(r'Phase Function [sr$^{-1}$]',size=14)
plt.xlabel(r'Scattering Angle[$^\circ$]',size=14)
ax2.grid('on')
#ax2.legend()
ax2.annotate(
'(c)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize='medium', verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
#fig2.savefig('AllPFs_OO24.pdf',bbox_inches="tight",dpi=600)


PFFF = VSFs[0]
PFHG = VSFs[1]
for i in range(0,len(VSFs[0])):
    PFFF[i] = PFFF[i]*10/25
for i in range(0,len(VSFs[1])):
    PFHG[i] = PFHG[i]*10

fig3, ax3 = plt.subplots(1,1,sharex=True,figsize=(7,5))
ax3.grid(which='major', alpha=0.4)
plt.yscale('log')
plt.xticks(np.arange(0,181,20))
ax3.plot(angles[4],PFs[4],color = colors[4],label='Coastal San Diego')
#ax3.plot(np.rad2deg(np.arccos(angles2[0])),PFFF,color = colors[1],linestyle = '-.',label='FF')
#ax3.plot(np.rad2deg(np.arccos(angles2[1])),PFHG,color = colors[0],linestyle = 'dotted',label='HG')
ax3.plot(np.rad2deg(np.arccos(angles2[0])),VSFs[0],color = colors[1],linestyle = '-.',label='Fournier-Forand')
ax3.plot(np.rad2deg(np.arccos(angles2[1])),VSFs[1],color = colors[0],linestyle = 'dotted',label='Henyey-Greenstein')
#ax3.plot(np.rad2deg(np.arccos(angles2[2])),VSFs[2],color = colors[5],linestyle = '--',label='EGY5')
plt.ylabel(r'Phase Function [sr$^{-1}$]',size=12)
plt.xlabel(r'Scattering Angle [$^\circ$]',size=12)
ax3.grid('on')
ax3.legend()
#fig3.savefig('SimPFs_OO24.pdf',bbox_inches="tight",dpi=600)
