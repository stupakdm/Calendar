# Calendar

Календарь для подсчета свободного времени сотрудников.

Реализовано 2 класса:
# Класс Calendar
Публичные методы:
  - add_new_worker - добавить нового сотрудника. Параметры функции: (name, quality, department, work_time="09:00-18:00",    busy_time="00:00-00:00")
  - get_work_time - получить рабочее время сотрудника 
  - get_free_time - получить свободные слоты сотрудника 
  - set_meeting - задать встречу для сотрудника
  - get_common_free_time - получить общее свободное время заданного списка сотрудников
# Класс Worker
Он хранит в себе всю информацию о сотруднике:
  - Имя, квалификация, отдел
  - Рабочее время сотрудника
  - Занятые слоты
  - Свободное время
  - Публичные методы:
    - busy_time_get - возвращает занятые слоты сотрудника
    - busy_time_set - задает занятые слоты для сотрудника
    - free_time_get - возвращает свободное время сотрудника
    - work_time_get - возращает рабочее время сотрудника
    
  - Приватные методы:
    - __add_busy_time - добавляет встречу в список встреч
    - __recount_free_time - подсчитывает свободное время сотрудника
    
 # Функция generate_names_dates тестирует правильность выполнения программы. В ней генерируется n число, для каждого генерируется своё рабочее время, время встречи. И затем выполняется расчёт общего свободного времени для случайного списка сотрудников.
 
  
