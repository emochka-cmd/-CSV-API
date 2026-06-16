import csv

from typing import Dict

DEFAULT_TIMESCALE = 30


def parse_doctors(path: str, filtration='ID') -> Dict:
    """need file path and key for parse doctor table. doctor id is not repeated."""
    doctors = {}

    with open(path, encoding='utf-8', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)

        for row in reader:
            active = row.pop('ENABLED')
            if active == 0:
                continue

            if row['TIMESCALE'] == 0 and row['MAX_GET_TIME'] == 0:
                row['TIMESCALE'] = DEFAULT_TIMESCALE
            else:
                row['TIMESCALE'] = row['MAX_GET_TIME']

            row.pop('MAX_GET_TIME')

            key = row.pop(filtration)
            doctors.setdefault(key, row)

    return doctors


def parse_doctors_schedule(path: str, filtration='DOCID') -> Dict:
    """for parse doctors schedule, need path and key"""
    doctors_schedule = {}

    with open(path, encoding='utf-8', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)

        for row in reader:
            hide = row.pop('HIDEINTALONS')
            if hide == 1:
                continue

            key = row.pop(filtration)

            doctors_schedule.setdefault(key, [])
            doctors_schedule[key].append(row)

    return doctors_schedule


def parse_talons(path: str, filtration='DOCID') -> Dict:
    """for parse talons, need path and key"""
    talon = {}

    with open(path, encoding='utf-8', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        next(reader)

        for row in reader:
            active = row.pop('ENABLED')
            if active == 0:
                continue

            key = row.pop(filtration)
            date = row.pop("SHIFTDATE")

            talon.setdefault(key, {})
            talon[key].setdefault(date, [])
            talon[key][date].append(row)

    return talon


if __name__ == '__main__':
    doctors = parse_doctors("/home/user/PycharmProjects/ArchimedParser/data/archimed_doctors.sql.csv")
    print(doctors)
    schedule = parse_doctors_schedule("/home/user/PycharmProjects/ArchimedParser/data/archimed_doctorsshedule.sql.csv")
    print(schedule)
    talons = parse_talons("/home/user/PycharmProjects/ArchimedParser/data/archimed_talons.sql.csv")
    print(talons)