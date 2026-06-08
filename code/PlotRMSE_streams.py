import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib as mpl
from pathlib import Path

script_dir = Path(__file__).parent
base_path = script_dir.parent

mpl.rcParams['font.family'] = "Times"
tfont = {'fontname':'Times'}

output_files_toa = sorted(glob.glob(str(base_path / "ContrastingSamples_config_outputs/WithSpecRef/EGY5_TOA/EGY5_radiance_*_config_output_file*.txt")))
output_files_toa_SRT = sorted(glob.glob(str(base_path / "ContrastingSamples_config_outputs/EGY5_TOA/EGY5_radiance_*_config_output_file*.txt")))
output_files_S3angs1 = sorted(glob.glob(str(base_path / "ContrastingSamples_config_outputs/WithSpecRef/SatelliteAngleSims/EGY5_TOA_Sentinel3/EGY5_TOA_AZI0/EGY5_radiance_*_config_output_file*.txt")))
output_files_S3angs2 = sorted(glob.glob(str(base_path / "ContrastingSamples_config_outputs/WithSpecRef/SatelliteAngleSims/EGY5_TOA_Sentinel3/EGY5_TOA_AZI180/EGY5_radiance_*_config_output_file*.txt")))
output_files_boa = sorted(glob.glob(str(base_path / "ContrastingSamples_config_outputs/EGY5_BOA/EGY5_radiance_*_config_output_file*.txt")))
output_files_PACE = sorted(glob.glob(str(base_path / "ContrastingSamples_config_outputs/WithSpecRef/SatelliteAngleSims/EGY5_TOA_PACE/EGY5_TOA_AZI0/EGY5_radiance_*_config_output_file*.txt")))
output_files_PACE2 = sorted(glob.glob(str(base_path / "ContrastingSamples_config_outputs/WithSpecRef/SatelliteAngleSims/EGY5_TOA_PACE/EGY5_TOA_AZI180/EGY5_radiance_*_config_output_file*.txt")))

streams = np.arange(6,94,2)
numWavelengths = 45

rrss_S3angs1=np.zeros([len(output_files_S3angs1),numWavelengths])
rrss_S3angs2=np.zeros([len(output_files_S3angs1),numWavelengths])
rrss_toa=np.zeros([len(output_files_toa),numWavelengths])
rrss_toa_SRT=np.zeros([len(output_files_toa_SRT),numWavelengths])
rrss_boa=np.zeros([len(output_files_boa),numWavelengths])
rrss_PACE=np.zeros([len(output_files_PACE),numWavelengths])
rrss_PACE2=np.zeros([len(output_files_PACE),numWavelengths])

RMSE_s3angs1 = np.zeros(len(rrss_S3angs1)) 
RMSE_s3angs2 = np.zeros(len(rrss_S3angs2)) 
RMSE_toa = np.zeros(len(rrss_toa))
RMSE_toa_SRT = np.zeros(len(rrss_toa_SRT))
RMSE_boa = np.zeros(len(rrss_boa))
RMSE_PACE = np.zeros(len(rrss_PACE))
RMSE_PACE2 = np.zeros(len(rrss_PACE))

def readFlickOutput(file_name):
    lambds=[]
    rrs=[]
    with open(file_name) as data:
        for line in data:
            p = line.split()
            if len(p) == 0:
                break
            else:
                lambd=float(p[0])*10**9
                lambds.append(lambd)
                rrs.append(p[1])
    return lambds, rrs

def getError(predictions, targets):
  #  percError = ((np.abs(predictions-targets)/np.abs(targets)).sum())/len(predictions)
    rmse = np.sqrt(((predictions-targets)**2/(targets**2)).sum()/len(predictions))*100
    return rmse
    #return percError, rmse

for i in range(0,len(output_files_toa_SRT)):
     lambds, rrss_toa_SRT[i,:] = readFlickOutput(output_files_toa_SRT[i])

for j in range(0,len(output_files_toa_SRT)):
    #pE_toa_SRT[j],
    RMSE_toa_SRT[j] = getError(rrss_toa_SRT[j,:],rrss_toa_SRT[len(rrss_toa_SRT)-1,:])

for i in range(0,len(output_files_S3angs1)):
    #print(i)
    lambds, rrss_S3angs1[i,:] = readFlickOutput(output_files_S3angs1[i])
    lambds, rrss_S3angs2[i,:] = readFlickOutput(output_files_S3angs2[i])
    lambds, rrss_toa[i,:] = readFlickOutput(output_files_toa[i])
    lambds, rrss_boa[i,:] = readFlickOutput(output_files_boa[i])
    lambds, rrss_PACE[i,:] = readFlickOutput(output_files_PACE[i])
    lambds, rrss_PACE2[i,:] = readFlickOutput(output_files_PACE[i])

for j in range(0,len(output_files_S3angs1)):
        #pE_s3angs1[j],
        RMSE_s3angs1[j] = getError(rrss_S3angs1[j,:],rrss_S3angs1[len(rrss_S3angs1)-1,:])
        #pE_s3angs2[j],
        RMSE_s3angs2[j] = getError(rrss_S3angs2[j,:],rrss_S3angs2[len(rrss_S3angs2)-1,:])
        #pE_toa[j],
        RMSE_toa[j] = getError(rrss_toa[j,:],rrss_toa[len(rrss_toa)-1,:])
       # pE_toa_p180[j],RMSE_toa_p180[j] = getError(rrss_toa_p180[j,:],rrss_toa_p180[len(rrss_toa)-1,:])
        #pE_boa[j],
        RMSE_boa[j] = getError(rrss_boa[j,:],rrss_boa[len(rrss_boa)-1,:])
        #pE_PACE[j],
        RMSE_PACE[j] = getError(rrss_PACE[j,:],rrss_PACE[len(rrss_PACE)-1,:])
        RMSE_PACE2[j] = getError(rrss_PACE[j,:],rrss_PACE[len(rrss_PACE)-1,:])


colors = pl.cm.cubehelix(np.linspace(0,1,11))
cmap = mpl.cm.cubehelix

fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111)
major_ticks = np.arange(0, 101, 20)
minor_ticks = np.arange(0, 101, 5)
ax.set_xticks(major_ticks)
ax.set_yscale('log')
ax.grid(which='major', alpha=0.4)
plt.plot(streams,RMSE_boa,color=colors[1],linestyle=(0, (5, 1)))
plt.plot(streams,RMSE_toa, color=colors[3],linestyle = '-.')
plt.plot(streams,RMSE_s3angs1,color=colors[4])
plt.plot(streams,RMSE_s3angs2,color = (0.5, 0.5, 0.5),linestyle='dotted')
plt.plot(streams,RMSE_PACE,color=colors[5],linestyle = '--')
#plt.title('RMSE in L$_{w}$',fontsize=14)
plt.legend(['BOA','TOA','OLCI 46.5$^{\circ}$W ','OLCI 22.1$^{\circ}$E','OCI 56.5$^{\circ}$W'],fontsize=12)
plt.ylabel(r"rRMSE [%]", fontsize=14)
plt.xlabel('Number of Streams',fontsize=14)
ax.xaxis.set_ticks([10,20,30,40,50,60,70,80,90])
plt.xlim([7,95])
ax.grid(True)
#fig.savefig(LwRMSEnew.pdf", bbox_inches="tight", dpi=600)
