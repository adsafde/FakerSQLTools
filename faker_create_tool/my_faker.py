from faker import Faker

f = Faker("zh_CN")


def get_faker_attribute(name: str):
    value = getattr(f, name)
    return value()
