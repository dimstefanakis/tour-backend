from django.core.management.base import BaseCommand
from tour.models import Tour, TourName, TourLocation
from destination.models import Destination, Location, Vessel
from datetime import datetime
import csv
import os


class Command(BaseCommand):
    def handle(self, **options):
        workpath = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(workpath, 'itinerary.csv')) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            current_year = datetime.now().year
            for row in reader:
                # print(row)
                print(row['FILE NO'], row['DATE'],
                      row['VESSEL'], row['PORT '], row['ETA'])
                vessel, vessel_created = Vessel.objects.get_or_create(
                    name=row['VESSEL'].strip())
                location, vessel_created = Location.objects.get_or_create(
                    name=row['PORT '].strip())
                datetime_str = f'{row["DATE"].strip()} {current_year} {row["ETA"].strip().replace(",", ":")}'\
                    .strip()
                try:
                    if not row["ETA"].strip():
                        datetime_obj = datetime.strptime(
                            datetime_str, '%d-%b %Y')
                    else:
                        datetime_obj = datetime.strptime(
                            datetime_str, '%d-%b %Y %H:%M')
                except ValueError:
                    datetime_obj = None
                destination = Destination.objects.create(
                    vessel=vessel, location=location, file_name=row['FILE NO'].strip(), eta=datetime_obj)
