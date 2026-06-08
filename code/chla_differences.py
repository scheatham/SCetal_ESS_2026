import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = "Times"
tfont = {'fontname':'Times'}
import matplotlib.pylab as pl

clouds_nadir = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_nadirSun/*_output_file.txt'))
clear_nadir = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_nadirSun/*_output_file.txt'))

clouds_75 = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_75Sun/*_output_file.txt'))
clear_75 = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_75Sun/*_output_file.txt'))

clouds_50 = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_50Sun/*_output_file.txt'))
clear_50 = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_50Sun/*_output_file.txt'))

clouds_15 = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_15Sun/*_output_file.txt'))
clear_15 = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_15Sun/*_output_file.txt'))

pace_edge_0 = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/TOA_PACE_sun0/*_output_file.txt'))
pace_nadir_0 = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/TOA_NADIR_sun0/*_output_file.txt'))

def getDifferences(clear_input,cloudy_input,lambdas):
    clear_vals = np.zeros([len(clear_input),len(lambdas),])
    cloudy_vals = np.zeros([len(cloudy_input),len(lambdas)])
    differences = np.zeros([len(clear_input),len(lambdas)])
    for i in range(0,len(cloudy_input)):
        currentcloudyFile = cloudy_input[i]
        currentclearFile = clear_input[i]
        cloudy=[]
        clear=[]
        with open(currentclearFile,'r') as data:
            for line in data:
                p=line.split()
                if len(p) == 0:
                    break
                else:
                    clear.append(float(p[1]))
        with open(currentcloudyFile,'r') as data2:
            for line in data2:
                p=line.split()
                if len(p) == 0:
                    break
                else:
                    cloudy.append(float(p[1]))
        # clear_vals[:,i] = clear
        # cloudy_vals[:,i] = cloudy
        clear_vals[i,:]=clear
        cloudy_vals[i,:]=cloudy
        for j in range(0,len(cloudy)): 
            diff = ((cloudy[j]-clear[j])/(clear[j]))*100 #percent difference
            differences[i,j]=diff
    return clear_vals, cloudy_vals, differences


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

lambdas = [400, 413, 443, 482, 483, 490, 510, 560,561, 620, 665, 670, 674, 681, 704, 705, 709, 754, 780] #for updated chl algorithms
#lambdas = [400, 413, 443, 482, 483, 490, 510, 560,561, 620, 665, 670, 674, 681, 704, 705, 780]
pace_lambdas = [400, 413, 443, 482, 483, 490, 510, 560,561,  620, 665, 670, 674, 681, 704, 705, 780]
#[4.0e-07, 4.13e-07, 4.43e-07, 4.82e-7, 4.83e-7, 4.9e-7, 5.1e-07, 5.6e-07, 5.61e-07,\
 #               6.2e-07, 6.65e-07, 6.7e-07, 6.74e-07, 6.81e-07, 7.04e-07, 7.05e-07, 7.8e-07]

nadir_vals, nadir_clouds_vals, nadir_differences = getDifferences(clear_nadir,clouds_nadir, lambdas)
vals75, clouds_vals75, differences75 = getDifferences(clear_75,clouds_75, lambdas)
vals50, clouds_vals50, differences50 = getDifferences(clear_50,clouds_50, lambdas)
vals15, clouds_vals15, differences15 = getDifferences(clear_15,clouds_15, lambdas)
pace_vals_0, nadir_vals_0, angle_differences_0 = getDifferences(pace_nadir_0,pace_edge_0,pace_lambdas)

#Moses 2019
def chl_moses_2019(rrs_vals,lambds):
    rrs_665 = rrs_vals[:,lambds.index(665)]
    rrs_709 = rrs_vals[:,lambds.index(709)]
    a = [153, 18.728]
    chl=[]
    for i in range(len(rrs_vals)):
        chl.append(a[0]*((1/rrs_665[i])*(1/rrs_709[i])*rrs_709[i]) + a[1])
    return chl

# Calculates chl-a using 3 band NIR (Moses et al 2012)
def chl_moses_3b(rrs_vals,lambds):
    # rrs_670 = rrs_vals[:,lambds.index(670)]
    # rrs_705 = rrs_vals[:,lambds.index(705)]
    # rrs_780 = rrs_vals[:,lambds.index(780)]
    ## MERIS Rrs 670 705 780
    #updated to olci 665 709 745
    rrs_665 = rrs_vals[:,lambds.index(665)]
    rrs_709 = rrs_vals[:,lambds.index(709)]
    rrs_754 = rrs_vals[:,lambds.index(754)]
    a = [232.29, 23.173]  # coefficients of Moses et al
    chl=[]
    for i in range(len(rrs_vals)):
        #chl.append(a[0] * (((1 / rrs_670[i]) - (1 / rrs_705[i])) * rrs_780[i]) + a[1])
        chl.append(a[0] * (((1 / rrs_665[i]) - (1 / rrs_709[i])) * rrs_754[i]) + a[1])
    return chl

# Mishra algorithm
# 665, 704 (or 708)
# is unitless!!
def chl_mishra(rrs_vals, lambds):
    rrs_665 = rrs_vals[:,lambds.index(665)]
    rrs_704 = rrs_vals[:,lambds.index(704)]
    a = [14.039, 86.115, 194.325]
    chl=[]
    for i in range(len(rrs_vals)):
        x = (rrs_704[i] - rrs_665[i]) / (rrs_704[i] + rrs_665[i])
        chl.append(a[0] + a[1] * x + a[2] * x**2)
    return chl

############### MBR algorithms ###############
# GENERAL shape:
# log10(CHL) = a0 + a1X + a2X^2 + a3X^3 + a4X^4
# X = log10(max(Rrs....) / Rrs)

# OC6 OLCI
def oc6_olci(rrs_vals, lambds):
    # 413, 443, 490, 510; 560, 665
    rrs_413 = rrs_vals[:,lambds.index(413)]
    rrs_443 = rrs_vals[:,lambds.index(443)]
    rrs_490 = rrs_vals[:,lambds.index(490)]
    rrs_510 = rrs_vals[:,lambds.index(510)]
    rrs_560 = rrs_vals[:,lambds.index(560)]
    rrs_665 = rrs_vals[:,lambds.index(665)]
    a = [0.95039, -3.05404, 2.17992, -1.12097, 0.15262]
    chl = []
    for i in range(len(rrs_vals)):
        x = np.log10(np.maximum.reduce([rrs_413[i], rrs_443[i], rrs_490[i], rrs_510[i]]) / np.mean([rrs_560[i], rrs_665[i]]))
        chl.append(10**(a[0] + a[1] * x + a[2] * x**2 + a[3] * x**3 + a[4] * x**4))
    return chl

# OC5 OLCI
def oc5_olci(rrs_vals, lambds):
    # 413, 443, 490, 510; 560
    rrs_413 = rrs_vals[:,lambds.index(413)]
    rrs_443 = rrs_vals[:,lambds.index(443)]
    rrs_490 = rrs_vals[:,lambds.index(490)]
    rrs_510 = rrs_vals[:,lambds.index(510)]
    rrs_560 = rrs_vals[:,lambds.index(560)]
    a = [0.43213, -3.13001, 3.05479, -1.45176, -0.24947]
    chl=[]
    for i in range(len(rrs_vals)):
        x = np.log10(np.maximum.reduce([rrs_413[i], rrs_443[i], rrs_490[i], rrs_510[i]]) / rrs_560[i])
        chl.append(10**(a[0] + a[1] * x + a[2] * x**2 + a[3] * x**3 + a[4] * x**4))
    return chl

# OC4 OLCI
def oc4_olci(rrs_vals, lambds):
    # 413, 443, 490, 510; 560
    rrs_413 = rrs_vals[:,lambds.index(413)]
    rrs_443 = rrs_vals[:,lambds.index(443)]
    rrs_490 = rrs_vals[:,lambds.index(490)]
    rrs_560 = rrs_vals[:,lambds.index(560)]
    a = [0.42540, -3.21679, 2.86907, -0.62628, -1.09333]
    chl=[]
    for i in range(len(rrs_vals)):
        x = np.log10(np.maximum.reduce([rrs_413[i], rrs_443[i], rrs_490[i]]) / rrs_560[i])
        chl.append(10**(a[0] + a[1] * x + a[2] * x**2 + a[3] * x**3 + a[4] * x**4))
    return chl

################OLI#####################
# L8 OLI from Franz et al 2015/acolite
def oc2_oli(rrs_vals, lambds):
    # 483, 561
    rrs_483 = rrs_vals[:,lambds.index(483)]
    rrs_561 = rrs_vals[:,lambds.index(561)]
    a = [0.1977, -1.8117, 1.9743, -2.5635, -0.7218]
    chl=[]
    for i in range(len(rrs_vals)):
        x = np.log10(rrs_483[i] / rrs_561[i])
        chl.append(10**(a[0] + a[1] * x + a[2] * x**2 + a[3] * x**3 + a[4] * x**4))
    return chl

# OC3 OLI from Werdell paper (different from Franz et al)
def oc3_oli(rrs_vals, lambds):
    # Rrs(443 > 482) / Rrs561 
    rrs_443 = rrs_vals[:,lambds.index(443)]
    rrs_482 = rrs_vals[:,lambds.index(482)]
    rrs_561 = rrs_vals[:,lambds.index(561)]
    a = [0.30963, -2.40052, 1.28932, 0.52802, -1.33825]
    chl=[]
    for i in range(len(rrs_vals)):
        x = np.log10(np.maximum(rrs_443[i], rrs_482[i]) / rrs_561[i])
        chl.append(10**(a[0] + a[1] * x + a[2] * x**2 + a[3] * x**3 + a[4] * x**4))
    return chl

def getDiff(cloudChl,noCloudChl, algName):
    print("Percent Change from Clear to Cloudy Conditions for "+ algName +" Algorithm:")
    for k in range(0,len(noCloudChl)):
        #diff = 100*((noCloudChl[k]-cloudChl[k])/noCloudChl[k])
        diff = 100*((cloudChl[k]-noCloudChl[k])/noCloudChl[k])
        print(diff)
    return diff 

def getChlDiffs(cloud_val, clear_val,lambds):
    # cloud_moses_2019 = chl_moses_2019(cloud_val, lambds)
    # clear_moses_2019 = chl_moses_2019(clear_val,lambds)
    # getDiff(clear_moses_2019,cloud_moses_2019, "moses 2019")
    cloud_oc6 = oc6_olci(cloud_val,lambds)
    clear_oc6 = oc6_olci(clear_val,lambds)
    getDiff(clear_oc6,cloud_oc6,"oc6")
    cloud_oc5 = oc5_olci(cloud_val,lambds)
    clear_oc5 = oc5_olci(clear_val, lambds)
    getDiff(clear_oc5,cloud_oc5,"oc5")
    cloud_oc4 = oc4_olci(cloud_val, lambds)
    clear_oc4 = oc4_olci(clear_val, lambds)
    getDiff(clear_oc4,cloud_oc4,"oc4")
    # cloud_oc2 = oc2_oli(cloud_val,lambds)
    # clear_oc2 = oc2_oli(clear_val, lambds)
    # getDiff(clear_oc2,cloud_oc2,"oc2")
    # cloud_oc3 = oc3_oli(cloud_val,lambds)
    # clear_oc3 = oc3_oli(clear_val,lambds)
    # getDiff(clear_oc3,cloud_oc3,"oc3")
    cloud_moses_3b = chl_moses_3b(cloud_val,lambds)
    clear_moses_3b = chl_moses_3b(clear_val,lambds)
    getDiff(clear_moses_3b,cloud_moses_3b,"moses3b")
    cloud_mishra = chl_mishra(cloud_val,lambds)
    clear_mishra = chl_mishra(clear_val,lambds)
    getDiff(clear_mishra,cloud_mishra,"mishra")

def getChla(Rrs,lambds):
    moses_3b = chl_moses_3b(Rrs,lambds)
    print('Moses3b chla return:' + str(moses_3b))
    mishra = chl_mishra(Rrs,lambds)
    print('Mishra chla return:' + str(mishra))
    oc6 = oc6_olci(Rrs,lambds)
    print('OC6 chla return:' + str(oc6))
    oc5 = oc5_olci(Rrs, lambds)
    print('OC5 chla return:' + str(oc5))
    oc4 = oc4_olci(Rrs, lambds)
    print('OC4 chla return:' + str(oc4))
    oc3 = oc3_oli(Rrs, lambds)
    print('OC3 chla return:' + str(oc3))
    oc2 = oc2_oli(Rrs,lambds)
    print('OC2 chla return:' + str(oc2))

# horizon_BGdiff = getDiff(noCloudChl_horizon,cloudChl_horizon)
# low_BGdiff = getDiff(noCloudChl_low,cloudChl_low)
# BG50diff = getDiff(noCloudChl_50,cloudChl_50)
# nadir_BGdiff = getDiff(noCloudChl_nadir,cloudChl_nadir)
#pace_BGdiff = getBGdiff(TOA_nadir,TOA_pace)

print("chla diffs 0")
getChlDiffs(nadir_vals,nadir_clouds_vals,lambdas)
print("chla diffs 50")
getChlDiffs(clouds_vals50,vals50,lambdas)
print("chla diffs 75")
getChlDiffs(clouds_vals75,vals75,lambdas)
