from main_absence_schedule.models import Absence, Schedule

def cronjob():
    print("SUCCESS CRON")
    for i in range(3):
        data = Absence.objects.get(pk=i)
        print(f"Data={data}")
    print("SUCCESS ADD")

cronjob()