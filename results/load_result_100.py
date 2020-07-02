import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

Dataset = "CIFAR100"
# [8][3]
titles = [
        #0
        ["Basic flip0.1",
        "Basic flip0.3",
        "Basic flip0.6"],
        #1
        ["Basic unif0.1",
        "Basic unif0.3",
        "Basic unif0.60"
        ],
        #2
        ['Meta-clean Train-flip0.1',   #0
        "Meta-clean Train-flip0.3",
        "Meta-clean Train-flip0.6",
        ],
        #3
        ["Meta-clean Train-unif0.1",     #1
        "Meta-clean Train-unif0.3",
        "Meta-clean Train-unif0.6",
        ],
        #4
        ["Meta-flip0.1 Train-flip0.1",  #4
        "Meta-flip0.3 Train-flip0.3",   #5
        "Meta-flip0.6 Train-flip0.6",
        ],
        #5
        ["Meta-unif0.1 Train-unit0.1",
        "Meta-unif0.3 Train-unif0.3",
        "Meta-unif0.6 Train-unif0.6"],
        #6
        ["Meta-flip0.1 Train-flip0.3",
        "Meta-flip0.1 Train-flip0.6",
        "Meta-flip0.3 Train-flip0.6"],
        #7
        ["Meta-unif0.1 Train-unit0.3",
        "Meta-unif0.1 Train-unif0.6",
        "Meta-unif0.3 Train-unif0.6",
        ]
    ]
filename = [
        #0
        ['cifar100clean0.0flip0.120200626-022720.txt',
        'cifar100clean0.0flip0.320200626-190502.txt',
        'cifar100clean0.0flip0.620200627-121441.txt'],
        #1
        ['cifar100clean0.0unif0.120200626-022748.txt',
        'cifar100clean0.0unif0.320200626-191052.txt',
        'cifar100clean0.0unif0.620200627-122238.txt'
        ],
        #2
        ['cifar100clean0.0flip0.120200626-022817.txt',
        'cifar100clean0.0flip0.320200627-184724.txt',
       'cifar100clean0.0flip0.620200629-053529.txt',
        ],
        #3
        ['cifar100clean0.0unif0.120200626-022939.txt',
        'cifar100clean0.0unif0.320200627-183958.txt',
        'cifar100clean0.0unif0.620200629-054008.txt'
        ],
        #4
        ["cifar100flip0.1flip0.120200626-023018.txt",
        "cifar100flip0.3flip0.320200627-182318.txt",
        "cifar100flip0.6flip0.620200629-042817.txt"
        ],
        #5
        ['cifar100unif0.1unif0.120200626-023120.txt',
        'cifar100unif0.3unif0.320200627-190342.txt',
        'cifar100unif0.6unif0.620200629-053750.txt'],
        #6
        ["cifar100flip0.1flip0.320200626-023155.txt",
        "cifar100flip0.1flip0.620200627-190018.txt",
        "cifar100flip0.3flip0.620200629-045914.txt"],
        #7
        ['cifar100unif0.1unif0.320200626-023222.txt',
        'cifar100unif0.1unif0.620200627-185404.txt',
        'cifar100unif0.3unif0.620200629-044026.txt']
    ]

results = []
for j in range(len(filename)):
    _res = []
    for i in range(len(filename[j])):
        list_read = []
        f = open(filename[j][i], 'r')
        a = f.readline()

        while (len(a) != 0):
            a = f.readline()
            if a[0] == "T":
                a = f.readline()
                a = a.split(" ")[:-1]
                a = [float(item) for item in a]
                list_read = a
                break
        f.close()
        plt.title(titles[j][i])
        x = [i for i in range(1,len(list_read)+1)]
        plt.plot(x, list_read)
        plt.grid()
        plt.savefig(titles[j][i]+".png")
        plt.cla()

        _res.append(list_read)
    results.append(_res)
"""
# entire plot
plt.title("compare test accuracy")
plt.figure(figsize=(15,10))
for i in range(len(filename)):
    x = [k for k in range(1,len(results[i])+1)]
    plt.plot(x, results[i], alpha=0.8, label=titles[i]) #, color=colors[i])
plt.legend()
plt.grid()
plt.savefig("entire.png")
"""


colors = ['black', 'grey', 'red', 'blue', 'purple', 'green', 'cyan', 'magenta']
lstyle=['-', '-.', '--']

