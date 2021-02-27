def cost2cart(cost):
    if cost != 0:
        return f'  {cost}р'
    else:
        return ''


def cart2cost(cart):
    return int(cart[:-1].lstrip())
