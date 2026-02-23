# Formula 1 Season Tracker

---
## Project Overview

---
The Formula 1 Season Tracker is a Django-based web application designed to manage and track various aspects of a Formula racing season. This application allows users to keep records of drivers, teams, races, and their respective results, providing a comprehensive overview of the racing season.

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

## Installation Guide

---
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
    - `ALLOWED_HOSTS`: Allowed hosts separated by commas, default ones are added for you
    - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Database settings
    
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

### 6. Load Sample Data (Optional)

```sh
python manage.py load_sample_data
```
This will load 3 teams with car models, 3 drivers, 3 tracks, 2 races and 2 race results

### 7. Create Superuser (Admin Access)


```sh
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 8. Run the Development Server

- `DEBUG=True`
```sh
python manage.py runserver
```

- `DEBUG=False`
````sh
python manage.py runserver --insecure
````
If `DEBUG=False` and you run the wrong command, static files will not load.

## Usage

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

Each app is responsible for a clearly defined domain, ensuring separation of concerns and maintainability.

The project adheres to the Model–View–Template (MVT) pattern:

- **Models** handle data representation and business rules.

- **Views** manage application logic and request handling.

- **Templates** define presentation and user interface.

- **Forms** handle validation and data processing.


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

| Field Name        | Type      | Description                 |
|:------------------|:----------|:----------------------------|
| `name`            | CharField | Official team name          |
| `principal`       | CharField | Team principal              |
| `base_country`    | CharField | Country where team is based |
| `engine_supplier` | CharField | Engine manufacturer         |
| `team_color`      | CharField | Hexadecimal UI color        |
| `logo_image_url`  | URLField  | URL to team logo            |


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

| Field Name     | Type                                           | Description           |
|:---------------|:-----------------------------------------------|:----------------------|
| `name`         | CharField                                      | Race name             |
| `round_number` | PositiveIntegerField                           | Championship round    |
| `weather`      | CharField                                      | Weather conditions    |
| `laps`         | PositiveIntegerField                           | Total laps            |
| `date`         | DateTimeField                                  | Race date and time    |
| `track`        | ForeignKey -> Track                            | Hosting circuit       |
| `drivers`      | ManyToManyField -> Driver (through RaceResult) | Drivers participating |

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

`@property` display_finishing_position -> Returns the race status if it is not `Finished`, otherwise,
returns the finishing position.

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
def recalculate_driver_stats(self) -> None:
    results = self.results.all()

    self.total_points = (results.aggregate(total=Sum("points_awarded"))["total"] or 0)

    self.wins = results.filter(finishing_position=1).count()
    self.podiums = results.filter(finishing_position__lte=3).count()
    self.dnfs = results.filter(status="DNF").count()

    self.save()
````

Usage example in `RaceResult` model:
````py
def save(self, *args, **kwargs) -> None:
    super().save(*args, **kwargs)
    self.driver.recalculate_driver_stats()

def delete(self, *args, **kwargs) -> None:
    super().delete(*args, **kwargs)
    self.driver.recalculate_driver_stats()
````
## Optimization

---
To improve performance and avoid N+1 query problems, the project utilizes:
- `select_related()` for ForeignKey joins
- `prefetch_related()` for ManyToMany joins
- `annotate()` for aggregated statistics

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
- DEBUG disabled in production
- CSRF protection
- Separation of database credentials

## Error Handling

---
- Custom 404 page implemented
  - Note that the custom 404 page will not show if `DEBUG=True`
- User-friendly validation messages


## Licensing

---
This project is licensed under the `MIT License`.
