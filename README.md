# Formula 1 Season Tracker

---
## Project Overview

---
The Formula 1 Season Tracker is a Django-based web application designed to manage and track various aspects of a Formula racing season. This application allows users to keep records of drivers, teams, races, and their respective results, providing a comprehensive overview of the racing season.


### Deployment
This application is deployed using `Azure`. Follow the link to access the application.

**Official URL:** https://formulaseasontracker-f8d6cme7h4hcethv.switzerlandnorth-01.azurewebsites.net/

## Application Preview

---
Preview of some of the pages included in the project.
### Home Page
![Home Page](docs/screenshots/home.png)

### Team Detail Page
![Team Detail](docs/screenshots/team-detail.png)

### Race Results Page
![Race Results](docs/screenshots/race-results.png)

_Please note that there is example data included in the screenshots_

## Requirements

---
In order to run this project, you will need to fulfill the following requirements:
- Python 3.10+
- Django
- PostgreSQL (database)


## Key Features

---
Based on the Django applications, the project includes functionalities for:

- **Common Utilities**: General functionalities and utilities shared across the application.
- **Drivers Management**: Detailed profiles and statistics for individual racing drivers.
- **Teams Management**: Information and performance tracking for racing teams.
- **Races Management**: Schedule, results, and details of each race event.
- **CRUD**: Full create/read/update/delete implemented for the following models:
  - `Team`
  - `CarModel`
  - `Race`
  - `RaceResult`
  - `Driver`
  - `Track` (only for users in the `TrackAdmin` group)

## Installation Guide

---
Follow the steps only if you want to run the project locally on your machine.
### 1️. Clone the Repository

```sh
git clone <repository-url>
cd <project-directory>
```
### 2. Edit Environment Details

- Copy the `env.template` file
    ````sh
    cp .env.template .env
    ````
- Configure the `.env` file by filling in the following variables  

    - `DJANGO_SECRET_KEY`: Secret key
    - `DEBUG`: True for development, False for production
    - `CSRF_TRUSTED_ORIGINS`: URLs, which the application should accept CSRF tokens from, separated by a comma 
    - `ALLOWED_HOSTS`: Allowed hosts separated by commas, default ones are added for you
    - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Database settings
    - `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`: Celery settings, should be a valid redis database (local or cloud)
      - **FOR EXAMINERS:** If you do not have a redis database, you can use mine with the following URL (use it for both celery environment variables): `redis://default:rhwtfoLb77Qw2wv0h7TpOib9uzoen1PE@redis-18776.c282.east-us-mz.azure.cloud.redislabs.com:18776`  
      Will be deleted after assessment.
    
### 3. Create Virtual Environment

#### Windows
```sh
python -m venv .venv
.venv/scripts/activate
```

#### macOS / Linux

```sh
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```sh
pip install -r requirements.txt
```

### 5. Apply Migrations

```sh
python manage.py migrate
```
- Three Tracks will be added automatically

### 6. Create Superuser (Admin Access)


```sh
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 8. Start `Celery`

```sh
celery -A FormulaSeasonTracker worker -l info --pool=threads
```

In a new terminal:  
- Enter the project directory again and also connect to the `venv`.
```sh
celery -A FormulaSeasonTracker beat -l info
```

### 7. Run the Development Server
In a new terminal:  
Enter the project folder again and also connect to the `venv`.

- `DEBUG=True`
```sh
python manage.py runserver
```

- `DEBUG=False`
````sh
python manage.py runserver --insecure
````
If `DEBUG=False` and you run the wrong command, static files will not load.


### 9. Usage

---
*   Navigate to `http://127.0.0.1:8000/` in your web browser.
*   Explore the different sections for drivers, teams, and races.
*   Access the Django admin panel at `http://127.0.0.1:8000/admin/` to manage data if you created a superuser.

## Project Structure

---
The application follows Django’s modular architecture by separating functionality into domain-specific apps:
- `teams` 
- `drivers` 
- `races` 
- `common`
- `tracks`
- `accounts`

Each app is responsible for a clearly defined domain, ensuring separation of concerns and maintainability.

The project adheres to the Model–View–Template (MVT) pattern:

- **Models** handle data representation and business rules.

- **Views** manage application logic and request handling, most of them are class-based.

- **Templates** define presentation and user interface.

- **Forms** handle validation and data processing.

## Django User Model Extension

---
A model called `Profile` utilizes a One-to-One relationship with the `User` model


