import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_service.settings")
django.setup()

from car_service.repositories.RepositoryManager import RepositoryManager

if __name__ == "__main__":
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_service.settings")
    django.setup()

    repo = RepositoryManager()

    """id=1
    sc=repo.serviceCenter.get_by_id(id)
    print(sc.repair_set.all())
    for repair in repo.repair.get_by_id():
        print(repair)
    print("Cars:")
    for car in repo.car.get_all():
        print(car)

    repo.car.update(1, brand="Toyota")
    # repo.car.update(1, brand="Audi")

    new_client = repo.client.create(
        firstName="Roman",
        lastName="Romanov",
        phoneNumber="+380971234777",
        email="roman@example.com"
    )
    print("\nNew Client Added:", new_client.idClient, new_client.firstName, new_client.lastName)

    id = 6
    rez = repo.client.delete(id)
    if rez:
        print(f"\nClient with id = {id} deleted")
    else:
        print(f"\nClient with id = {id} doesn't exist")

    print("Clients:")
    for client in repo.client.get_all():
        print(client)
    emp = repo.employee.get_by_id(1)
    if emp:
        print("\nEmployee with ID=1:", emp)"""
