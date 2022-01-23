import sqlite3


def troichka(id_1, id_2, pr_splav='Амереканская версия', har_spla=()):
    con = sqlite3.connect("Spider-man_cards_stats.sqlite")
    cur = con.cursor()
    if id_1 == 142:
        if pr_splav == 'Амереканская версия':
            haract_1 = (1, 140, 125)
            haract_2 = cur.execute(f"""SELECT danger_stars, speed_and_agility, power from cadrs_hero_villain
            WHERE id = {id_2}""").fetchall()[0]
    elif id_2 == 142:
        if pr_splav == 'Амереканская версия':
            haract_1 = cur.execute(f"""SELECT danger_stars, speed_and_agility, power from cadrs_hero_villain
            WHERE id = {id_1}""").fetchall()[0]
            haract_2 = (1, 140, 125)
    else:
        haract_1 = cur.execute(f"""SELECT danger_stars, speed_and_agility, power from cadrs_hero_villain
        WHERE id = {id_1}""").fetchall()[0]
        haract_2 = cur.execute(f"""SELECT danger_stars, speed_and_agility, power from cadrs_hero_villain
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