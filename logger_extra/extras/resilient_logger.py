import uuid
from typing import Any


def _parse_uuid(value: str | uuid.UUID | None) -> uuid.UUID | None:
    """
    Parses the given value into a UUID instance or returns None if parsing fails.
    """
    if value is None:
        return None

    if isinstance(value, uuid.UUID):
        return value

    try:
        return uuid.UUID(value)
    except (ValueError, TypeError):
        return None


def _mask_str(value: str) -> str:
    """
    Masks the first half of the input string to remove sensitive data.
    """
    mask_limit = int(len(value) / 2)
    return "*" * mask_limit + value[mask_limit:]


def _get_field(target: object, key: str) -> Any:
    """
    Functions as either getattr(object, key, None) or dict.get(key, None)
    """
    if isinstance(target, dict):
        return target.get(key, None)
    return getattr(target, key, None)


def resolve_actor_with_masked_email(actor) -> dict:
    """
    resolve_actor function for django-resilient-logger. Includes actor email (masked)
    and UUID in the resilient log entry

    Returns:
        dict: The actor data with resolved UUID, and masked email, if those are present
    """
    actor_data = {
        "uuid": None,
        "version": None,
        "email": None,
    }

    if not actor:
        return actor_data

    raw_uuid = _get_field(actor, "uuid")
    raw_email = _get_field(actor, "email")
    parsed_uuid = _parse_uuid(raw_uuid)

    if parsed_uuid:
        actor_data["uuid"] = str(parsed_uuid)
        actor_data["version"] = getattr(parsed_uuid, "version", None)
    if raw_email:
        actor_data["email"] = _mask_str(raw_email)

    return actor_data
