from scipy.special import legendre
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from matplotlib.transforms import ScaledTranslation
import glob 

mpl.rcParams['font.family'] = "Times"
tfont = {'fontname':'Times'}

from pathlib import Path

script_dir = Path(__file__).parent

wignerFiles_ff16 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/FournierForand550/wig16/wigner16*.txt"))
)
wignerFiles_ff24 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/FournierForand550/wig24/wigner24*.txt"))
)
wignerFiles_ff34 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/FournierForand550/wig34/wigner34*.txt"))
)

wignerFiles_HG16 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/HenyeyGreenstein550/wig16/wigner16*.txt"))
)
wignerFiles_HG24 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/HenyeyGreenstein550/wig24/wigner24*.txt"))
)
wignerFiles_HG34 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/HenyeyGreenstein550/wig34/wigner34*.txt"))
)

wignerFiles_EGY16 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/EGY5550/wig16/wigner16*.txt"))
)
wignerFiles_EGY24 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/EGY5550/wig24/wigner24*.txt"))
)
wignerFiles_EGY34 = sorted(
    glob.glob(str(script_dir / "SensitivityAnalyses/EGY5550/wig34/wigner34*.txt"))
)

def getWigs(wignerFile):
    with open(wignerFile,'r') as data:
        wigCoefs = []
        for line in data:
            p = line.split()
            if len(p) == 0:
                break
            else:
                wigCoefs.append(float(p[0]))
    return wigCoefs

def readtwocolFile(file_name):
    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split()
            if len(p) == 0:
                break
            else:
                x.append(float(p[0]))
                y.append(float(p[1]))
    return x, y

def residuals(predictions, targets):
    return np.abs((predictions-targets).mean())

def rmse(predictions, targets):
    rmse = np.sqrt(((predictions-targets)**2/(targets**2)).sum()/len(predictions))*100
    return rmse

def getVSFfromWig(mu, numTerms,wigFile):
    wigCoefs = getWigs(wigFile)
    wigVSFs = []
    totP=0
    for i in range(0,len(mu)):
        for j in range(0,numTerms):
            legTerms = legendre(j)
            evalLeg = legTerms(mu[i])
            p = wigCoefs[j]*evalLeg
            totP += p
        wigVSFs.append(totP)
        totP=0
    return wigVSFs

def findThreshold(test_list):
    return next((x for x, val in enumerate(test_list) if val < 1e-2), None)

###### Here we get VSF from wigner and legendre coefs, and convert angles to degrees###########
mu = np.linspace(-1,1,500)
theta = np.rad2deg(np.arccos(mu))

def makeVSFapprox():
    wigVSFAngs_ff16 = np.zeros([len(wignerFiles_ff16),len(mu)])
    wigVSFAngs_ff24 = np.zeros([len(wignerFiles_ff24),len(mu)])
    wigVSFAngs_ff34 = np.zeros([len(wignerFiles_ff34),len(mu)])

    wigVSFAngs_HG16 = np.zeros([len(wignerFiles_HG16),len(mu)])
    wigVSFAngs_HG24 = np.zeros([len(wignerFiles_HG24),len(mu)])
    wigVSFAngs_HG34 = np.zeros([len(wignerFiles_HG34),len(mu)])

    wigVSFAngs_EGY16 = np.zeros([len(wignerFiles_EGY16),len(mu)])
    wigVSFAngs_EGY24 = np.zeros([len(wignerFiles_EGY24),len(mu)])
    wigVSFAngs_EGY34 = np.zeros([len(wignerFiles_EGY34),len(mu)])

    #def collectWigs():
    for i in range(0,len(wignerFiles_ff16)):
        wigVSFAngs_ff16[i,:] = getVSFfromWig(mu, 16,wignerFiles_ff16[i])
        wigVSFAngs_HG16[i,:] = getVSFfromWig(mu, 16,wignerFiles_HG16[i])
        wigVSFAngs_EGY16[i,:] = getVSFfromWig(mu, 16,wignerFiles_EGY16[i])

    for i in range(0,len(wignerFiles_ff24)):
        wigVSFAngs_ff24[i,:] = getVSFfromWig(mu, 24,wignerFiles_ff24[i])
        wigVSFAngs_HG24[i,:] = getVSFfromWig(mu, 24,wignerFiles_HG24[i])
        wigVSFAngs_EGY24[i,:] = getVSFfromWig(mu, 24,wignerFiles_EGY24[i])
        
    for l in range(0,len(wignerFiles_ff34)):
        wigVSFAngs_ff34[l,:] = getVSFfromWig(mu, 34,wignerFiles_ff34[l])
        wigVSFAngs_HG34[l,:] = getVSFfromWig(mu, 34,wignerFiles_HG34[l])
        wigVSFAngs_EGY34[l,:] = getVSFfromWig(mu, 34,wignerFiles_EGY34[l])

    return (
        wigVSFAngs_ff16, wigVSFAngs_ff24, wigVSFAngs_ff34,
        wigVSFAngs_HG16, wigVSFAngs_HG24, wigVSFAngs_HG34,
        wigVSFAngs_EGY16, wigVSFAngs_EGY24, wigVSFAngs_EGY34
    )

