import os


if __name__ == "__main__":
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    classes = os.listdir(parent)
    for class_ in classes:
        if class_ != "MoveFiles.py":
            simulations = os.listdir(parent + "/" + class_)
            for i, simulation in enumerate(simulations):
                files = os.listdir(parent + "/" + class_ + "/" + simulation)
                files.sort(reverse=True)
                file_to_move = files[0]
                with open(parent + "/" + class_ + "/" + simulation + "/" + file_to_move, 'r') as f:
                    lines = f.readlines()
                f. close()

                with open(parent + "/../../DataBackup/ripser_backup/ImageBoundaries/" + class_ + "-" + str(i) + ".txt", 'w') as f:
                    for line in lines:
                        write_line = line.strip('\n')
                        print(write_line, file=f)
                f.close()

else:
    exit(-1)
