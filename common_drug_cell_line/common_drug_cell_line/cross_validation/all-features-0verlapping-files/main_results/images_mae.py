# Figure 3
CCLE_GDSC=[]
CCLE_gCSI=[]
GDSC_gCSI=[]

ccle_gdsc_our_method_mae=[0.08695411418941361, 0.0916581780453893, 0.08865606635422661, 0.08998799084244602, 0.09067305163596122, 0.08985990159019976, 0.09557773109709825, 0.08585861315084806, 0.08918172401334142, 0.09065094012001543]
ccle_gcsi_our_method_mae=[0.10348528176255219, 0.09223059358160807, 0.0935885495331036, 0.09404098776569114, 0.09278845291418235, 0.09273817991008082, 0.10231546838036956, 0.09253320682358902, 0.09864694455436673, 0.0956248566608895]
gdsc_gcsi_our_method_mae=[0.08379067090907578, 0.08774115488303427, 0.07315509908219545, 0.07938220261034372, 0.0841795070559512, 0.07757656419547433, 0.08029584750207251, 0.08213002851588548, 0.08300374160788844, 0.07614101205676678]



ccle_gdsc_combined_dataset_mae=[0.10494072971566162, 0.1054787515513821, 0.10749936694262581, 0.1056678092178499, 0.11083690534976871, 0.1018498117429481, 0.11445204087806617, 0.11026946732105922, 0.10369137169919392, 0.10757213324705588]
ccle_gcsi_combined_dataset_mae=[0.12205601841309921, 0.09845937803436793, 0.10998469457963303, 0.10398384654292006, 0.1009867427174397, 0.10001490743558944, 0.11621340085582202, 0.10615328975176395, 0.11480542452629128, 0.09993066557946077]
gdsc_gcsi_combined_dataset_mae=[0.09484003778826945, 0.09767140969714343, 0.08506039525057353, 0.0931755151257722, 0.10028342953095382, 0.09118846947663048, 0.09441078522962083, 0.09400210262039443, 0.09945084200028907, 0.09116890580339185]



ccle_gdsc_selected_best_mae=[0.1039382026653871, 0.10643200616142531, 0.10496980268471928, 0.10185158498787161, 0.10669024281523394, 0.1024814432581326, 0.11667468772582554, 0.10652137469029975, 0.10193166645458353, 0.1055220913455225]
ccle_gcsi_selected_best_mae=[0.10928136073773466, 0.10130548327269435, 0.10221525058501844, 0.09900379227234063, 0.10746235280316813, 0.10072429503401853, 0.10863568898814877, 0.11250720538795184, 0.10349246827587566, 0.10194847152930077]
gdsc_gcsi_selected_best_mae=[0.09883611823489111, 0.10644801153078064, 0.09179599356173125, 0.10183839633583208, 0.10763766471638982, 0.10143182297610948, 0.10110245678016436, 0.10192958131800833, 0.10628846801216367, 0.09382578395446861]




ccle_gdsc_weighted_average_mae=[0.10027124318932275, 0.10130038031907188, 0.10216096387508343, 0.09963949734570166, 0.10435904936729246, 0.09571961896444604, 0.1083089264918877, 0.10277726441551287, 0.09946793116836637, 0.10268519873575993]
ccle_gcsi_weighted_average_mae=[0.0996263381641745, 0.09124419569241721, 0.09634218087168575, 0.09337280969813001, 0.0934252864394043, 0.09128474582785603, 0.10352050928025314, 0.09447445293520947, 0.09761111543812721, 0.09166141321525773]
gdsc_gcsi_weighted_average_mae=[0.09193469874658436, 0.09725365511643487, 0.08307289796145675, 0.09160408841054071, 0.09930539747370916, 0.08947884642419315, 0.09199301124362409, 0.09222812486656089, 0.09726206193302012, 0.08856467763559671]



