import glob
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.pylab as pl
import matplotlib as mpl 
from pathlib import Path

mpl.rcParams['font.family'] = "Times"
tfont = {'fontname':'Times'}

script_dir = Path(__file__).parent
base_dir = script_dir.parent

plane_irradiances = glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getAvgSunAngle/plane_irradiance/*/*_file.txt'))
scalar_irradiances = glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getAvgSunAngle/scalar_irradiance/*/*_file.txt'))

sunSet_plane_sun = sorted(glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getAvgSunAngle/sunSet_plane/Sun/*_file.txt')))
sunSet_plane_clouds = sorted(glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getAvgSunAngle/sunSet_plane/Clouds/*_file.txt')))

sunSet_scalar_sun = sorted(glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getAvgSunAngle/sunSet_scalar/Sun/*_file.txt')))
sunSet_scalar_clouds = sorted(glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getAvgSunAngle/sunSet_scalar/Clouds/*_file.txt')))

additional_plane_irradiances = glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getAvgSunAngle/additional_plane_irradiance/*_file.txt'))
additional_scalar_irradiances = glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getAvgSunAngle/additional_scalar_irradiance/*_file.txt'))

SR_subtracted = glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getSpecRef/SRSubtracted/*/*_file.txt'))
SR_included = glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getSpecRef/SRIncluded/*/*_file.txt'))

Rrs_sunSets = np.sort(glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getSpecRef/getRrs*/SR_included/*_file.txt')))
Rrs_sunSets_SRSubtracted = np.sort(glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getSpecRef/getRrs*/SR_subtracted/*_file.txt')))

Rrs_sunSets_clouds = np.sort(glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getSpecRef/getRrs*/SR_included_addClouds/*_file.txt')))
Rrs_sunSets_SRSubtracted_clouds = np.sort(glob.glob(str(base_dir / 'ContrastingSamples_config_outputs/getSpecRef/getRrs*/SR_subtracted_addClouds/*_file.txt')))

def getRrs(input_file):
    lambdas = []    
    rrs = []
    with open(input_file,'r') as data:
        for line in data:
            p=line.split()
            if len(p) == 0:
                break
            else:
                lambdas.append(float(p[0]))
                rrs.append(float(p[1]))
    return rrs, lambdas

def getPercentSR(SR_subtracted, SR_included):
    allRatios = []
    for i in range(0,len(SR_subtracted)):
        SR_sub,lambdas = getRrs(SR_subtracted[i])
        SR_incl,lambdas = getRrs(SR_included[i])
        ratios = np.zeros(len(SR_sub))
        for j in range(0,len(SR_sub)):
            ratios[j] = 1 - (SR_sub[j]/SR_incl[j])
        allRatios.append(ratios)
    return allRatios, lambdas

def getRawSR(SR_subtracted,SR_included):
    allRAW = []
    for i in range(0,len(SR_subtracted)):
        SR_sub,lambdas = getRrs(SR_subtracted[i])
        SR_incl,lambdas = getRrs(SR_included[i])
        rawSRS = np.zeros(len(SR_sub))
        for j in range(0,len(SR_sub)):
            rawSRS[j] = SR_incl[j] - SR_sub[j]
        allRAW.append(rawSRS)
    return allRAW, lambdas

def getCosSunAngle(plane_irradiances,scalar_irradiances):
    allCosAngles = []
    for i in range(0,len(plane_irradiances)):
        plane_irr,lambdas = getRrs(plane_irradiances[i])
        scalar_irr,lambdas = getRrs(scalar_irradiances[i])
        cosAngles = np.zeros(len(plane_irr))
        for j in range(0,len(plane_irr)):
            cosAngles[j] = (plane_irr[j]/scalar_irr[j])
        allCosAngles.append(cosAngles)
    return allCosAngles, lambdas

allRatios,lambdas = getPercentSR(SR_subtracted,SR_included)
allRawSRs, lambdas = getRawSR(SR_subtracted,SR_included)
allCosAngles,lambdas = getCosSunAngle(plane_irradiances,scalar_irradiances)
additionalCosAngles, lambdas = getCosSunAngle(additional_plane_irradiances,additional_scalar_irradiances)

sunSetCosAngles_sun, green = getCosSunAngle(sunSet_plane_sun, sunSet_scalar_sun)
sunSetCosAngles_clouds, green = getCosSunAngle(sunSet_plane_clouds, sunSet_scalar_clouds)

sunset_Angles = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]

rrss_704 = np.zeros(len(Rrs_sunSets))
rrss_704_SRsubtracted = np.zeros(len(Rrs_sunSets_SRSubtracted))
rrss_ratio = np.zeros(len(Rrs_sunSets))

rrss_704_clouds = np.zeros(len(Rrs_sunSets))
rrss_704_SRsubtracted_clouds = np.zeros(len(Rrs_sunSets_SRSubtracted))
rrss_ratio_clouds = np.zeros(len(Rrs_sunSets))

sunAngles = np.linspace(0,75,16)

for i in range(0,len(Rrs_sunSets)):
    current_rrs, lambdas = getRrs(Rrs_sunSets[i])
    current_rrs_clouds, lambdas = getRrs(Rrs_sunSets_clouds[i])
    rrss_704[i] = current_rrs[lambdas.index(7.04e-07)]
    rrss_704_clouds[i] = current_rrs_clouds[lambdas.index(7.04e-07)]
for j in range(0,len(Rrs_sunSets_SRSubtracted)):
    current_rrs_SRsub, lambdas = getRrs(Rrs_sunSets_SRSubtracted[j])
    current_rrs_SRsub_clouds, lambdas = getRrs(Rrs_sunSets_SRSubtracted_clouds[j])
    rrss_704_SRsubtracted[j] = current_rrs_SRsub[lambdas.index(7.04e-07)]
    rrss_704_SRsubtracted_clouds[j] = current_rrs_SRsub_clouds[lambdas.index(7.04e-07)]
for k in range(0,len(rrss_704)):
    rrss_ratio[k] = 1 - (rrss_704_SRsubtracted[k]/rrss_704[k])
    rrss_ratio_clouds[k] = 1 - (rrss_704_SRsubtracted_clouds[k]/rrss_704_clouds[k])

colors = pl.cm.cubehelix(np.linspace(0,1,11))

fig6,ax6=plt.subplots(1,2,figsize=(10, 4), sharex=True, sharey=True)
ax6[0].grid(which='major', alpha=0.4)
ax6[0].set_title(r"Clear Skies")
ax6[0].set_ylabel(r"$\mu_d$, 510 nm")
ax6[0].plot(sunset_Angles,sunSetCosAngles_sun[0:16],color = colors[6],linestyle = '--')
ax6[0].plot(sunset_Angles,sunSetCosAngles_sun[16:32],color = colors[4])
ax6[0].set_xlabel(r"Solar Angle [$^\circ$]")
ax6[0].legend(['Hardangerfjord','Coastal San Diego'])

ax6[1].grid(which='major', alpha=0.4)
#ax6[1].text(-15, 0.9, 'Average Cosine of Incoming Radiation', va='center',rotation='vertical')
#ax6[1].supylabel(r"Average Cosine of Incoming Radiation") #510 nm
ax6[1].set_xlabel(r"Solar Angle [$^\circ$]")
ax6[1].set_title(r"Clouds")
ax6[1].plot(sunset_Angles,sunSetCosAngles_clouds[0:16],color = colors[6],linestyle = '--')
ax6[1].plot(sunset_Angles,sunSetCosAngles_clouds[16:32],color = colors[4])

fig6.savefig('deltaAvgCos.pdf',bbox_inches="tight",dpi=600)
#ax6[1].legend(['Hardangerfjord','Coastal San Diego']