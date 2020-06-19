import matplotlib.pyplot as plt

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
        "Meta-flip0.1 Train-flip0.3",
        "Meta-flip0.1 Train-flip0.6"],
        #5
        ["Meta-unif0.1 Train-unit0.1",   #6
        "Meta-unif0.1 Train-unit0.3",
        "Meta-unif0.1 Train-unif0.6"],
        #6
        ["Meta-flip0.3 Train-flip0.3",   #5
        "Meta-flip0.3 Train-flip0.6",
        "Meta-flip0.6 Train-flip0.6",
        ],
        #7
        ["Meta-unif0.3 Train-unif0.3",   #7
        "Meta-unif0.3 Train-unif0.6",
        "Meta-unif0.6 Train-unif0.6",
        ]
    ]
filename = [
        #0
        ['Falseclean0.0flip0.11.txt',
        'Falseclean0.0flip0.31.txt',
        'Falseclean0.0flip0.61.txt'],
        #1
        ['Falseclean0.0unif0.11.txt',
        'Falseclean0.0unif0.31.txt',
        'Falseclean0.0unif0.61.txt'
        ],
        #2
        ['clean0.0flip0.10.txt',
        'clean0.0flip0.30.txt',
       'clean0.0flip0.60.txt',
        ],
        #3
        ['clean0.0unif0.10.txt',
        'clean0.0unif0.30.txt',
        'clean0.0unif0.60.txt'
        ],
        #4
        ["flip0.1flip0.10.txt",
        "flip0.1flip0.30.txt",
        "flip0.1flip0.60.txt"],
        #5
        ['unif0.1unif0.10.txt',
        'unif0.1unif0.30.txt',
        'unif0.1unif0.60.txt'],
        #6
        ["flip0.3flip0.30.txt",
        "flip0.3flip0.60.txt",
        "flip0.6flip0.60.txt"
        ],
        #7
        ['unif0.3unif0.30.txt',
            'unif0.3unif0.60.txt',
            'unif0.6unif0.60.txt',
        ]
    ]

results = []
for j in range(len(filename)):
    _res = []
    for i in range(len(filename[j])):
        list_read = []
        f = open(filename[j][i], 'r')
        a = f.readline(10)\

        while (len(a) != 0):
            a = f.readline()
            if a[0:6] == "EPOCH ":
                list_read.append(float(a[6:-1]))
            else:
                for k in range(len(a)):
                    if a[k] == "Y":
                        list_read.append(float(a[k+1:-1]))
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