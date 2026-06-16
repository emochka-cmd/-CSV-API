import parser
import create_schedule
import request

from datetime import datetime


def main():
    doctors = parser.parse_doctors(
        "/home/user/PycharmProjects/ArchimedParser/data/archimed_doctors.sql.csv")
    schedule = parser.parse_doctors_schedule(
        "/home/user/PycharmProjects/ArchimedParser/data/archimed_doctorsshedule.sql.csv")
    talon = parser.parse_talons(
        "/home/user/PycharmProjects/ArchimedParser/data/archimed_talons.sql.csv")

    data_to_send = {
        "schedule": {
            "1": "1",
            "data": {
                "1": {}
            }
        }
    }

    start_program_time = datetime.now()

    filial_shedule = create_schedule.create_schedule(doctors, schedule, talon)
    data_to_send["schedule"]["data"]["1"] = filial_shedule

    end_program_time = datetime.now() - start_program_time
    print(end_program_time)

    request.make_request(
       url="https://api.prodoctorov.ru/v2/doctors/send_schedule/",
       data=data_to_send)


if __name__ == '__main__':
    main()