# 0,1, 2,3
plt.figure(figsize=(12,8))
plt.title(Dataset+"_Clean Metadata Exists")
for j in [0,1,2,3]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        plt.plot(x, results[j][i], alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig(Dataset+"_Clean Metadata Exists.png")
plt.cla()

# 0,1, 4,5
plt.figure(figsize=(12,8))
plt.title(Dataset+"_Same level corruption")
for j in [0,1,4,5]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        plt.plot(x, results[j][i], alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig(Dataset+"_Same level corruption.png")
plt.cla()

# 0,1, 6,7
plt.figure(figsize=(12,8))
plt.title(Dataset+"_Worse Traindata")
for j in [0,1,6,7]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        plt.plot(x, results[j][i], alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig(Dataset+"_Worse Traindata.png")
plt.cla()

############ smoothing
win_sz=51
order=3

# 0,1, 2,3
plt.figure(figsize=(12,8))
plt.title(Dataset+"_[filtered]Clean Metadata Exists")
for j in [0,1,2,3]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        yhat = savgol_filter(results[j][i], win_sz, order)
        plt.plot(x, yhat, alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig(Dataset+"_[filtered]Clean Metadata Exists.png")
plt.cla()

# 0,1, 4,5
plt.figure(figsize=(12,8))
plt.title(Dataset+"_[filtered]Same level corruption")
for j in [0,1,4,5]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        yhat = savgol_filter(results[j][i], win_sz, order)
        plt.plot(x, yhat, alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig(Dataset+"_[filtered]Same level corruption.png")
plt.cla()

# 0,1, 6,7
plt.figure(figsize=(12,8))
plt.title(Dataset+"_[filtered]Worse Traindata")
for j in [0,1,6,7]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        yhat = savgol_filter(results[j][i], win_sz, order)
        plt.plot(x, yhat, alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig(Dataset+"_[filtered]Worse Traindata.png")
plt.cla()


#=============== GAP ==================
# 0,1, 6,7
plt.figure(figsize=(12,8))
plt.title(Dataset+"_[GAP]Worse Traindata")

win_sz = 51
order = 3

noise_name = "flip"
base_num1 = 0
base_num2 = [1,2,2]
setting_1 = 6
setting_2 = [0,1,2]

for k in range(len(base_num2)):
    name = "#" + str(setting_1) + "-#"+str(base_num1)+", noise "+noise_name+str(setting_2[k])
    x = [k for k in range(1,len(results[j][i])+1)]
    gap = [a-b for a,b in zip(results[setting_1][setting_2[k]],results[base_num1][base_num2[k]])]
    gap = savgol_filter(gap, win_sz, order)
    plt.plot(x, gap, alpha=0.7, label=name, color=colors[setting_1], linestyle=lstyle[k])

noise_name = "unif"
base_num1 = 1
base_num2 = [1,2,2]
setting_1 = 7
setting_2 = [0,1,2]

for k in range(len(base_num2)):
    name = "#" + str(setting_1) + "-#"+str(base_num1)+", noise "+noise_name+str(setting_2[k])
    x = [k for k in range(1,len(results[j][i])+1)]
    gap = [a-b for a,b in zip(results[setting_1][setting_2[k]],results[base_num1][base_num2[k]])]
    gap = savgol_filter(gap, win_sz, order)
    plt.plot(x, gap, alpha=0.7, label=name, color=colors[setting_1], linestyle=lstyle[k])

plt.legend()
plt.grid()
plt.savefig(Dataset+"_[GAP]Worse Traindata.png")
plt.cla()

#=====================
# 0,1, 4,5
plt.figure(figsize=(12,8))
plt.title(Dataset+"_[GAP]Same Level Corruption")

win_sz = 51
order = 3

noise_name = "flip"
base_num1 = 0
base_num2 = [0,1,2]
setting_1 = 4
setting_2 = [0,1,2]

for k in range(len(base_num2)):
    name = "#" + str(setting_1) + "-#"+str(base_num1)+", noise "+noise_name+str(setting_2[k])
    x = [k for k in range(1,len(results[j][i])+1)]
    gap = [a-b for a,b in zip(results[setting_1][setting_2[k]],results[base_num1][base_num2[k]])]
    gap = savgol_filter(gap, win_sz, order)
    plt.plot(x, gap, alpha=0.7, label=name, color=colors[setting_1], linestyle=lstyle[k])

noise_name = "unif"
base_num1 = 1
base_num2 = [0,1,2]
setting_1 = 5
setting_2 = [0,1,2]

for k in range(len(base_num2)):
    name = "#" + str(setting_1) + "-#"+str(base_num1)+", noise "+noise_name+str(setting_2[k])
    x = [k for k in range(1,len(results[j][i])+1)]
    gap = [a-b for a,b in zip(results[setting_1][setting_2[k]],results[base_num1][base_num2[k]])]
    gap = savgol_filter(gap, win_sz, order)
    plt.plot(x, gap, alpha=0.7, label=name, color=colors[setting_1], linestyle=lstyle[k])

plt.legend()
plt.grid()
plt.savefig(Dataset+"_[GAP]Same Level Corruption.png")
plt.cla()

#=====================
# 0,1, 2,3
plt.figure(figsize=(12,8))
plt.title(Dataset+"_[GAP]Clean Meta Exist")

win_sz = 51
order = 3

noise_name = "flip"
base_num1 = 0
base_num2 = [0,1,2]
setting_1 = 2
setting_2 = [0,1,2]

for k in range(len(base_num2)):
    name = "#" + str(setting_1) + "-#"+str(base_num1)+", noise "+noise_name+str(setting_2[k])
    x = [k for k in range(1,len(results[j][i])+1)]
    gap = [a-b for a,b in zip(results[setting_1][setting_2[k]],results[base_num1][base_num2[k]])]
    gap = savgol_filter(gap, win_sz, order)
    plt.plot(x, gap, alpha=0.7, label=name, color=colors[setting_1], linestyle=lstyle[k])

noise_name = "unif"
base_num1 = 1
base_num2 = [0,1,2]
setting_1 = 3
setting_2 = [0,1,2]

for k in range(len(base_num2)):
    name = "#" + str(setting_1) + "-#"+str(base_num1)+", noise "+noise_name+str(setting_2[k])
    x = [k for k in range(1,len(results[j][i])+1)]
    gap = [a-b for a,b in zip(results[setting_1][setting_2[k]],results[base_num1][base_num2[k]])]
    gap = savgol_filter(gap, win_sz, order)
    plt.plot(x, gap, alpha=0.7, label=name, color=colors[setting_1], linestyle=lstyle[k])

plt.legend()
plt.grid()
plt.savefig(Dataset+"_[GAP]Clean Meta Exist.png")
plt.cla()
