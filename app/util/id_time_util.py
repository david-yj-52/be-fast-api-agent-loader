import uuid


def generate_obj_id():
    return generate_id("OBJ")


def generate_tid():
    return generate_id("TID")


def generate_id(prefix: str):
    return prefix + "-" + _generate_unique_id()


def _generate_unique_id():
    return str(uuid.uuid4())