# def plotVSFapprox():
#     plt.plot(angles,PFs,color = (0.7, 0.7, 0.7))
#     #plt.plot(fitAngles,fitVSF)
#     plt.plot(mu, wigVSFAngs[79,:],'--',color =(0.7, 0.7, 0.7))
#     plt.plot(mu,VSF24,'--',color = (0.5, 0.5, 0.5))
#     plt.plot(mu, VSF34,'--',color = (0.3, 0.3, 0.3))
#     plt.legend(['Real VSF','16 Streams','24 Streams','34 Streams'])
#     plt.yscale('log')
#     plt.title('VSF Approximation: Fournier Forand')
#     plt.xlabel("Scattering Angle [$\circ$]")
#     plt.ylabel("VSF [m$^{-1}$ sr$^{-1}$]")
#     #plt.savefig('FF_VSF_approx',dpi=600)

###Here we make the arrays to fill with the percent difference and RMSEs between sampling point choices#######
rmses_ff16=np.zeros(len(wignerFiles_ff16))
rmses_ff24=np.zeros(len(wignerFiles_ff24))
rmses_ff34=np.zeros(len(wignerFiles_ff34))

rmses_HG16=np.zeros(len(wignerFiles_HG16))
rmses_HG24=np.zeros(len(wignerFiles_HG24))
rmses_HG34=np.zeros(len(wignerFiles_HG34))

rmses_EGY16=np.zeros(len(wignerFiles_EGY16))
rmses_EGY24=np.zeros(len(wignerFiles_EGY24))
rmses_EGY34=np.zeros(len(wignerFiles_EGY34))


(
    wigVSFAngs_ff16, wigVSFAngs_ff24, wigVSFAngs_ff34,
    wigVSFAngs_HG16, wigVSFAngs_HG24, wigVSFAngs_HG34,
    wigVSFAngs_EGY16, wigVSFAngs_EGY24, wigVSFAngs_EGY34
) = makeVSFapprox()

deltaStreams = np.linspace(10,500,80)#HG
mum = mu.tolist()
mum.reverse()

for i in range(0,len(wigVSFAngs_ff16)):
    rmses_ff16[i] = rmse(wigVSFAngs_ff16[i,:],wigVSFAngs_ff16[len(wigVSFAngs_ff16)-1,:])
    rmses_HG16[i] = rmse(wigVSFAngs_HG16[i,:],wigVSFAngs_HG16[len(wigVSFAngs_HG16)-1,:])
    rmses_EGY16[i] = rmse(wigVSFAngs_EGY16[i,:],wigVSFAngs_EGY16[len(wigVSFAngs_EGY16)-1,:])
    
    rmses_ff24[i] = rmse(wigVSFAngs_ff24[i,:],wigVSFAngs_ff24[len(wigVSFAngs_ff24)-1,:])
    rmses_HG24[i] = rmse(wigVSFAngs_HG24[i,:],wigVSFAngs_HG24[len(wigVSFAngs_HG24)-1,:])
    rmses_EGY24[i] = rmse(wigVSFAngs_EGY24[i,:],wigVSFAngs_EGY24[len(wigVSFAngs_EGY24)-1,:])

    rmses_ff34[i] = rmse(wigVSFAngs_ff34[i,:],wigVSFAngs_ff34[len(wigVSFAngs_ff34)-1,:])
    rmses_HG34[i] = rmse(wigVSFAngs_HG34[i,:],wigVSFAngs_HG34[len(wigVSFAngs_HG34)-1,:])
    rmses_EGY34[i] = rmse(wigVSFAngs_EGY34[i,:],wigVSFAngs_EGY34[len(wigVSFAngs_EGY34)-1,:])

