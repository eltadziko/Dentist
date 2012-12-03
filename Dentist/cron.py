from django_cron import CronJobBase, Schedule
from models import *
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 2 # every 2 minutes
    RUN_AT_TIMES = ['20:00', '20:01', '20:02']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'Dentist.my_cron_job'    # a unique code

    def do(self):
        print 'BLEEEEEEEEEEEEE'
        dis = disease(disease_name="plum")
        dis.save()