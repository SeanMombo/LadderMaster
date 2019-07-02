

class player:
    def __init__(self):
        self.winloss = {}


def confirm(player, beat, score):
    p = player
    p2 = beat

    if len(score) == 3 and score[1] == '-' and isinstance(int(score[0]), int) and isinstance(int(score[2]), int):
        print(score[0])
        print(score[2])

    windata = p.winloss



if __name__ == "__main__":
    p = player()

    lis = []

    confirm(p, 0, 'a-1')
    # lis.append([3,0])
    # lis.append([3,0])
    # lis.append([3,2])
    # lis.append([1,3])
    # lis.append([2,3])
    # lis.append([0,3])
    # lis.append([0,3])
    # lis.append([3,1])

    windata = p.winloss

    #for data in windata:
    windata.update({'wizzrobe':[]})
    windata.update({'jizzrod':[]})
    data = p.winloss['wizzrobe']

    data.append([3,0])
    data.append([3,0])
    data.append([3,2])
    data.append([1,3])
    data.append([2,3])
    data.append([0,3])
    data.append([0,3])
    data.append([3,1])
    
