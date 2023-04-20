from django.core.management.base import BaseCommand
from tour.models import Tour, TourName, TourLocation
from destination.models import Destination, Location, Vessel
from guide.models import Guide, ResponseStatus
from datetime import datetime
import csv
import os


class Command(BaseCommand):
    def handle(self, **options):
        workpath = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(workpath, 'april_guides.csv')) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            days_dict = {}

            for i, row in enumerate(reader):
                # print(row)
                for key, item in row.items():
                    if i == 0:
                        if key not in days_dict:
                            days_dict[key] = {'ship': item, 'guides': []}
                    elif i == 1:
                        days_dict[key]['location'] = item
                    else:
                        if item:
                            days_dict[key]['guides'].append(item)

            guides_dict = {}
            # now we need a dictionary with guides as keys and day / ship / location as values

            for day, data in days_dict.items():
                for guide in data['guides']:
                    if guide not in guides_dict:
                        guides_dict[guide] = []
                    guides_dict[guide].append(
                        {'day': day, 'ship': data['ship'], 'location': data['location']})

            for guide_name, data in guides_dict.items():
                guide = Guide.objects.filter(
                    name__iexact=guide_name)
                if not guide.exists():
                    guide = Guide.objects.create(
                        name=guide_name)
                else:
                    guide = guide.first()
                for tour_data in data:
                    input_format = "%A %d %B"
                    # some days have a special word in front of them, so we need to remove that
                    print(tour_data)
                    if len(tour_data['day'].split(' ')) > 3:
                        tour_data['day'] = tour_data['day'].split(' ', 1)[1]
                    day = datetime.strptime(tour_data['day'], input_format)
                    vessel = tour_data['ship']
                    location = tour_data['location']

                    destination = Destination.objects.filter(
                        vessel__name__iexact=vessel.strip(), location__name__iexact=location.strip()).first()
                    if not destination:
                        destination = Destination.objects.create(
                            vessel=Vessel.objects.create(name=vessel.strip()),
                            location=Location.objects.create(
                                name=location.strip())
                        )
                    tour, tour_created = Tour.objects.get_or_create(
                        day=day, destination=destination,
                        guide=guide)
                    tour_name, tour_name_created = TourName.objects.get_or_create(
                        name=f"{tour_data['location']}")
                    tour.destination = destination
                    tour.name = tour_name
                    tour.save()
