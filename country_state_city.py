import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCCIA.settings')
django.setup()
from django.db import transaction
from xlrd import open_workbook
from adminapp.models import *
import os

#Start:Use this for local system
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_dir = BASE_DIR + '/MCCIA_BACKOFFICE/Final_data'
#End:Use this for local system

#Start:on server file path
#file_dir='/srv/wsgi/Final_data'
#End:on server file path


@transaction.atomic
def add_country():
    try:
        file_path = [ file_dir +'/countrylist.xlsx']
        print file_path
        for file in file_path:
            wb = open_workbook(file)
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            country_list = []
            for row in range(1, number_of_rows):
                value = (wb.sheets()[0].cell(row, 0).value)
                country_list.append(value)

            print country_list[1]

            sid = transaction.savepoint()
            try:
                for country in country_list:
                    try:
                        Country.objects.get(country_name=country)
                    except Country.DoesNotExist, e:
                        pass
                        try:
                            Countrysobj = Country(country_name=country, created_by="Admin")
                            Countrysobj.save()
                        except Exception, e:
                            print e
                            pass
                            transaction.rollback(sid)
                transaction.savepoint_commit(sid)
            except Exception,e:
                print e
                pass

        print "Country added succesfully"
    except Exception, e:
        print e

if __name__ == "__main__":
    add_country()
