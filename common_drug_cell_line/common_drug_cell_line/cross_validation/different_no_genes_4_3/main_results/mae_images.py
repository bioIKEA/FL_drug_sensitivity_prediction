our_method_mae=[[0.08862282551008656, 0.09205313974437195, 0.09073155491053839, 0.09044950217754473, 0.08999903510718579, 0.0921505597174794, 0.09697359666629869, 0.08832405500187171, 0.09109152025622125, 0.09379671289892162], [0.08816447597874805, 0.0922458847201788, 0.09057806439323297, 0.09032153446804278, 0.0894808878064025, 0.09196075301706667, 0.09605302820893584, 0.08786854081335574, 0.090640044677491, 0.09255691697524798], [0.08705124944558076, 0.09177875100329051, 0.08969573065530141, 0.09052125458055467, 0.08959477423245323, 0.09022784500620065, 0.09622143139923976, 0.08614958711094865, 0.09015917730563576, 0.09179793322797863], [0.08694601304383508, 0.09165336226082482, 0.08865581787325989, 0.08998378194048103, 0.0906611144340201, 0.08986126893020804, 0.09557258181139645, 0.08585787188407178, 0.08918447882539889, 0.090651880078215], [0.08695411418941358, 0.09165817804538928, 0.08865606635422663, 0.08998799084244602, 0.09067305163596122, 0.08985990159019977, 0.09557773109709826, 0.08585861315084804, 0.0891817240133414, 0.09065094012001543]]




methods={
        0:our_method_mae,
        }

names={
        0:"Our Method",
        }


# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



plt.style.use('ggplot')
plt.figure(figsize=(10,10))
plt.suptitle("MAE score comparison between different number of genes")
for counter in range(len(methods)):
    ax = plt.subplot(1, 1, counter + 1)
    main=ax.boxplot(methods[counter], patch_artist=True)
    m = np.array(methods[counter]).mean(axis=1)
    st = np.array(methods[counter]).std(axis=1)
    ax.set_title(names[counter])
    for i, line in enumerate(main['medians']):
        x, y = line.get_xydata()[1]
        text = ' μ={:.4f}\n σ={:.4f}'.format(m[i], st[i])
        ax.annotate(text, xy=(x, y))
    ax.set_xticks([1, 2,3,4, 5])
    ax.set_xticklabels(["50 genes","100 genes", "200 genes", "500 genes",'902 genes'], rotation=10)
    # ax.set_ylim(-20,10)

    colors=["forestgreen", "blue", "dimgray",  "slategray", "tomato"]
     
    for patch, color in zip(main['boxes'],colors):
        patch.set_facecolor(color)
plt.tight_layout()
plt.savefig('Mae_our_method_only.png')
plt.show()

