def print_on_same_line(msg: str, max_len: int) -> int:
    msg_len = len(msg)
    print('\r' + msg, end='')

    if msg_len < max_len:
        print(' ' * (max_len-msg_len), end='')
    elif msg_len > max_len:
        max_len = msg_len

    return max_len


def ask_yes_or_no(msg: str) -> bool:
    while True:
        resp = input(f'{msg} [y/n] ').upper()

        if resp in ['Y', 'YES']:
            return True

        elif resp in ['N', 'NO']:
            return False
