from datetime import datetime, timedelta


MINUTE_IN_HOUR = 60
SECOND_IN_HOUR = 60
HOUR_IN_DAY = 24
MIN_ROUNDING = 5
FLOAT_ROUNDING = 7


def create_year(values) -> str:
    base_date = datetime(year=1899, month=12, day=30)

    days_delta = timedelta(days=int(values))
    year_in_shedule = base_date + days_delta

    return year_in_shedule.strftime("%Y-%m-%d")


def create_time_in_string(values: float) -> str:
    """values - part of day"""
    seconds = int(values * HOUR_IN_DAY * MINUTE_IN_HOUR * SECOND_IN_HOUR)

    days_delta = timedelta(seconds=seconds)

    time_in_shedule = datetime.min + days_delta

    if time_in_shedule.second > MIN_ROUNDING:
        time_in_shedule += timedelta(minutes=1) - timedelta(seconds=time_in_shedule.second)

    hour = time_in_shedule.hour
    minute = time_in_shedule.minute

    return f"{hour:02}:{minute:02}"


def works_fragments(work_start: float,
                    work_end: float,
                    duration: int,
                    start_break=None,
                    end_break=None) -> [[float]]:
    """to split the schedule
    work_start, work_end - part of day
    duration - minutes
    """
    slots = []

    if duration < 1:
        return slots

    duration_in_part_day = duration / MINUTE_IN_HOUR / HOUR_IN_DAY

    work_interval = []
    if start_break and end_break:
        if work_start > start_break and end_break < work_end:
            work_interval.append([work_start, start_break])
            work_interval.append([end_break, work_end])
    else:
        work_interval.append([work_start, work_end])

    for work_interval_start, work_interval_end in work_interval:

        iteration = 0
        max_iteration = 1000

        while work_interval_start <= work_interval_end and iteration < max_iteration:
            current_work_interval_end = work_interval_start + duration_in_part_day

            slots.append([
                round(work_interval_start, FLOAT_ROUNDING),
                round(current_work_interval_end, FLOAT_ROUNDING)
            ])

            work_interval_start = current_work_interval_end
            iteration += 1

    return slots


def is_busy(slot_start, slot_end, talons) -> bool:
    slot_start = float(slot_start)
    slot_end = float(slot_end)

    for talon in talons:
        talon_start = round(float(talon['BEGINTIME']), FLOAT_ROUNDING)
        talon_end = round(float(talon['ENDTIME']), FLOAT_ROUNDING)

        if slot_start < talon_end and slot_end > talon_start:
            return True

    return False


def create_doctor_cells(doctor, doctor_schedule, talon):
    """helper function for creating cells"""
    doctor_cells = list()

    slot_duration = doctor.get('TIMESCALE', 30)

    for current_schedule in doctor_schedule:
        current_date = current_schedule["SHIFTDATE"]
        current_talons = talon.get(current_date)

        slots = works_fragments(
            work_start=float(current_schedule['BEGINTIME']),
            work_end=float(current_schedule['ENDTIME']),
            duration=int(slot_duration),
            start_break=current_schedule['BEGINTIME_P'],
            end_break=current_schedule['ENDTIME_P']
        )

        for slot in slots:
            slot_busy = False

            slot_start = slot[0]
            slot_end = slot[1]

            if current_talons:
                slot_busy = is_busy(slot_start, slot_end, current_talons)

            cell_data = {
                'dt': create_year(current_date),
                'time_start': create_time_in_string(slot[0]),
                'time_end': create_time_in_string(slot[1]),
                'free': not slot_busy
            }

            doctor_cells.append(cell_data)

    return doctor_cells


def create_schedule(doctors, schedule, talon):
    """creating a schedule request"""
    filial_doctors = {}

    for doctor_id, doctor_info in doctors.items():
        if doctor_id in schedule:
            doctor_cells = create_doctor_cells(doctor_info, schedule[doctor_id], talon[doctor_id])

            if not doctor_cells:
                continue

            current_doctor = {
                'efio': doctor_info["FULLNAME"],
                'cells': doctor_cells
            }

            filial_doctors[doctor_id] = current_doctor

    return filial_doctors