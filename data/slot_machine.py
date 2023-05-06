import random

values = [':bell:', ':seven:', ':cherries:', ':lemon:', ':watermelon:']

def make_spin(monies):
    a = []
    for i in range(3):
        a.append(random.choice(values))
    d = {}
    mx = 0
    for val in a:
        try:
            d[val] += 1
            mx = max(mx, d[val])
        except KeyError:
            d[val] = 1
            mx = max(mx, d[val])
    if mx == 1:
        if ':cherries:' in a:
            return ' '.join(a), 'Ну, у Вас есть вишенка :cherries:', monies
        return ' '.join(a), 'Вы ничего не выиграли', 0
    elif mx == 2:
        return ' '.join(a), 'Ух ты, дубль! :coin::coin:', monies * 2
    elif mx == 3:
        if ':seven:' in a:
            return ' '.join(a), ':moneybag:ДЖЕКПОТ!!!:moneybag:', monies * 10
        return ' '.join(a), 'Три одинаковых! :coin::coin::coin:', monies * 5
