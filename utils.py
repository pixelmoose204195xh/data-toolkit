"""General-purpose helpers for the data-toolkit project."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from typing import Any, TypeVar

T = TypeVar("T")


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield items in lists containing at most ``size`` elements.

    Args:
        items: Iterable whose values will be grouped.
        size: Maximum number of elements per chunk. Must be positive.

    Yields:
        Lists of up to ``size`` elements, preserving input order.

    Raises:
        ValueError: If ``size`` is not positive.
    """
    if size <= 0:
        raise ValueError("size must be greater than zero")

    chunk: list[T] = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


def flatten_mapping(
    data: Mapping[str, Any],
    *,
    separator: str = ".",
    prefix: str = "",
) -> dict[str, Any]:
    """Flatten a nested mapping into a dictionary with joined string keys.

    Args:
        data: Mapping to flatten. Nested mapping values are processed recursively.
        separator: Text inserted between key path components.
        prefix: Optional path prepended to every generated key.

    Returns:
        A flat dictionary. Empty nested mappings are retained as values.

    Raises:
        ValueError: If ``separator`` is empty.
        TypeError: If a mapping key is not a string.
    """
    if not separator:
        raise ValueError("separator must not be empty")

    flattened: dict[str, Any] = {}
    pending: list[tuple[str, Mapping[str, Any]]] = [(prefix, data)]

    while pending:
        current_prefix, current = pending.pop()
        for key, value in current.items():
            if not isinstance(key, str):
                raise TypeError("all mapping keys must be strings")

            path = (
                f"{current_prefix}{separator}{key}"
                if current_prefix
                else key
            )
            if isinstance(value, Mapping) and value:
                pending.append((path, value))
            else:
                flattened[path] = value

    return flattened


def get_nested(
    data: Mapping[str, Any],
    path: str | Iterable[str],
    *,
    default: Any = None,
    separator: str = ".",
) -> Any:
    """Read a value from a nested mapping without raising for missing keys.

    Args:
        data: Mapping to traverse.
        path: Iterable of keys or a separator-delimited key path.
        default: Value returned when a key is absent or traversal reaches a
            non-mapping value.
        separator: Delimiter used when ``path`` is a string.

    Returns:
        The located value, or ``default`` when the path cannot be resolved.

    Raises:
        ValueError: If a string path or its separator is empty.
    """
    if isinstance(path, str):
        if not separator:
            raise ValueError("separator must not be empty")
        if not path:
            raise ValueError("path must not be empty")
        keys = path.split(separator)
    else:
        keys = list(path)
        if not keys:
            raise ValueError("path must not be empty")

    current: Any = data
    for key in keys:
        if not isinstance(current, Mapping) or key not in current:
            return default
        current = current[key]

    return current


def coerce_boolean(value: Any, *, strict: bool = True) -> bool | None:
    """Convert common scalar representations to a boolean value.

    Recognized true values are ``True``, ``1``, ``"true"``, ``"yes"``,
    ``"y"``, and ``"1"``. False equivalents include ``False``, ``0``,
    ``"false"``, ``"no"``, ``"n"``, and ``"0"``. String matching ignores
    surrounding whitespace and letter case.

    Args:
        value: Scalar value to convert.
        strict: Raise an error for unrecognized values when true; otherwise
            return ``None``.

    Returns:
        The converted boolean, or ``None`` for an unrecognized value in
        non-strict mode.

    Raises:
        ValueError: If ``value`` is unrecognized and ``strict`` is true.
    """
    if isinstance(value, bool):
        return value
    if value == 1:
        return True
    if value == 0:
        return False
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in {"true", "yes", "y", "1"}:
            return True
        if normalized in {"false", "no", "n", "0"}:
            return False

    if strict:
        raise ValueError(f"cannot coerce {value!r} to boolean")
    return None