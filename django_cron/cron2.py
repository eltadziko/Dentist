from django_cron import CronJobBase, Schedule
from Dentist.models import *
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 2 # every 2 minutes
    RUN_AT_TIMES = ['20:04', '20:09', '20:13']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'django_crons.my_cron_job'    # a unique code

    def do(self):
        print 'BLEEEEEEEEEEEEE2'
        dis = disease(disease_name="plum2")
        dis.save()