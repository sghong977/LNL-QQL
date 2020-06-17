import matplotlib.pyplot as plt

titles = ['Meta-clean Train-flip0.1',
        #
        "Meta-clean Train-unif0.1",
        #
        "Meta-flip0.1 Train-flip0.1",
        "Meta-flip0.1 Train-flip0.3",
        ##
        "Meta-unif0.1 Train-unit0.1",
        "Meta-unif0.1 Train-unit0.3",
        ##
        ]
filename = ['clean0.0flip0.10.txt',
            #
            'clean0.0unif0.10.txt',
            #
            "flip0.1flip0.10.txt",
            "flip0.1flip0.30.txt",
            ##
            'unif0.1unif0.10.txt',
            'unif0.1unif0.30.txt',
            ##
            ]

colors = ['red', 'black', 'magenta', 'blue', 'green', 'cyan', 'pink']

results = []
for i in range(len(filename)):
    list_read = []
    f = open(filename[i], 'r')
    a = f.readline(10)\

    while (len(a) != 0):
        a = f.readline()
        if a[0:5] == "EPOCH":
            if a[-6] == "Y":
                list_read.append(float(a[-5:-1]))
            else:
                list_read.append(float(a[-6:-1]))
    f.close()
    plt.title(titles[i])
    x = [i for i in range(1,121)]
    plt.plot(x, list_read)
    plt.grid()
    plt.savefig(titles[i]+".png")
    plt.cla()

    results.append(list_read)


# entire plot
x = [i for i in range(1,121)]
for i in range(len(filename)):
    plt.title("compare test accuracy")
    plt.plot(x, results[i], alpha=0.5, label=titles[i], color=colors[i])
plt.legend()
plt.grid()
plt.savefig("entire.png")