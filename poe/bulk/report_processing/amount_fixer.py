def fix_amount(amount):
    if amount in 'sz':
        return 2
    elif amount in 't':
        return 1
    return amount