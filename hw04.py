from typing import Callable, Dict


def input_error(func: Callable) -> Callable:
    def inner(*args: list, **kwargs: dict):
        try:
            return func(*args, **kwargs)
        except Exception:
            return 'Something went wrong.'

    def add_contact_error(args: list[str], contacts: dict) -> str:
        try:
            return func(args, contacts)
        except ValueError:
            return 'Give me a new name and a new phone, please.'

    def change_contact_error(args: list[str], contacts: dict) -> str:
        try:
            return func(args, contacts)
        except KeyError:
            return 'Give me an added name, please.'
        except ValueError:
            return 'Give me an added name and a new phone, please.'

    def show_phone_error(args: list[str], contacts: dict) -> str:
        try:
            return func(args, contacts)
        except (KeyError, IndexError):
            return 'Give me an added name, please.'

    def show_all_error(contacts: dict) -> str:
        try:
            return func(contacts)
        except ValueError:
            return 'Contacts list is empty.'

    HANDLERS: Dict[str, Callable] = {
        'add_contact': add_contact_error,
        'change_contact': change_contact_error,
        'show_phone': show_phone_error,
        'show_all': show_all_error
    }

    return HANDLERS.get(func.__name__, inner)


@input_error
def parse_input(user_input: str) -> tuple[str]:
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


@input_error
def add_contact(args: list[str], contacts: dict) -> str:
    name, phone = args

    if contacts.get(name) is not None:
        return 'Contact is already added!'

    contacts[name] = phone

    return 'Contact added.'


@input_error
def change_contact(args: list[str], contacts: dict) -> str:
    name, phone = args

    # Try to remove a contact to ensure that it has existed.
    del contacts[name]

    contacts[name] = phone

    return 'Contact updated.'


@input_error
def show_phone(args: list[str], contacts: dict) -> str:
    return contacts[args[0]]


@input_error
def show_all(contacts: dict) -> str:
    def divider(left: str, right: str, middle: str, cell: str = '═'):
        return left + cell * (longest_name + 2) + middle + cell * \
            (longest_phone + 2) + right

    def row() -> str:
        right = ' ' * (longest_name - len(name) + 1)
        left = ' ' * (longest_phone - len(phone) + 1)
        return f'║ {name}{right}│{left}{phone} ║'

    name, phone = 'Full name', 'Phone number'
    longest_name = max([len(name) for name in contacts.keys()])
    longest_phone = max([len(phone) for phone in contacts.values()])

    if longest_name < len(name):
        longest_name = len(name)

    if longest_phone < len(phone):
        longest_phone = len(phone)

    rows = [divider('╔', '╗', '╤'), row(), divider('╟', '╢', '┼', '─')]

    for name, phone in contacts.items():
        rows.append(row())

    rows.append(divider('╚', '╝', '╧'))

    return '\n'.join(rows)


def main() -> None:
    contacts: Dict[str, str] = {}

    print('Welcome to the assistant bot!')

    while True:
        command, *args = parse_input(input('Enter a command: '))

        match command:
            case 'hello': print('How can I help you?')
            case 'add': print(add_contact(args, contacts))
            case 'change': print(change_contact(args, contacts))
            case 'phone': print(show_phone(args, contacts))
            case 'all': print(show_all(contacts))
            case _ if command in ['close', 'exit']:
                print('Good bye!')
                break
            case _: print('Invalid command.')


if __name__ == '__main__':
    main()
