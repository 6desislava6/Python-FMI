CATEGORIES = {(-10 ** 20, 15): 'тежко недохранване',
              (15, 16): 'средно недохранване',
              (16, 18.5): 'леко недохранване',
              (18.5, 25): 'нормално тегло',
              (25, 30): 'наднормено тегло',
              (30, 35): 'затлъстяване I степен',
              (35, 40): 'затлъстяване II степен',
              (40, 10 ** 20): 'затлъстяване III степен'}


def body_mass_index(weight, height):
    return weight / height ** 2


def checkRange(bmi):
    for bmis, status in CATEGORIES.items():
        if bmis[0] < bmi and bmi <= bmis[1]:
            return status


def shape_of(weight, height):
    return checkRange(body_mass_index(weight, height))

