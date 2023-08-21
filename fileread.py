def fileRead(file):
    with open(file) as f:
        lines = f.readlines()

        for index, line in enumerate(lines):
            if index == 0:
                continue

            infos = [int(info) for info in line.split()]

            