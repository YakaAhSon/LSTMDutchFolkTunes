tune_strings = [open("DutchFolkTunes/allnlb%d000.abc"%i,"r").read() for i in range(1,20)]
tune_strings = [i.split("\n\n") for i in tune_strings]

tunes = []
for i in tune_strings:
    tunes = tunes+i

tune_strings = tunes
tune_strings = filter(lambda x: len(x)>20, tune_strings)
del tunes