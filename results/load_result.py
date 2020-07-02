import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

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
        ['cifar10clean0.0flip0.120200626-022148.txt',
        'cifar10clean0.0flip0.320200626-184047.txt',
        'cifar10clean0.0flip0.620200627-114932.txt'],
        #1
        ['cifar10clean0.0unif0.120200626-022342.txt',
        'cifar10clean0.0unif0.320200626-184918.txt',
        'cifar10clean0.0unif0.620200627-120317.txt'
        ],
        #2
        ['cifar10clean0.0flip0.120200626-022420.txt',
        'cifar10clean0.0flip0.320200627-184557.txt',
       'cifar10clean0.0flip0.620200629-054355.txt',
        ],
        #3
        ['cifar10clean0.0unif0.120200626-022459.txt',
        'cifar10clean0.0unif0.320200627-181652.txt',
        'cifar10clean0.0unif0.620200629-051705.txt'
        ],
        #4
        ["cifar10flip0.1flip0.120200626-022525.txt",
        "cifar10flip0.3flip0.320200627-182431.txt",
        "cifar10flip0.6flip0.620200629-042157.txt"
        ],
        #5
        ['cifar10unif0.1unif0.120200626-022555.txt',
        'cifar10unif0.3unif0.320200627-183927.txt',
        'cifar10unif0.6unif0.620200629-050247.txt'],
        #6
        ["cifar10flip0.1flip0.320200626-022622.txt",
        "cifar10flip0.1flip0.620200627-182401.txt",
        "cifar10flip0.3flip0.620200629-040510.txt"],
        #7
        ['cifar10unif0.1unif0.320200626-022642.txt',
        'cifar10unif0.1unif0.620200627-184054.txt',
        'cifar10unif0.3unif0.620200629-051132.txt']
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
plt.title("Clean Metadata Exists")
for j in [0,1,2,3]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        plt.plot(x, results[j][i], alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig("Clean Metadata Exists.png")
plt.cla()

# 0,1, 4,5
plt.figure(figsize=(12,8))
plt.title("Same level corruption")
for j in [0,1,4,5]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        plt.plot(x, results[j][i], alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig("Same level corruption.png")
plt.cla()

# 0,1, 6,7
plt.figure(figsize=(12,8))
plt.title("Worse Traindata")
for j in [0,1,6,7]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        plt.plot(x, results[j][i], alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig("Worse Traindata.png")
plt.cla()

############ smoothing
win_sz=51
order=3

# 0,1, 2,3
plt.figure(figsize=(12,8))
plt.title("[filtered]Clean Metadata Exists")
for j in [0,1,2,3]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        yhat = savgol_filter(results[j][i], win_sz, order)
        plt.plot(x, yhat, alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig("[filtered]Clean Metadata Exists.png")
plt.cla()

# 0,1, 4,5
plt.figure(figsize=(12,8))
plt.title("[filtered]Same level corruption")
for j in [0,1,4,5]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        yhat = savgol_filter(results[j][i], win_sz, order)
        plt.plot(x, yhat, alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig("[filtered]Same level corruption.png")
plt.cla()

# 0,1, 6,7
plt.figure(figsize=(12,8))
plt.title("[filtered]Worse Traindata")
for j in [0,1,6,7]:
    for i in range(len(results[j])):
        x = [k for k in range(1,len(results[j][i])+1)]
        yhat = savgol_filter(results[j][i], win_sz, order)
        plt.plot(x, yhat, alpha=0.7, label=titles[j][i], color=colors[j], linestyle=lstyle[i])
plt.legend()
plt.grid()
plt.savefig("[filtered]Worse Traindata.png")
plt.cla()


#=============== GAP ==================
# 0,1, 6,7
plt.figure(figsize=(12,8))
plt.title("[GAP]Worse Traindata")

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
plt.savefig("[GAP]Worse Traindata.png")
plt.cla()

#=====================
# 0,1, 4,5
plt.figure(figsize=(12,8))
plt.title("[GAP]Same Level Corruption")

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
plt.savefig("[GAP]Same Level Corruption.png")
plt.cla()

#=====================
# 0,1, 2,3
plt.figure(figsize=(12,8))
plt.title("[GAP]Clean Meta Exist")

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
plt.savefig("[GAP]Clean Meta Exist.png")
plt.cla()
