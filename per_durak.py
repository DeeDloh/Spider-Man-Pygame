import sqlite3

CHISL_HARACT = {1: 'intellect',
                2: 'power',
                3: 'speed_and_agility',
                4: 'special_skills',
                5: 'fighting_skills'}


def per_durak(card_beat, card_defend, haracterist, pr_splav='Амереканская версия'):
    """card_beat and card_defend -> list | len == 1 or 2. Хранятся id карт.
    haracterist -> int
    1 - intellect, 2 - power, 3 - speed and agility, 4 - special skills, 5 - fighting skills"""

    con = sqlite3.connect("Spider-man_cards_stats.sqlite")
    cur = con.cursor()
    if len(card_beat) == 1:
        if card_beat[0] == 71:
            if pr_splav == 'Амереканская версия':
                haract_beat = (132, 125, 140, 351, 110)[haracterist]
                haract_defend = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
                WHERE id = {card_defend[0]}""").fetchall()[0][0]
        elif card_defend[0] == 71:
            if pr_splav == 'Амереканская версия':
                haract_beat = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
                WHERE id = {card_beat[0]}""").fetchall()[0][0]
                haract_defend = (132, 125, 140, 351, 110)[haracterist]
        else:
            haract_beat = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
            WHERE id = {card_beat[0]}""").fetchall()[0][0]
            haract_defend = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
            WHERE id = {card_defend[0]}""").fetchall()[0][0]
        if haract_beat > haract_defend:
            return card_beat
        elif haract_beat < haract_defend:
            return card_defend
        else:
            return [card_beat[0], card_defend[0]]
    else:
        if card_beat[0] == 71:
            if pr_splav == 'Амереканская версия':
                haract_beat_1 = (132, 125, 140, 351, 110)[haracterist]
                haract_beat_2 = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
                WHERE id = {card_beat[1]}""").fetchall()[0][0]
        elif card_beat[1] == 71:
            if pr_splav == 'Амереканская версия':
                haract_beat_1 = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
                WHERE id = {card_beat[0]}""").fetchall()[0][0]
                haract_beat_2 = (132, 125, 140, 351, 110)[haracterist]
        else:
            haract_beat_1 = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
            WHERE id = {card_beat[0]}""").fetchall()[0][0]
            haract_beat_2 = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
            WHERE id = {card_beat[1]}""").fetchall()[0][0]

        if card_defend[0] == 71:
            if pr_splav == 'Амереканская версия':
                haract_defend_1 = (132, 125, 140, 351, 110)[haracterist]
                haract_defend_2 = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
                WHERE id = {card_defend[1]}""").fetchall()[0][0]
        elif card_defend[1] == 71:
            if pr_splav == 'Амереканская версия':
                haract_defend_1 = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
                WHERE id = {card_defend[0]}""").fetchall()[0][0]
                haract_defend_2 = (132, 125, 140, 351, 110)[haracterist]
        else:
            haract_defend_1 = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
            WHERE id = {card_defend[0]}""").fetchall()[0][0]
            haract_defend_2 = cur.execute(f"""SELECT {CHISL_HARACT[haracterist]} from cadrs_hero_villain
            WHERE id = {card_defend[1]}""").fetchall()[0][0]
        min_haract_beat = min(haract_beat_1, haract_beat_2)
        vivod = any([min_haract_beat >= haract_defend_1, min_haract_beat >= haract_defend_2])
        if vivod:
            return card_beat
        else:
            return card_defend