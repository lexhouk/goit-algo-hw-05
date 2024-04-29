from collections import Counter
from sys import argv
from re import search


def parse_log_line(line: str) -> dict:
    '''
    Validate and split a log row into separate cells.

    :param line: str

    :return: dict
    '''

    # E.g. 2024-01-22 12:00:00 INFO User logged out.
    PATTERN = (r'^(?P<date>\d{4}-\d{2}-\d{2})\s+'
               r'(?P<time>\d{2}:\d{2}:\d{2})\s+'
               r'(?P<level>[A-Z]+)\s+'
               r'(?P<message>[A-Z]{1}.+\.)$')

    columns = search(PATTERN, line.strip())

    return columns.groupdict() if columns else {}


def load_logs(file_path: str) -> list[dict]:
    '''
    Read a file and convert its data into a table.

    :param file_path: str

    :return: list[dict]
    '''

    logs = []

    try:
        with open(file_path, encoding='utf-8') as file:
            for line in file.readlines():
                log = parse_log_line(line)

                if log:
                    logs.append(log)

    except FileNotFoundError:
        print(f'Файл {file_path} не знайдено!')

    except Exception as e:
        print('Сталася наступна помилка:', e)

    return logs


def filter_logs_by_level(logs: list[dict], level: str) -> list[dict]:
    '''
    Choose rows of a specified level.

    :param logs: list[dict]
    :param level: str

    :return: list[dict]
    '''

    return list(filter(lambda log: log['level'] == level, logs))


def count_logs_by_level(logs: list[dict]) -> dict:
    '''
    Calculate the number of records from each level.

    :param logs: list[dict]

    :return: dict
    '''

    items = {}

    for item in Counter([log['level'] for log in logs]).most_common():
        items[item[0]] = item[1]

    return items


def display_log_counts(counts: dict) -> None:
    '''
    Show data in the table view provided by the previous function.

    :param counts: dict

    :return: None
    '''

    if counts:
        print('Рівень логування | Кількість\n-----------------|----------')

        for level, count in counts.items():
            print(f'{level:<17}| {count}')


def main() -> None:
    # Display common statistics.
    if len(argv) > 1:
        logs = load_logs(argv[1])
        display_log_counts(count_logs_by_level(logs))

        # Display statistics for a selected level.
        if len(argv) > 2:
            level = argv[2].upper()
            logs = filter_logs_by_level(logs, level)
            suffix = ':' if logs else ' відсутні!'

            print(f"\nДеталі логів для рівня '{level}'{suffix}")

            if logs:
                for log in logs:
                    print(log['date'], log['time'], '-', log['message'])
    else:
        print(('Скрипт має бути запущений хоча б з одним аргументом - шляхом '
               'до файлів з логами!'))


if __name__ == '__main__':
    main()
