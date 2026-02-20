from django.core.management.base import BaseCommand
from teams.models import Team, CarModel
from races.models import Track
from drivers.models import Driver
from races.models import Race, Result
from django.utils.timezone import make_aware
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        # TEAMS
        ferrari = Team.objects.create(
            name="Ferrari",
            principal="Frédéric Vasseur",
            base_country="Italy",
            engine_supplier="Ferrari",
            team_color="#ED1131",
            logo_image_url="https://www.edigitalagency.com.au/wp-content/uploads/Ferrari-logo-png-full-colour-medium-size.png"
        )

        redbull = Team.objects.create(
            name="Red Bull Racing",
            principal="Christian Horner",
            base_country="Austria",
            engine_supplier="Honda",
            team_color="#003773",
            logo_image_url="https://static.wikia.nocookie.net/f1wikia/images/1/18/Oracle_Red_Bull_Racing.png"
        )

        mercedes = Team.objects.create(
            name="Mercedes",
            principal="Toto Wolff",
            base_country="UK",
            engine_supplier="Mercedes AMG",
            team_color="#00D7B6",
            logo_image_url="https://r2.thesportsdb.com/images/media/team/badge/6caw0r1744037679.png"
        )

        # CAR MODELS
        CarModel.objects.create(
            name="RB20",
            year=2024,
            power_unit="Honda RBPTH002",
            in_use=True,
            team=redbull
        )

        CarModel.objects.create(
            name="MERCEDES",
            year=2025,
            power_unit="MC",
            in_use=True,
            team=mercedes
        )

        # TRACKS
        monza = Track.objects.create(
            name="Monza",
            country="Italy",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Monza_track_map.svg/1920px-Monza_track_map.svg.png",
            length_km=5.79
        )

        silverstone = Track.objects.create(
            name="Silverstone",
            country="United Kingdom",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Silverstone_Circuit_vector_map.png/1920px-Silverstone_Circuit_vector_map.png",
            length_km=5.89
        )

        spa = Track.objects.create(
            name="Spa-Francorchamps",
            country="Belgium",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Spa-Francorchamps_of_Belgium.svg/1920px-Spa-Francorchamps_of_Belgium.svg.png",
            length_km=7.00
        )

        # DRIVERS
        verstappen = Driver.objects.create(
            name="Max Verstappen",
            nationality="NL",
            age=28,
            rookie_status=False,
            image="https://sportrenders.com/wp-content/uploads/2023/10/Verstappen-Red-bull-Render-PNG-Formula-1-Sport-Renders-Images.png",
            team=redbull,
            wins=2,
            total_points=25,
            podiums=2,
            dnfs=0
        )

        leclerc = Driver.objects.create(
            name="Charles Leclerc",
            nationality="MC",
            age=28,
            rookie_status=False,
            image="https://media.formula1.com/image/upload/c_fill,w_720/q_auto/v1740000000/common/f1/2025/ferrari/chalec01/2025ferrarichalec01right.webp",
            team=ferrari,
            wins=0,
            total_points=0,
            podiums=1,
            dnfs=0
        )

        tsunoda = Driver.objects.create(
            name="Yuki Tsunoda",
            nationality="JP",
            age=25,
            rookie_status=True,
            image="https://www.kymillman.com/wp-content/uploads/f1/pages/driver-profiles/yuki-tsunoda/yuki-tsunoda-hero-driver.png",
            team=redbull,
            wins=0,
            total_points=0,
            podiums=1,
            dnfs=0
        )

        # RACES
        austrian_gp = Race.objects.create(
            name="Austrian Grand Prix",
            round_number=12,
            weather="Sunny",
            laps=67,
            date=make_aware(datetime(2026, 2, 15)),
            track=monza
        )

        belgian_gp = Race.objects.create(
            name="Belgian Grand Prix",
            round_number=13,
            weather="Rainy",
            laps=67,
            date=make_aware(datetime(2026, 2, 15)),
            track=spa
        )

        # RESULTS
        Result.objects.create(
            qualifying_position=1,
            finishing_position=1,
            points_awarded=25,
            fastest_lap=True,
            status="Finished",
            driver=verstappen,
            race=austrian_gp
        )

        Result.objects.create(
            qualifying_position=2,
            finishing_position=2,
            points_awarded=0,
            fastest_lap=False,
            status="Finished",
            driver=leclerc,
            race=austrian_gp
        )

        self.stdout.write(self.style.SUCCESS("Sample data loaded successfully!"))
