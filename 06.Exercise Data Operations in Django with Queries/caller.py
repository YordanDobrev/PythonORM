import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


# Create queries within functions

def create_pet(name: str, species: str):
    pet = Pet.objects.create(
        name=name,
        species=species
    )
    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return str(artifact)


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    locations = Location.objects.all().order_by("-id")

    return "\n".join(str(l) for l in locations)


def new_capital():
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    locations = Location.objects.filter(is_capital=True).values("name")
    return locations


def delete_first_location():
    location = Location.objects.first().delete()


def apply_discount():
    all_cars = Car.objects.all()

    for car in all_cars:
        discount = sum(int(d) for d in str(car.year)) / 100 * float(car.price)
        car.price_with_discount = float(car.price) - discount
        car.save()


def get_recent_cars():
    cars = Car.objects.filter(year__gt=2020).values("model", "price_with_discount")
    return cars


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    tasks = Task.objects.filter(is_finished=False)
    return "\n".join(str(t) for t in tasks)


def complete_odd_tasks():
    tasks = Task.objects.all()
    for t in tasks:
        if t.id % 2 == 1:
            t.is_finished = True
            t.save()


def encode_and_replace(text: str, task_title: str):
    encoded_text = "".join(chr(ord(t) - 3) for t in text)
    Task.objects.filter(title=task_title).update(description=encoded_text)


def get_deluxe_rooms():
    rooms = HotelRoom.objects.filter(room_type="Deluxe")
    return "\n".join(str(r) for r in rooms if r.id % 2 == 0)


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by('id')  # id 1, id 2...

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()