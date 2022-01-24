import sqlite3

PEREVOD_HAR = {0: 'intellect',
               1: 'power',
               2: 'speed_and_agility',
               3: 'special_skills',
               4: 'fighting_skills',
               }


def domination(cards, haract, pr_splav='Амереканская версия',
               har_splav=(132, 125, 140, 351, 110)):
    '''cards -> list| [(id_cards, player_n)]'''
    haract_1 = []
    id = [i[0] for i in cards]
    con = sqlite3.connect("data/databases/Spider-man_cards_stats.sqlite")
    cur = con.cursor()
    for i in id:
        if i == 142:
            if pr_splav == 'Амереканская версия':
                haract_1.append(har_splav[haract[0]])
        else:
            haract_card = cur.execute(f"""SELECT {PEREVOD_HAR[haract[0]]}, {PEREVOD_HAR[haract[1]]}
from cadrs_hero_villain WHERE id = {i}""").fetchall()[0]
            haract_1.append(haract_card[0])
    maxx = -1
    ind = [-1]
    for i in range(3):
        if maxx < haract_1[i]:
            maxx = haract_1[i]
            ind[0] = i
        elif maxx == haract_1[i]:
            ind = [ind[0], i]
    if len(ind) == 2:
        return None
    else:
        return cards[ind[0]][1]