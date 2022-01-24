import sqlite3

PEREVOD_HAR = {'intellect': 0,
               'power': 1,
               'speed_and_agility': 2,
               'special_skills': 3,
               'fighting_skills': 4,
               }


def troichka_plus(id_1, id_2, r_har, pr_splav='Амереканская версия', har_spla=(132, 125, 140, 351, 110)):
    con = sqlite3.connect("data/databases/Spider-man_cards_stats.sqlite")
    cur = con.cursor()
    if id_1 == 142:
        if pr_splav == 'Амереканская версия':
            haract_1 = (1, har_spla[PEREVOD_HAR[r_har[0]]], har_spla[PEREVOD_HAR[r_har[1]]])
            haract_2 = cur.execute(f"""SELECT danger_stars, {r_har[0]}, {r_har[1]} from cadrs_hero_villain
            WHERE id = {id_2}""").fetchall()[0]
    elif id_2 == 142:
        if pr_splav == 'Амереканская версия':
            haract_1 = cur.execute(f"""SELECT danger_stars, {r_har[0]}, {r_har[1]} from cadrs_hero_villain
            WHERE id = {id_1}""").fetchall()[0]
            haract_2 = (1, har_spla[PEREVOD_HAR[r_har[0]]], har_spla[PEREVOD_HAR[r_har[1]]])
    else:
        haract_1 = cur.execute(f"""SELECT danger_stars, {r_har[0]}, {r_har[1]} from cadrs_hero_villain
        WHERE id = {id_1}""").fetchall()[0]
        haract_2 = cur.execute(f"""SELECT danger_stars, {r_har[0]}, {r_har[1]} from cadrs_hero_villain
        WHERE id = {id_2}""").fetchall()[0]
    scores_1 = sum([1 if haract_1[0] > haract_2[0] else 0,
                    1 if haract_1[1] > haract_2[1] else 0,
                    1 if haract_1[2] > haract_2[2] else 0])
    scores_2 = sum([1 if haract_1[0] < haract_2[0] else 0,
                    1 if haract_1[1] < haract_2[1] else 0,
                    1 if haract_1[2] < haract_2[2] else 0])
    '''Возвращает id проигравшего'''

    if scores_1 > scores_2:
        return id_2
    elif scores_1 < scores_2:
        return id_1
    else:
        return None