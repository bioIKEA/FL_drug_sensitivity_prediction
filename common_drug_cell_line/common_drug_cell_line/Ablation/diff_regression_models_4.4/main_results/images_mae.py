# Figure 6
CCLE_GDSC=[]
CCLE_gCSI=[]
GDSC_gCSI=[]


ccle_gcsi_our_method_mae_nn=[0.08668495, 0.07448171, 0.087835446, 0.0762009, 0.07681237, 0.08894648, 0.08475392, 0.08796197, 0.085450694, 0.07325786]

ccle_gdsc_our_method_mae_nn=[0.06523813, 0.06446937, 0.06212968, 0.061930284, 0.06522192, 0.061260942, 0.063307256, 0.0634574, 0.06325646, 0.06310654]

gdsc_gcsi_our_method_mae_nn=[0.0513365, 0.057317026, 0.053249404, 0.050084595, 0.050829295, 0.053955108, 0.05450533, 0.051226508, 0.053906966, 0.049653683]


ccle_gcsi_our_method_mae_rf=[0.08618977710875342, 0.07661970903663616, 0.08005678537512055, 0.08069825124782602, 0.08739808098162671, 0.07877984248825101, 0.07976632945602367, 0.08553764167659418, 0.08186563667616899, 0.08189334137426695]



ccle_gdsc_our_method_mae_rf=[0.09254496144379804, 0.09235864536787654, 0.09146280108988285, 0.08995741082243752, 0.09005058345741583, 0.09170957498122545, 0.09873630847367071, 0.08886959922221338, 0.09189425196391522, 0.09302568333729831]

gdsc_gcsi_our_method_mae_rf=[0.08926223396724142, 0.09017880210685031, 0.07919247579551153, 0.08272057739890634, 0.08653573404777946, 0.08092202725801244, 0.0847823730556527, 0.08608143879495453, 0.08764086947495901, 0.08014624787022381]



ccle_gcsi_our_method_mae_ridge=[0.09575888916599974, 0.0894169623220406, 0.090283024712969, 0.08865641948824676, 0.09306425684891388, 0.08489963876603474, 0.09585022583638599, 0.09143204956726013, 0.09211219502259178, 0.08886173261354949]

ccle_gdsc_our_method_mae_ridge=[0.08811303000178299, 0.09252995270716392, 0.09021932089143504, 0.0903177913241033, 0.08995430507704989, 0.0922276995406163, 0.09615350730138658, 0.08833880968164165, 0.09089300838060944, 0.09332153990701968]


gdsc_gcsi_our_method_mae_ridge=[0.08706545407055087, 0.08880644290525962, 0.07433494395714559, 0.08088570642225983, 0.08668707561554091, 0.07983188163334322, 0.08232836125316662, 0.08360520288558185, 0.08534975292266915, 0.07828895251578143]


CCLE_GDSC.append(ccle_gdsc_our_method_mae_rf)
CCLE_GDSC.append(ccle_gdsc_our_method_mae_ridge)
CCLE_GDSC.append(ccle_gdsc_our_method_mae_nn)

CCLE_gCSI.append(ccle_gcsi_our_method_mae_rf)
CCLE_gCSI.append(ccle_gcsi_our_method_mae_ridge)
CCLE_gCSI.append(ccle_gcsi_our_method_mae_nn)

GDSC_gCSI.append(gdsc_gcsi_our_method_mae_rf)
GDSC_gCSI.append(gdsc_gcsi_our_method_mae_ridge)
GDSC_gCSI.append(gdsc_gcsi_our_method_mae_nn)

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
              'figure.figsize':(15,8),
    }

plt.rcParams.update(plot_fonts)

# plt.style.use('ggplot')
# plt.figure(figsize=(12,8))
plt.suptitle("MAE score comparison between different regressions")
for counter in range(len(datasets)):
    ax = plt.subplot(1, 3, counter + 1)
    main=ax.boxplot(datasets[counter], patch_artist=True, widths = 0.5)
    m = np.array(datasets[counter]).mean(axis=1)
    st = np.array(datasets[counter]).std(axis=1)
    ax.set_title(names[counter])
    # for i, line in enumerate(main['medians']):
    #     x, y = line.get_xydata()[1]
    #     text = ' μ={:.4f}\n σ={:.4f}'.format(m[i], st[i])
    #     ax.annotate(text, xy=(x, y))
        
    y_min = np.inf
    y_max = -np.inf
    for i, line in enumerate(main['whiskers']):
        x, y = line.get_xydata()[1]        
        y_min = np.min([y_min, y])
        y_max = np.max([y_max, y])
        if(i%2 == 0):
            text = ' μ={:.3f}\n σ={:.3f}'.format(m[int(i/2)], st[int(i/2)])
            ax.annotate(text, xy=(x, y-0.0035))         
        
    ax.set_xticks([1, 2,3])
    ax.set_xticklabels(["Random Forest", "Ridge Regression", "Neural Network"], rotation=45)
    ax.set_ylim(y_min-0.005,y_max+0.005)
    ax.set_xlim(0.5,3.75)
    plt.grid()
    colors=["forestgreen","yellow", "blue"]
     
    for patch, color in zip(main['boxes'],colors):
        patch.set_facecolor(color)
plt.tight_layout()
plt.savefig('Mae.png')
plt.savefig('Das_Leveraging_MultiSource_Figure 6.png')
plt.savefig('Das_Leveraging_MultiSource_Figure 6.pdf')
plt.savefig('Das_Leveraging_MultiSource_Figure 6.svg')
plt.show()
