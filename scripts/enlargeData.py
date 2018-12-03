from scripts import preProcessing

working_dir = preProcessing.get_working_dir()

with open(working_dir + "profile_semantic_trafo_final.txt", "r") as f:
    data = f.read()

for i in range(10):
    print(i)
    dat = data.split("\n")[3:]
    newdata = []
    for i in range(1, len(dat), 2):
        newtime = int(dat[i].split(" ")[0]) + 1
        newline = str(newtime) + " " + " ".join(dat[i].split(" ")[1:])
        newdata.append("")
        newdata.append(newline)


    old = data.split("\n")
    for i in newdata:
        old.append(i)

    data = "\n".join(old)

with open(working_dir + "large.txt", "w") as f:
    f.write(data)