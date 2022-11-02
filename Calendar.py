from datetime import datetime
import random


class Worker:
    def __init__(self, name, quality, department, work_time, busy_time):
        self.name = name
        self.quality = quality
        self.department = department
        self.busy_time = []
        work_time = work_time.split('-')
        try:
            work_time_start = datetime.strptime(work_time[0], "%H:%M")
        except:
            work_time_start = datetime.strptime("09:00", "%H:%M")

        try:
            work_time_end = datetime.strptime(work_time[1], "%H:%M")
        except:
            work_time_end = datetime.strptime("18:00", "%H:%M")

        if work_time_end<= work_time_start:
            print("Incorrect working time")
        self.work_time = [work_time_start, work_time_end]
        self.free_time = [self.work_time.copy()]
        self.__add_busy_time(busy_time)

    def busy_time_get(self):
        return self.busy_time

    def free_time_get(self):
        return self.free_time

    def work_time_get(self):
        return self.work_time

    def busy_time_set(self, busy_time):
        self.__add_busy_time(busy_time)

    def __add_busy_time(self, busy_time):
        busy_time = busy_time.split(' ')
        for time in busy_time:
            time = time.split('-')
            try:
                begin_time = datetime.strptime(time[0], "%H:%M")
            except:
                continue

            if begin_time < self.work_time[0]:
                begin_time = self.work_time[0]

            try:
                end_time = datetime.strptime(time[1], "%H:%M")
            except:
                continue

            if end_time > self.work_time[1]:
                end_time = self.work_time[1]
            if end_time <= begin_time:
                continue
            flag = True
            for j in range(len(self.busy_time)):
                if (self.busy_time[j][0] <= begin_time < self.busy_time[j][1]) or (
                        self.busy_time[j][0] < end_time <= self.busy_time[j][1]) or (
                        begin_time <= self.busy_time[j][0] and end_time >= self.busy_time[j][1]):
                    flag = False
                    break
                if begin_time < self.busy_time[j][0] and end_time <= self.busy_time[j][0]:
                    flag = False
                    if j != 0:
                        self.busy_time = self.busy_time[:j - 1] + [[begin_time, end_time]] + self.busy_time[j:]
                    else:
                        self.busy_time = [[begin_time, end_time]] + self.busy_time[j:]
                    break
            if flag:
                self.busy_time.append([begin_time, end_time])

        self.__recount_free_time()

    def __recount_free_time(self):
        begin_free_time = self.free_time[0][0]
        end_free_time = self.free_time[-1][1]
        free_time = []
        for time in self.busy_time:
            first_end = time[0]
            if begin_free_time < first_end:
                free_time.append([begin_free_time, first_end])
            begin_free_time = time[1]
        if begin_free_time < end_free_time:
            free_time.append([begin_free_time, end_free_time])
        if len(free_time) != 0:
            self.free_time = free_time.copy()



class Calendar:
    def __init__(self):
        self.workers = dict()

    def add_new_worker(self, name, quality, department, work_time="09:00-18:00", busy_time="00:00-00:00"):
        worker = Worker(name, quality, department, work_time=work_time, busy_time=busy_time)
        self.workers[name + quality + department] = worker

    def get_work_time(self, name, quality, department):
        try:
            work_time = self.workers[name + quality + department].work_time_get()
            return [work_time[0].strftime("%H:%M"), work_time[1].strftime("%H:%M")]
        except KeyError:
            print("Такого сотрудника нет в базе данных")
            return None

    def get_free_time(self, name, quality, department):
        try:
            free_time = self.workers[name + quality + department].free_time_get()
            return [[time[0].strftime("%H:%M"), time[1].strftime("%H:%M")] for time in free_time]
        except KeyError:
            print("Такого сотрудника нет в базе данных")
            return None

    def set_meeting(self, name, quality, department, time):
        try:
            self.workers[name + quality + department].busy_time_set(time)
        except KeyError:
            print("Такого сотрудника нет в базе данных")

    def get_common_free_time(self, workers):
        if len(workers) == 0:
            return None
        all_free_time = []
        for ind, worker in enumerate(workers):
            free_time = self.workers[''.join(worker)].free_time_get()
            if ind == 0:
                all_free_time = free_time.copy()
                continue
            free_all_time = []
            for time_worker in free_time:
                begin_time = None
                end_time = None
                for all_time in all_free_time:

                    if all_time[0] <= time_worker[0] <= all_time[1]:
                        begin_time = time_worker[0]
                    elif time_worker[0] <= all_time[0] <= time_worker[1]:
                        begin_time = all_time[0]

                    if all_time[0] <= time_worker[1] <= all_time[1]:
                        end_time = time_worker[1]
                        if [begin_time, end_time] not in free_all_time:
                            free_all_time.append([begin_time, end_time])
                        break
                    elif time_worker[0] <= all_time[1] <= time_worker[1]:
                        end_time = all_time[1]
                        if [begin_time, end_time] not in free_all_time:
                            free_all_time.append([begin_time, end_time])
                        begin_time = None
                        end_time = None
            all_free_time = free_all_time.copy()
        return [[time[0].strftime("%H:%M"), time[1].strftime("%H:%M")] for time in all_free_time]