def plotErrors(deltaStreams):
    major_ticks = np.arange(0, 501, 50)
    colors = pl.cm.cubehelix(np.linspace(0,1,11))

    fig4, axs = plt.subplots(3,1, sharex=True, sharey=True, figsize=(6, 7))
    plt.xlabel(r"$\beta$ Sampling Points",fontsize=14)
    plt.grid('on')
    
    axs[0].set_yscale('log')
    axs[0].grid(which='major', alpha=0.4)
    axs[0].plot(deltaStreams,rmses_HG16, color=colors[0]) #color = (0.3, 0.3, 0.3))
    axs[0].plot(deltaStreams,rmses_HG24, color=colors[2],linestyle='-.') #color = (0.5, 0.5, 0.5))
    axs[0].plot(deltaStreams,rmses_HG34, color=colors[4],linestyle='--')#color = (0.7, 0.7, 0.7))
    axs[0].legend(['16','24','34'])
    axs[0].set_title("Henyey-Greenstein",fontsize=14)
    axs[0].annotate(
    '(a)',
    xy=(0, 1), xycoords='axes fraction',
    xytext=(+0.5, -0.5), textcoords='offset fontsize',
    fontsize='medium', verticalalignment='top',
    bbox=dict(facecolor='1', edgecolor='none', pad=3.0))

    axs[1].set_yscale('log')
    axs[1].grid(which='major', alpha=0.4)
    axs[1].plot(deltaStreams,rmses_ff16,  color=colors[0])#color = (0.3, 0.3, 0.3))
    axs[1].plot(deltaStreams,rmses_ff24,  color=colors[2],linestyle='-.')#color = (0.5, 0.5, 0.5))
    axs[1].plot(deltaStreams,rmses_ff34,  color=colors[4],linestyle='--')#color = (0.7, 0.7, 0.7))
    axs[1].set_ylabel(r"rRMSE [%]",fontsize=14)
    axs[1].set_title("Fournier-Fourand",fontsize=14)
    axs[1].annotate(
    '(b)',
    xy=(0, 1), xycoords='axes fraction',
    xytext=(+0.5, -0.5), textcoords='offset fontsize',
    fontsize='medium', verticalalignment='top',
    bbox=dict(facecolor='1', edgecolor='none', pad=3.0))

    axs[2].set_xticks(major_ticks)
    axs[2].set_yscale('log')
    axs[2].grid(which='major', alpha=0.4)
    axs[2].plot(deltaStreams,rmses_EGY16,  color=colors[0])#color = (0.3, 0.3, 0.3))
    axs[2].plot(deltaStreams,rmses_EGY24,  color=colors[2],linestyle='-.')#color = (0.5, 0.5, 0.5))
    axs[2].plot(deltaStreams,rmses_EGY34,  color=colors[4],linestyle='--')#color = (0.7, 0.7, 0.7))
    axs[2].set_title("Coastal San Diego",fontsize=14)
    axs[2].annotate(
    '(c)',
    xy=(0, 1), xycoords='axes fraction',
    xytext=(+0.5, -0.5), textcoords='offset fontsize',
    fontsize='medium', verticalalignment='top',
    bbox=dict(facecolor='1', edgecolor='none', pad=3.0))

    for nn, ax in enumerate(axs):
        if nn == 1:
            ax.set_yticks([10**-4,10**-3,10**-2,10**-1,10**0,10**1])

    #fig4.savefig('finalrmseALLVSFs.pdf',bbox_inches="tight",dpi=600)
