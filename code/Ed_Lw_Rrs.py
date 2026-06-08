import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = "Times"
tfont = {'fontname':'Times'}
import matplotlib.pylab as pl

clouds_nadir_Ed = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_nadirSun/Ed/*_output_file.txt'))
clear_nadir_Ed = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_nadirSun/Ed/*_output_file.txt'))

clouds_50_Ed = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_50Sun/Ed/*_output_file.txt'))
clear_50_Ed = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_50Sun/Ed/*_output_file.txt'))

clouds_75_Ed = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_75Sun/Ed/*_output_file.txt'))
clear_75_Ed = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_75Sun/Ed/*_output_file.txt'))

clouds_nadir_Lw = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_nadirSun/Lw/*_output_file.txt'))
clear_nadir_Lw = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_nadirSun/Lw/*_output_file.txt'))

clouds_50_Lw = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_50Sun/Lw/*_output_file.txt'))
clear_50_Lw = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_50Sun/Lw/*_output_file.txt'))

clouds_75_Lw = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_clouds_75Sun/Lw/*_output_file.txt'))
clear_75_Lw = sorted(glob.glob(r'/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/BOA_75Sun/Lw/*_output_file.txt'))

lambdas = [400, 413, 443, 482, 483, 490, 510, 560,561, 620, 665, 670, 674, 681, 704, 705, 709, 754, 780] #for updated chl algorithms

def get_flick_output(input_files):
    lambdas = []    
    flick_outputs = []
    for current_file in input_files:
        current_output = []
        with open(current_file,'r') as data:
            for line in data:
                p=line.split()
                if len(p) == 0:
                    break
                else:
                    #lambdas.append(float(p[0]))
                    current_output.append(float(p[1]))
        flick_outputs.append(current_output)
    return flick_outputs

def extract_solar_irradiance(filepath, lambdas):
    solar_irradiance = []
    with open(filepath,'r') as data:
        for line in data:
            if line.strip() == "/end_header":
                break
        for line in data:
            p=line.split()
            #print(p)
            for i in lambdas:
             #   print(i)
                if float(p[0]) == float(i):
                    solar_irradiance.append(float(p[1]))
    return solar_irradiance

solar_irradiance = extract_solar_irradiance("/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/ContrastingSamples_config_outputs/getSpecRef/spectral_solar_constant.txt",lambdas)

nadir_clouds_flick_output = get_flick_output(clouds_nadir_Ed)
nadir_clear_flick_output = get_flick_output(clear_nadir_Ed)

clouds_flick_output_50 = get_flick_output(clouds_50_Ed)
clear_flick_output_50 = get_flick_output(clear_50_Ed)

clouds_flick_output_75 = get_flick_output(clouds_75_Ed)
clear_flick_output_75 = get_flick_output(clear_75_Ed)

nadir_clouds_Lw_flick_output = get_flick_output(clouds_nadir_Lw)
nadir_clear_Lw_flick_output = get_flick_output(clear_nadir_Lw)  

clouds_Lw_flick_output_50 = get_flick_output(clouds_50_Lw)
clear_Lw_flick_output_50 = get_flick_output(clear_50_Lw)

clouds_Lw_flick_output_75 = get_flick_output(clouds_75_Lw)
clear_Lw_flick_output_75 = get_flick_output(clear_75_Lw)

def calculate_BOA_Ed_Lw(flick_output, lambds, solar_constant):
    Eds = []
    for j in flick_output:
        current_flick_output = j
        current_Ed = np.zeros(len(lambds))
        for i in range(len(lambds)):
            current_Ed[i] = current_flick_output[i] * solar_constant[i]
        Eds.append(current_Ed)
    return Eds

BOA_Ed_nadir_clouds = calculate_BOA_Ed_Lw(nadir_clouds_flick_output,lambdas,solar_irradiance)
BOA_Ed_nadir_clear = calculate_BOA_Ed_Lw(nadir_clear_flick_output,lambdas,solar_irradiance)

BOA_Ed_50_clouds = calculate_BOA_Ed_Lw(clouds_flick_output_50,lambdas,solar_irradiance)
BOA_Ed_50_clear = calculate_BOA_Ed_Lw(clear_flick_output_50,lambdas,solar_irradiance)  

BOA_Ed_75_clouds = calculate_BOA_Ed_Lw(clouds_flick_output_75,lambdas,solar_irradiance)
BOA_Ed_75_clear = calculate_BOA_Ed_Lw(clear_flick_output_75,lambdas,solar_irradiance)

BOA_Lw_nadir_clouds = calculate_BOA_Ed_Lw(nadir_clouds_Lw_flick_output,lambdas,solar_irradiance)
BOA_Lw_nadir_clear = calculate_BOA_Ed_Lw(nadir_clear_Lw_flick_output,lambdas,solar_irradiance)

BOA_Lw_50_clouds = calculate_BOA_Ed_Lw(clouds_Lw_flick_output_50,lambdas,solar_irradiance)
BOA_Lw_50_clear = calculate_BOA_Ed_Lw(clear_Lw_flick_output_50,lambdas,solar_irradiance)

BOA_Lw_75_clouds = calculate_BOA_Ed_Lw(clouds_Lw_flick_output_75,lambdas,solar_irradiance)
BOA_Lw_75_clear = calculate_BOA_Ed_Lw(clear_Lw_flick_output_75,lambdas,solar_irradiance)

def calculate_differences(clear_BOA,cloudy_BOA):
    differences = []
    for i in range(len(clear_BOA)):
        current_difference = np.zeros(len(lambdas))
        for j in range(len(lambdas)):
            current_difference[j] = ((cloudy_BOA[i][j]-clear_BOA[i][j])/clear_BOA[i][j])*100
        differences.append(current_difference)
    return differences


def filter_lambdas_and_data(lambdas, data, desired_lambdas):
    indices = [lambdas.index(d) for d in desired_lambdas if d in lambdas]
    filtered_lambdas = [lambdas[i] for i in indices]
    filtered_data = [[row[i] for i in indices] for row in data]
    return filtered_lambdas, filtered_data

desired_lambdas = [400, 413, 443, 510, 560, 620, 665, 674, 709, 754, 780]

_, nadir_clouds_flick_output = filter_lambdas_and_data(lambdas, nadir_clouds_flick_output, desired_lambdas)
_, nadir_clear_flick_output = filter_lambdas_and_data(lambdas, nadir_clear_flick_output, desired_lambdas)
_, clouds_flick_output_50 = filter_lambdas_and_data(lambdas, clouds_flick_output_50, desired_lambdas)
_, clear_flick_output_50 = filter_lambdas_and_data(lambdas, clear_flick_output_50, desired_lambdas)
_, clouds_flick_output_75 = filter_lambdas_and_data(lambdas, clouds_flick_output_75, desired_lambdas)
_, clear_flick_output_75 = filter_lambdas_and_data(lambdas, clear_flick_output_75, desired_lambdas)
_, nadir_clouds_Lw_flick_output = filter_lambdas_and_data(lambdas, nadir_clouds_Lw_flick_output, desired_lambdas)
_, nadir_clear_Lw_flick_output = filter_lambdas_and_data(lambdas, nadir_clear_Lw_flick_output, desired_lambdas)
_, clouds_Lw_flick_output_50 = filter_lambdas_and_data(lambdas, clouds_Lw_flick_output_50, desired_lambdas)
_, clear_Lw_flick_output_50 = filter_lambdas_and_data(lambdas, clear_Lw_flick_output_50, desired_lambdas)
_, clouds_Lw_flick_output_75 = filter_lambdas_and_data(lambdas, clouds_Lw_flick_output_75, desired_lambdas)
_, clear_Lw_flick_output_75 = filter_lambdas_and_data(lambdas, clear_Lw_flick_output_75, desired_lambdas)
_, BOA_Ed_nadir_clouds = filter_lambdas_and_data(lambdas, BOA_Ed_nadir_clouds, desired_lambdas)
_, BOA_Ed_nadir_clear = filter_lambdas_and_data(lambdas, BOA_Ed_nadir_clear, desired_lambdas)
_, BOA_Ed_50_clouds = filter_lambdas_and_data(lambdas, BOA_Ed_50_clouds, desired_lambdas)
_, BOA_Ed_50_clear = filter_lambdas_and_data(lambdas, BOA_Ed_50_clear, desired_lambdas)
_, BOA_Ed_75_clouds = filter_lambdas_and_data(lambdas, BOA_Ed_75_clouds, desired_lambdas)
_, BOA_Ed_75_clear = filter_lambdas_and_data(lambdas, BOA_Ed_75_clear, desired_lambdas)
_, BOA_Lw_nadir_clouds = filter_lambdas_and_data(lambdas, BOA_Lw_nadir_clouds, desired_lambdas)
_, BOA_Lw_nadir_clear = filter_lambdas_and_data(lambdas, BOA_Lw_nadir_clear, desired_lambdas)
_, BOA_Lw_50_clouds = filter_lambdas_and_data(lambdas, BOA_Lw_50_clouds, desired_lambdas)
_, BOA_Lw_50_clear = filter_lambdas_and_data(lambdas, BOA_Lw_50_clear, desired_lambdas)
_, BOA_Lw_75_clouds = filter_lambdas_and_data(lambdas, BOA_Lw_75_clouds, desired_lambdas)
_, BOA_Lw_75_clear = filter_lambdas_and_data(lambdas, BOA_Lw_75_clear, desired_lambdas)

lambdas, _ = filter_lambdas_and_data(lambdas, [lambdas], desired_lambdas)

BOA_Ed_nadir_differences = calculate_differences(BOA_Ed_nadir_clear,BOA_Ed_nadir_clouds)
BOA_Ed_50_differences = calculate_differences(BOA_Ed_50_clear,BOA_Ed_50_clouds)
BOA_Ed_75_differences = calculate_differences(BOA_Ed_75_clear,BOA_Ed_75_clouds)

BOA_Lw_nadir_differences = calculate_differences(BOA_Lw_nadir_clear,BOA_Lw_nadir_clouds)
BOA_Lw_50_differences = calculate_differences(BOA_Lw_50_clear,BOA_Lw_50_clouds)
BOA_Lw_75_differences = calculate_differences(BOA_Lw_75_clear,BOA_Lw_75_clouds)

_, BOA_Ed_nadir_differences = filter_lambdas_and_data(lambdas, BOA_Ed_nadir_differences, desired_lambdas)
_, BOA_Ed_50_differences = filter_lambdas_and_data(lambdas, BOA_Ed_50_differences, desired_lambdas)
_, BOA_Ed_75_differences = filter_lambdas_and_data(lambdas, BOA_Ed_75_differences, desired_lambdas)
_, BOA_Lw_nadir_differences = filter_lambdas_and_data(lambdas, BOA_Lw_nadir_differences, desired_lambdas)
_, BOA_Lw_50_differences = filter_lambdas_and_data(lambdas, BOA_Lw_50_differences, desired_lambdas)
_, BOA_Lw_75_differences = filter_lambdas_and_data(lambdas, BOA_Lw_75_differences, desired_lambdas)

def calculate_rrs(Ed, Lw):
    rrs = []
    for i in range(len(Ed)):
        current_rrs = np.zeros(len(lambdas))
        for j in range(len(lambdas)):
            current_rrs[j] = Lw[i][j]/Ed[i][j]
        rrs.append(current_rrs)
    return rrs

BOA_rrs_nadir_clouds = calculate_rrs(BOA_Ed_nadir_clouds,BOA_Lw_nadir_clouds)
BOA_rrs_nadir_clear = calculate_rrs(BOA_Ed_nadir_clear,BOA_Lw_nadir_clear)
BOA_rrs_50_clouds = calculate_rrs(BOA_Ed_50_clouds,BOA_Lw_50_clouds)
BOA_rrs_50_clear = calculate_rrs(BOA_Ed_50_clear,BOA_Lw_50_clear)
BOA_rrs_75_clouds = calculate_rrs(BOA_Ed_75_clouds,BOA_Lw_75_clouds)    
BOA_rrs_75_clear = calculate_rrs(BOA_Ed_75_clear,BOA_Lw_75_clear)   

BOA_rrs_nadir_differences = calculate_differences(BOA_rrs_nadir_clear,BOA_rrs_nadir_clouds)
BOA_rrs_50_differences = calculate_differences(BOA_rrs_50_clear,BOA_rrs_50_clouds)
BOA_rrs_75_differences = calculate_differences(BOA_rrs_75_clear,BOA_rrs_75_clouds)

_, BOA_rrs_nadir_differences = filter_lambdas_and_data(lambdas, BOA_rrs_nadir_differences, desired_lambdas)
_, BOA_rrs_50_differences = filter_lambdas_and_data(lambdas, BOA_rrs_50_differences, desired_lambdas)
_, BOA_rrs_75_differences = filter_lambdas_and_data(lambdas, BOA_rrs_75_differences, desired_lambdas)

fig,ax=plt.subplots(1,2,figsize=(10, 4), sharex=True, sharey=False)
plt.grid('on')
ax[0].grid(which='major', alpha=0.4)
ax[0].set_title("Clear Skies",fontsize=16)
#axs[1].set_ylabel(r"BOA Ed clear ",fontsize=16)
ax[0].set_xlabel("Wavelength [nm]",fontsize=16)
ax[0].set_ylabel(r"Downward irradiance [W m$^{-2}$ nm$^{-1}$]", fontsize=16)
line1, = ax[0].plot(lambdas,BOA_Ed_50_clear[0],color=colors[3],linestyle = 'dotted',label = "Gaupnefjord")
line2, = ax[0].plot(lambdas,BOA_Ed_50_clear[1],color=colors[6],linestyle = '--',label = "Hardangerfjord")
line3, = ax[0].plot(lambdas,BOA_Ed_50_clear[3],color=colors[4],label = "Coastal San Diego")
line4, = ax[0].plot(lambdas,BOA_Ed_50_clear[2],color=colors[2],linestyle='-.', label = "Beaufort Sea")
ax[0].legend(['Hardangerfjord','Coastal San Diego'])

ax[1].grid(which='major', alpha=0.4)
ax[1].set_title(r"Clouds", fontsize=16)
ax[1].set_xlabel("Wavelength [nm]",fontsize=16)
ax[1].plot(lambdas,BOA_Ed_50_clouds[0],color=colors[3],linestyle = 'dotted')
ax[1].plot(lambdas,BOA_Ed_50_clouds[1],color=colors[6],linestyle = '--')
ax[1].plot(lambdas,BOA_Ed_50_clouds[3],color=colors[4])
ax[1].plot(lambdas,BOA_Ed_50_clouds[2],color=colors[2],linestyle='-.')

ax[0].set_xticks([400, 500, 600, 700, 800])
ax[0].set_ylim([100,170])
ax[1].set_xticks([400, 500, 600, 700, 800])
#ax[1].set_ylim([60,100])
ax[0].legend([line1, line2, line4, line3], 
             ['Gaupnefjord', 'Hardangerfjord', 'Beaufort Sea', 'Coastal San Diego'],
             loc="lower left", fontsize="medium")

fig.savefig("/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/Figures/BOA_Ed_50Sun.pdf",bbox_inches="tight",dpi=600)


# axs[2].grid(which='major', alpha=0.4)
# axs[2].plot(lambdas,BOA_Ed_75_clear[0],color=colors[3],linestyle = 'dotted')
# axs[2].plot(lambdas,BOA_Ed_75_clear[1],color=colors[6],linestyle = '--')
# axs[2].plot(lambdas,BOA_Ed_75_clear[2],color=colors[2],linestyle='-.')
# axs[2].plot(lambdas,BOA_Ed_75_clear[3],color=colors[4])
# axs[2].set_title("Sun 0$^\circ$",fontsize=16)
# axs[2].set_ylabel(r"BOA Ed difference clouds/clear ",fontsize=16)
# axs[2].set_xlabel("Wavelength [nm]",fontsize=16)
# axs[2].annotate(
# '(c)',
# xy=(0, 1), xycoords='axes fraction',
# xytext=(+0.5, -0.5), textcoords='offset fontsize',
# fontsize=16, verticalalignment='top',
# bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
# axs[2].tick_params(axis='both', which='major', labelsize=14)

# axs[2].grid(which='major', alpha=0.4)
# axs[2].plot(lambdas,BOA_Ed_50_clouds[0],color=colors[3],linestyle = 'dotted')
# axs[2].plot(lambdas,BOA_Ed_50_clouds[1],color=colors[6],linestyle = '--')
# axs[2].plot(lambdas,BOA_Ed_50_clouds[2],color=colors[2],linestyle='-.')
# axs[2].plot(lambdas,BOA_Ed_50_clouds[3],color=colors[4])
# axs[2].set_title("Sun 75$^\circ$",fontsize=16)
# axs[2].set_xlabel("Wavelength [nm]",fontsize=16)
# #axs[2].legend(['GF217','K1s','VF17'],bbox_to_anchor = [0.1, 0.45])

# axs[2].annotate(
# '(c)',
# xy=(0, 1), xycoords='axes fraction',
# xytext=(+0.5, -0.5), textcoords='offset fontsize',
# fontsize=16, verticalalignment='top',
# bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
# axs[2].tick_params(axis='both', which='major', labelsize=14)


fig2,axs2 = plt.subplots(3,3, sharex=True, figsize=(14,12))
plt.grid('on')

axs2[0,0].grid(which='major', alpha=0.4)
axs2[0,0].plot(lambdas,BOA_Ed_nadir_differences[0],color=colors[3],linestyle = 'dotted')
axs2[0,0].plot(lambdas,BOA_Ed_nadir_differences[1],color=colors[6],linestyle = '--')
axs2[0,0].plot(lambdas,BOA_Ed_nadir_differences[2],color=colors[2],linestyle='-.')
axs2[0,0].plot(lambdas,BOA_Ed_nadir_differences[3],color=colors[4])
axs2[0,0].set_xticks([400, 500, 600, 700, 800])
axs2[0,0].set_title("Sun 0$^\circ$",fontsize=16)#axs[1].set_ylim([0,125])
#axs2[0,0].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[0,0].annotate(
'(a)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[0,0].tick_params(axis='both', which='major', labelsize=14)
axs2[0,0].set_ylabel(r"Change in E$_d$ [%]",fontsize=16)

axs2[0,1].grid(which='major', alpha=0.4)
axs2[0,1].plot(lambdas,BOA_Ed_50_differences[0],color=colors[3],linestyle = 'dotted')
axs2[0,1].plot(lambdas,BOA_Ed_50_differences[1],color=colors[6],linestyle = '--')
axs2[0,1].plot(lambdas,BOA_Ed_50_differences[2],color=colors[2],linestyle='-.')
axs2[0,1].plot(lambdas,BOA_Ed_50_differences[3],color=colors[4])
axs2[0,1].set_title("Sun 50$^\circ$",fontsize=16)
axs2[0,1].set_xticks([400, 500, 600, 700, 800])
#axs2[0,1].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[0,1].annotate( 
'(b)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[0,1].tick_params(axis='both', which='major', labelsize=14)
axs2[0,1].legend(['Gaupnefjord','Hardangerfjord','Beaufort Sea','Coastal San Diego'],loc = "upper right",fontsize="medium")#,bbox_to_anchor = [0.1, 0.45])


axs2[0,2].grid(which='major', alpha=0.4)
axs2[0,2].plot(lambdas,BOA_Ed_75_differences[0],color=colors[3],linestyle = 'dotted')
axs2[0,2].plot(lambdas,BOA_Ed_75_differences[1],color=colors[6],linestyle = '--')
axs2[0,2].plot(lambdas,BOA_Ed_75_differences[2],color=colors[2],linestyle='-.')
axs2[0,2].plot(lambdas,BOA_Ed_75_differences[3],color=colors[4])
axs2[0,2].set_title("Sun 75$^\circ$",fontsize=16)
#axs2[0,2].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[0,2].annotate(   
'(c)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[0,2].tick_params(axis='both', which='major', labelsize=14)

axs2[1,0].grid(which='major', alpha=0.4)
axs2[1,0].plot(lambdas,BOA_Lw_nadir_differences[0],color=colors[3],linestyle = 'dotted')
axs2[1,0].plot(lambdas,BOA_Lw_nadir_differences[1],color=colors[6],linestyle = '--')
axs2[1,0].plot(lambdas,BOA_Lw_nadir_differences[2],color=colors[2],linestyle='-.')
axs2[1,0].plot(lambdas,BOA_Lw_nadir_differences[3],color=colors[4])
axs2[1,0].set_xticks([400, 500, 600, 700, 800])

#axs2[1,0].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[1,0].annotate( 
'(d)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[1,0].tick_params(axis='both', which='major', labelsize=14) 
axs2[1,0].set_ylabel(r"Change in L$_w$ [%]",fontsize=16)

axs2[1,1].grid(which='major', alpha=0.4)
axs2[1,1].plot(lambdas,BOA_Lw_50_differences[0],color=colors[3],linestyle = 'dotted')
axs2[1,1].plot(lambdas,BOA_Lw_50_differences[1],color=colors[6],linestyle = '--')
axs2[1,1].plot(lambdas,BOA_Lw_50_differences[2],color=colors[2],linestyle='-.')
axs2[1,1].plot(lambdas,BOA_Lw_50_differences[3],color=colors[4])
axs2[1,1].set_xticks([400, 500, 600, 700, 800])

#axs2[1,1].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[1,1].annotate(
'(e)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[1,1].tick_params(axis='both', which='major', labelsize=14)

axs2[1,2].grid(which='major', alpha=0.4)
axs2[1,2].plot(lambdas,BOA_Lw_75_differences[0],color=colors[3],linestyle = 'dotted')
axs2[1,2].plot(lambdas,BOA_Lw_75_differences[1],color=colors[6],linestyle = '--')
axs2[1,2].plot(lambdas,BOA_Lw_75_differences[2],color=colors[2],linestyle='-.')
axs2[1,2].plot(lambdas,BOA_Lw_75_differences[3],color=colors[4])
axs2[1,2].set_xticks([400, 500, 600, 700, 800])

#axs2[1,2].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[1,2].annotate(
'(f)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[1,2].tick_params(axis='both', which='major', labelsize=14)

axs2[2,0].grid(which='major', alpha=0.4)
axs2[2,0].plot(lambdas,BOA_rrs_nadir_differences[0],color=colors[3],linestyle = 'dotted')
axs2[2,0].plot(lambdas,BOA_rrs_nadir_differences[1],color=colors[6],linestyle = '--')
axs2[2,0].plot(lambdas,BOA_rrs_nadir_differences[2],color=colors[2],linestyle='-.')
axs2[2,0].plot(lambdas,BOA_rrs_nadir_differences[3],color=colors[4])
axs2[2,0].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[2,0].annotate( 
'(g)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[2,0].tick_params(axis='both', which='major', labelsize=14) 
axs2[2,0].set_ylabel(r"Change in R$_{rs}$ [%]",fontsize=16) 

axs2[2,1].grid(which='major', alpha=0.4)
axs2[2,1].plot(lambdas,BOA_rrs_50_differences[0],color=colors[3],linestyle = 'dotted')
axs2[2,1].plot(lambdas,BOA_rrs_50_differences[1],color=colors[6],linestyle = '--')
axs2[2,1].plot(lambdas,BOA_rrs_50_differences[2],color=colors[2],linestyle='-.')
axs2[2,1].plot(lambdas,BOA_rrs_50_differences[3],color=colors[4])
axs2[2,1].set_xticks([400, 500, 600, 700, 800])

axs2[2,1].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[2,1].annotate(
'(h)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[2,1].tick_params(axis='both', which='major', labelsize=14)

axs2[2,2].grid(which='major', alpha=0.4)
axs2[2,2].plot(lambdas,BOA_rrs_75_differences[0],color=colors[3],linestyle = 'dotted')
axs2[2,2].plot(lambdas,BOA_rrs_75_differences[1],color=colors[6],linestyle = '--')
axs2[2,2].plot(lambdas,BOA_rrs_75_differences[2],color=colors[2],linestyle='-.')
axs2[2,2].plot(lambdas,BOA_rrs_75_differences[3],color=colors[4])
axs2[2,2].set_xticks([400, 500, 600, 700, 800])

axs2[2,2].set_xlabel("Wavelength [nm]",fontsize=16)
axs2[2,2].annotate( 
'(i)',
xy=(0, 1), xycoords='axes fraction',
xytext=(+0.5, -0.5), textcoords='offset fontsize',
fontsize=16, verticalalignment='top',
bbox=dict(facecolor='1', edgecolor='none', pad=3.0))
axs2[2,2].tick_params(axis='both', which='major', labelsize=14)

fig2.savefig("/Users/sheacheatham/Documents/GitHub/FlickTests/SensitivityAnalyses/ContrastingSamples/Figures/BOA_Ed_Lw_Rrs_Differences.pdf",bbox_inches="tight",dpi=600)