# Тест для сотрудников(передавать num)
def generate_names_dates(num = 100, n_meeting = 10):
    calendar = Calendar()
    name = 'Alex'
    quality = 'programer'
    department = 'it'
    names = []
    for i in range(num):
        new_name = name+str(i)
        names.append([new_name, quality, department])
        hour_begin = random.randint(0, 22)
        hour_begin += 1
        hour_end = random.randint(hour_begin, 23)
        minute_begin = random.randint(0, 58)
        minute_end = random.randint(0, 59)
        if hour_begin == hour_end:
            minute_end = random.randint(minute_begin+1, 59)

        calendar.add_new_worker(new_name, quality, department, work_time=f"{hour_begin}:{minute_begin}-{hour_end}:{minute_end}")
        meeting_amm = random.randint(1, n_meeting)
        for j in range(meeting_amm):
            if hour_begin == hour_end-1:
                meeting_hour_begin = hour_begin
                meeting_hour_end = hour_begin
                meeting_minute_begin = random.randint(0, 58)
                meeting_minute_end = random.randint(meeting_minute_begin+1, 59)
            else:
                meeting_hour_begin = random.randint(hour_begin, hour_end)
                meeting_hour_end = random.randint(meeting_hour_begin, hour_end)
                meeting_minute_begin = random.randint(0, 59)
                meeting_minute_end = random.randint(0, 59)

            calendar.set_meeting(new_name, quality, department, f"{meeting_hour_begin}:{meeting_minute_begin}-{meeting_hour_end}:{meeting_minute_end}")

    for name in names:
        print('Work time for ', ' '.join(name), calendar.get_work_time(name[0], name[1], name[2]))
        print('Free time for ', ' '.join(name), calendar.get_free_time(name[0], name[1], name[2]))

    part_of_names = random.randint(1, num)
    part_workers = random.sample(names, part_of_names)
    print('Random workers are: ', part_workers)
    print('All free time: ', calendar.get_common_free_time(part_workers))

if __name__ == '__main__':
    calendar = Calendar()
    calendar.add_new_worker("ivan", "programer", "it")
    calendar.set_meeting("ivan", "programer", "it", "9:00-15:27")
    calendar.set_meeting("ivan", "programer", "it", "15:30-16:00 16:00-17:00")

    calendar.add_new_worker("alex", "programer", "it")
    calendar.set_meeting("alex", "programer", "it", "17:00-15:27")
    calendar.set_meeting("alex", "programer", "it", "10:30-12:00 16:00-17:00")

    workers = [["ivan", "programer", "it"], ["alex", "programer", "it"]]

    for worker in workers:

        print("work time for ", ' '.join(worker), calendar.get_work_time(*worker))
        print("free time for ", ' '.join(worker), calendar.get_free_time(*worker))


    print("All free time: ", calendar.get_common_free_time(workers))
    print()
    generate_names_dates(num = 3, n_meeting = 2)