ccle_gdsc_model_average_mae=[0.09911027603367574, 0.10164072738120385, 0.10183515909515108, 0.09934906196076089, 0.10410879618882171, 0.0971320487719532, 0.10803650800890695, 0.10194752657200692, 0.10064816820132093, 0.10244442320329053]
ccle_gcsi_model_average_mae=[0.09737590298552071, 0.09083195712934197, 0.09275084588754884, 0.09209921757847576, 0.0951711683612694, 0.09138633089916162, 0.10013981567853861, 0.09337482792198903, 0.09322135474012977, 0.09144692946062731]
gdsc_gcsi_model_average_mae=[0.092209541124946, 0.09606871307922037, 0.08317398911804198, 0.09198140972233819, 0.09864522292574421, 0.09013277253163407, 0.0919117472092784, 0.0923991421080598, 0.09797115045948279, 0.08883558530688375]


CCLE_GDSC.append(ccle_gdsc_our_method_mae)
CCLE_GDSC.append(ccle_gdsc_combined_dataset_mae)
CCLE_GDSC.append(ccle_gdsc_selected_best_mae)
CCLE_GDSC.append(ccle_gdsc_weighted_average_mae)
CCLE_GDSC.append(ccle_gdsc_model_average_mae)

CCLE_gCSI.append(ccle_gcsi_our_method_mae)
CCLE_gCSI.append(ccle_gcsi_combined_dataset_mae)
CCLE_gCSI.append(ccle_gcsi_selected_best_mae)
CCLE_gCSI.append(ccle_gcsi_weighted_average_mae)
CCLE_gCSI.append(ccle_gcsi_model_average_mae)


GDSC_gCSI.append(gdsc_gcsi_our_method_mae)
GDSC_gCSI.append(gdsc_gcsi_combined_dataset_mae)
GDSC_gCSI.append(gdsc_gcsi_selected_best_mae)
GDSC_gCSI.append(gdsc_gcsi_weighted_average_mae)
GDSC_gCSI.append(gdsc_gcsi_model_average_mae)



datasets={
        0:CCLE_GDSC,
        1:CCLE_gCSI,
        2:GDSC_gCSI,
        }


names={
        0:"CCLE-GDSC",
        1:"CCLE-gCSI",
        2:"GDSC-gCSI"
        }


# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Plot fonts
plot_fonts = {'font.family':'Arial',
               'font.size' : 14,
              'figure.figsize':(18,6),
    }

plt.rcParams.update(plot_fonts)

positions = np.array([1, 2, 3, 4, 5])*1.9

# plt.style.use('ggplot')
# plt.figure(figsize=(15,6))
plt.suptitle("MAE score comparison between different methods")
for counter in range(len(datasets)):
    ax = plt.subplot(1, 3, counter + 1)
    main=ax.boxplot(datasets[counter], patch_artist=True, positions = positions, widths = 0.75)
    m = np.array(datasets[counter]).mean(axis=1)
    st = np.array(datasets[counter]).std(axis=1)
    ax.set_title(names[counter])
    # for i, line in enumerate(main['medians']):
    #     x, y = line.get_xydata()[1]
    #     text = ' μ={:.3f}\n σ={:.3f}'.format(m[i], st[i])
    #     ax.annotate(text, xy=(x, y))
        
    y_min = np.inf
    y_max = -np.inf
    for i, line in enumerate(main['whiskers']):
        x, y = line.get_xydata()[1]        
        y_min = np.min([y_min, y])
        y_max = np.max([y_max, y])
        if(i%2 == 0):
            text = ' μ={:.3f}\n σ={:.3f}'.format(m[int(i/2)], st[int(i/2)])
            ax.annotate(text, xy=(x, y-0.0045))
        
    ax.set_xticks(positions)
    ax.set_xticklabels(["Our Method","Combined Dataset", "Selected Best", "Weighted Average", "Model Average"], rotation=45)
    ax.set_ylim(y_min-0.005,y_max+0.005)
    ax.set_xlim(np.min(positions)-0.5,np.max(positions)+1.5)
    
    colors=["forestgreen","yellow", "blue", "dimgray", "orange"]
     
    plt.grid()
    
    for patch, color in zip(main['boxes'],colors):
        patch.set_facecolor(color)
plt.tight_layout()
plt.savefig('Das_Leveraging_MultiSource_Figure 3.png')
plt.savefig('Das_Leveraging_MultiSource_Figure 3.pdf')
plt.savefig('Das_Leveraging_MultiSource_Figure 3.svg')
plt.savefig('Mae.png')
plt.show()