| Field Name        | Type                     | Description                        |
|:------------------|:-------------------------|:-----------------------------------|
| `profile_picture` | ImageField               | Profile picture of a user          |
| `favorite_tracks` | Many-to-Many to `Tracks` | Indicates a user's favorite tracks |

The application also handles media files. `Pillow` is used for `ImageField`.  
A custom validator, `MaxSizeValidator`, checks whether the profile picture is under a certain amount of `MB`.

## User Groups

---
The user groups are defined in the Django admin. There are **two** of them currently:
- `Users` - automatically assigned on user creation through a signal
  - They have CRUD access for the following models: `Race`, `Result`, `Driver`, `Team`
- `TrackAdmins` - only assigned through Django Administration
  - They only have CRUD access to the `Track` model


## Models

---
### BaseTimeStamp Model
Abstract class, does not create a database table.

| Field Name   | Type          | Description                 |
|:-------------|:--------------|:----------------------------|
| `updated_at` | DateTimeField | When model was last updated |
| `created_at` | DateTimeField | When model was created      |

---
### Team Model | Inherits `BaseTimeStamp`

Represents a Formula 1 constructor.

| Field Name        | Type               | Description                  |
|:------------------|:-------------------|:-----------------------------|
| `name`            | CharField          | Official team name           |
| `principal`       | CharField          | Team principal               |
| `base_country`    | CharField          | Country where team is based  |
| `engine_supplier` | CharField          | Engine manufacturer          |
| `team_color`      | CharField          | Hexadecimal UI color         |
| `logo_image_url`  | URLField           | URL to team logo             |
| `owner`           | ForeignKey -> User | Indicates team's owner       |


#### Relationships:
- One-to-Many with Driver
- One-to-One with CarModel

---
### CarModel Model
Represents a team's car.

| Field Name       | Type                  | Description             |
|:-----------------|:----------------------|:------------------------|
| `name`           | CharField             | Car model name          |
| `year`           | PositiveIntegerField  | Manufacturing year      |
| `power_unit`     | CharField             | Engine specification    |
| `in_use`         | BooleanField          | Indicates active status |
| `team`           | OneToOneField -> Team | Associated team         |

---
### Driver Model
Represents a Formula 1 driver.

| Field Name      | Type                 | Description                                              |
|:----------------|:---------------------|:---------------------------------------------------------|
| `name`          | CharField            | Driver name                                              |
| `number`        | PositiveIntegerField | A number with which the driver is associated             |
| `nationality`   | CharField            | Country 2 letter code                                    |
| `age`           | PositiveIntegerField | Driver age                                               |
| `rookie_status` | BooleanField         | Rookie indicator                                         |
| `image`         | URLField             | Link to driver's image                                   |
| `team`          | ForeignKey -> Team   | Associated team                                          |
| `wins`          | PositiveIntegerField | Total wins                                               |
| `total_points`  | PositiveIntegerField | Accumulated points                                       |
| `podiums`       | PositiveIntegerField | Podium finishes                                          |
| `dnfs`          | PositiveIntegerField | Number of times driver **D**id **N**ot **F**inish a race |
| `owner`         | ForeignKey -> User   | Indicates driver's owner                                 |

---
### Track Model | Inherits `BaseTimeStamp`
Represents a Formula 1 circuit.

| Field Name  | Type         | Description                |
|:------------|:-------------|:---------------------------|
| `name`      | CharField    | Circuit Name               |
| `country`   | CharField    | Host country               |
| `image_url` | URLField     | Track layout image         |
| `length_km` | DecimalField | Track length in kilometers |

**IMPORTANT:** Tracks can only be created/edited/deleted through the Track Admin.

---
### Race Model
Represents a Grand Prix event.

| Field Name     | Type                                           | Description                                |
|:---------------|:-----------------------------------------------|:-------------------------------------------|
| `name`         | CharField                                      | Race name                                  |
| `round_number` | PositiveIntegerField                           | Championship round                         |
| `weather`      | CharField                                      | Weather conditions                         |
| `laps`         | PositiveIntegerField                           | Total laps                                 |
| `date`         | DateTimeField                                  | Race date and time                         |
| `track`        | ForeignKey -> Track                            | Hosting circuit                            |
| `drivers`      | ManyToManyField -> Driver (through RaceResult) | Drivers participating                      |
| `started_by`   | ForeignKey -> User                             | Refers to the user, who initiated the race |

