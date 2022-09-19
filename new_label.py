from shutil import copyfile


def get_speed_new_label(label,new_label,speed):
    file = open(label, 'r', encoding='utf-8')
    new_file = open(new_label, 'w', encoding='utf-8')

    for i in range(1, 4):
        data = file.readline()
        new_file.write(data)

    for i in range(4, 6):
        data = float(file.readline().replace('\n', ''))
        data = str(round(data / speed, 2)) + '\n'
        new_file.write(data)
        # data = file.readline()
        #print(data)

    for i in range(6, 10):
        data = file.readline()
        new_file.write(data)

    for i in range(10, 12):
        data = float(file.readline().replace('\n', ''))
        data = str(round(data / speed, 2)) + '\n'
        new_file.write(data)
        # data = file.readline()
        #print(data)

    data = file.readline()
    new_file.write(data)

    for i in range(13, 15):
        data = float(file.readline().replace('\n', ''))
        data = str(round(data / speed, 2)) + '\n'
        new_file.write(data)
        # data = file.readline()
        #print(data)

    for i in range(15, 18):
        data = file.readline()
        new_file.write(data)

    for i in range(18, 20):
        data = float(file.readline().replace('\n', ''))
        data = str(round(data / speed, 2)) + '\n'
        new_file.write(data)
        # data = file.readline()
        #print(data)

    data = file.readline().replace('\n', '')
    num = int(data)
    new_file.write(data + '\n')

    for i in range(0, num):
        for j in range(0, 2):
            data = float(file.readline().replace('\n', ''))
            data = str(round(data / speed, 2)) + '\n'
            new_file.write(data)
            # data = file.readline()
            #print(data)
        data = file.readline()
        new_file.write(data)

    for i in range(0, 2):
        data = file.readline()
        new_file.write(data)

    for i in range(0, 2):
        data = float(file.readline().replace('\n', ''))
        data = str(round(data / speed, 2)) + '\n'
        new_file.write(data)
        # data = file.readline()
        #print(data)

    data = file.readline().replace('\n', '')
    num = int(data)
    new_file.write(data + '\n')

    for i in range(0, num):
        for j in range(0, 2):
            data = float(file.readline().replace('\n', ''))
            data = str(round(data / speed, 2)) + '\n'
            new_file.write(data)
            # data = file.readline()
            #print(data)
        data = file.readline()
        new_file.write(data)

def get_new_label(label,new_label):
    copyfile(label,new_label)