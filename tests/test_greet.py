def greet(name: str) -> str:
    """Return a greeting string for the given name."""
    return f"Hello, {name}!"


def test_greeting() -> None:
    """Test that the greet function returns the expected string."""
    result = greet("World")
    assert result == "Hello, World!"