---
### RaceResult Model
Stores contextual race performance data.

| Field Name            | Type                 | Description                                 |
|:----------------------|:---------------------|:--------------------------------------------|
| `qualifying_position` | PositiveIntegerField | Grid position                               |
| `finishing_position`  | PositiveIntegerField | Final position                              |
| `points_awarded`      | PositiveIntegerField | Points earned                               |
| `fastest_lap`         | BooleanField         | Fastest lap indicator                       |
| `status`              | CharField            | Race status for driver (Finished, DNF, etc) |
| `driver`              | ForeignKey -> Driver | Associated driver                           |
| `race`                | ForeignKey -> Race   | Associated race                             |
| `owner`               | ForeignKey -> User   | Indicates who created the result            |

`@property` display_finishing_position -> Returns the race status if it is not `Finished`, otherwise,
returns the finishing position.

---
###

## Mixins

---
### `ReadOnlyFormFieldsMixin`
- Turns a form's fields into read-only by inheriting the mixin
- Used as delete confirmation for forms which delete database records

Usage examples:

````py
class DriverDeleteForm(ReadOnlyFormFieldsMixin, DriverFormBase):
    pass

class RaceDeleteForm(ReadOnlyFormFieldsMixin, RaceFormBase):
    pass
````

### `OwnerOnlyMixin`
- Inherits `UserPassesTestMixin` and overrides `test_func`
- Checks whether the request user matches with an object's owner
---
## Data Integrity & Constraints

The following constraints are enforced:
- A driver can only have one result per race
- Finishing and qualifying positions must be unique per race
- Only one fastest lap is allowed per race
- A team can have a maximum of 2 drivers

Validation layers:
- Form-level validation 
- Model-level validation 
  - Custom validators included
- Database-level constraints

Overriding some models' `save()`, `delete()` and `clean()` methods

Example:

The Driver model has a method `recalculate_driver_stats`, which
recalculates a driver's `total_points`, `wins`, `dnfs` and `podiums`.

````py
@shared_task
def recalculate_driver_stats_task(driver_id):
    try:
        driver = Driver.objects.get(pk=driver_id)
        results = driver.results.all()

        driver.total_points = (results.aggregate(total=Sum("points_awarded"))["total"] or 0)
        driver.wins = results.filter(finishing_position=1).count()
        driver.podiums = results.filter(finishing_position__lte=3).count()
        driver.dnfs = results.filter(status="DNF").count()

        driver.save(update_fields=["total_points", "wins", "podiums", "dnfs"])
    except Driver.DoesNotExist:
        pass

````

Usage example in `RaceResult` model:
````py
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        recalculate_driver_stats_task.delay(self.driver.pk)

    def delete(self, *args, **kwargs) -> None:
        super().delete(*args, **kwargs)
        recalculate_driver_stats_task.delay(self.driver.pk)
````

## Asynchronous Operations

---
Currently, there are **two** asynchronous operations implemented using `celery` and a `redis` database:
- `recalculate_driver_stats_task` used for recalculating a driver's points, wins, DNFs and podiums every time a race
  result is added, edited or deleted.
- `delete_all_races_task` deletes all races every 24 hours at a set time. This uses celery beat.


## Optimization

---
To improve performance and avoid N+1 query problems, the project utilizes:
- `select_related()` for ForeignKey joins
- `prefetch_related()` for ManyToMany joins
- `annotate()` for aggregated statistics
- Asynchronous operations using `celery` and `redis`

Example:

````py
driver.results.select_related("race").order_by("-race__date")[:3]
````
To avoid having too many templates:
- Template inheritance to avoid repetitive HTML
- For each model, the forms used to create, edit, and delete records are merged into a single template.
- Reusing templates in views

## Security

---
Security is handled through:
- Environment variable configuration
- Hidden SECRET_KEY
- Proper ALLOWED_HOSTS configuration
- Usage of CSRF_ALLOWED_HOSTS
- DEBUG disabled in production
- CSRF protection
- Separation of database credentials

## Testing

To ensure the app works properly in the future, tests are included as well:
- Currently, there are a total of **26** tests for this project
- They can be found in the `tests` directory

## Error Handling

---
- Custom `404` page implemented as well as one for `403`
  - Note that the custom 404 page will not show if `DEBUG=True`
- User-friendly validation messages


## Licensing

---
This project is licensed under the `MIT License`.
