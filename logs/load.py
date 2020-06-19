import matplotlib.pyplot as plt

titles = ['Meta-clean Train-flip0.1',
        "Meta-clean Train-flip0.3",
        "Meta-clean Train-flip0.6",

        "Meta-clean Train-unif0.1",
        "Meta-clean Train-unif0.3",
        "Meta-clean Train-unif0.6",

#        "Basic flip0.1",
#        "Basic flip0.3",
#        "Basic flip0.6",
#        "Basic unif0.1",
#        "Basic unif0.3",

        "Meta-flip0.1 Train-flip0.1",
        "Meta-flip0.1 Train-flip0.3",
        "Meta-flip0.1 Train-flip0.6",
        
        "Meta-flip0.3 Train-flip0.3",
        "Meta-flip0.3 Train-flip0.6",
        "Meta-flip0.6 Train-flip0.6",

        "Meta-unif0.1 Train-unit0.1",
        "Meta-unif0.1 Train-unit0.3",
        "Meta-unif0.1 Train-unif0.6",
        
        "Meta-unif0.3 Train-unif0.3",
        "Meta-unif0.3 Train-unif0.6",
        "Meta-unif0.6 Train-unif0.6",
        ]
filename = ['clean0.0flip0.10.txt',
            'clean0.0flip0.30.txt',
            'clean0.0flip0.60.txt',

            'clean0.0unif0.10.txt',
            'clean0.0unif0.30.txt',
            'clean0.0unif0.60.txt',

#            'Falseclean0.0flip0.10.txt',
#            'Falseclean0.0flip0.30.txt',
#            'Falseclean0.0flip0.60.txt',

#            'Falseclean0.0unif0.10.txt',
#            'Falseclean0.0unif0.30.txt',

            "flip0.1flip0.10.txt",
            "flip0.1flip0.30.txt",
            "flip0.1flip0.60.txt",

            "flip0.3flip0.30.txt",
            "flip0.3flip0.60.txt",
            "flip0.6flip0.60.txt",

            'unif0.1unif0.10.txt',
            'unif0.1unif0.30.txt',
            'unif0.1unif0.60.txt',

            'unif0.3unif0.30.txt',
            'unif0.3unif0.60.txt',
            'unif0.6unif0.60.txt',
            ]

#colors = ['red', 'black', 'magenta', 'blue', 'green', 'cyan', 'pink']

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
    x = [i for i in range(1,len(list_read)+1)]
    plt.plot(x, list_read)
    plt.grid()
    plt.savefig(titles[i]+".png")
    plt.cla()

    results.append(list_read)


# entire plot
plt.title("compare test accuracy")
plt.figure(figsize=(15,10))
for i in range(len(filename)):
    x = [k for k in range(1,len(results[i])+1)]
    plt.plot(x, results[i], alpha=0.8, label=titles[i]) #, color=colors[i])
plt.legend()
plt.grid()
plt.savefig("entire.png")