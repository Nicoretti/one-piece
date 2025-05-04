def _normalize(
    name: str,
    prefix_from: str | None = None,
    prefix_to: str = ":",
    name_sep_from: str | None = "-",
    name_sep_to: str = "_",
) -> str:
    """Normalize a name.

    Args:
    ----
        name: The original name string to normalize.
        prefix_from: The prefix to replace; if None, no replacement occurs.
        prefix_to: The prefix to replace with.
        name_sep_from: The name separator to replace; if None, no replacement occurs.
        name_sep_to: The name separator to replace with.

    Returns:
    -------
        The normalized name.

    """
    name = name.replace(prefix_from, prefix_to) if prefix_from else name
    name = name.replace(name_sep_from, name_sep_to) if name_sep_from else name
    name = name.lower()
    name = name.strip(name_sep_to)
    return name


class NameError(Exception):
    pass


class Identifier:
    @staticmethod
    def validate_identifier(identifier: str):
        """Validates a name string based on a predefined format.

        The expected format is:

        ```bnf
        <IDENTIFIER_FMT> ::= <NAME> | <PREFIX>:<NAME>

        <PREFIX> ::= <IDENTIFIER>
        <NAME> ::= <IDENTIFIER>

        <IDENTIFIER> ::= <LETTER> <IDENTIFIER_PART>
        <IDENTIFIER_PART> ::= <IDENTIFIER_CHAR> | <IDENTIFIER_CHAR> <IDENTIFIER_PART>
                            | ''  (* epsilon, meaning zero or more IDENTIFIER_CHARs *)
        <IDENTIFIER_CHAR> ::= <LETTER> | <DIGIT> | '_'

        <LETTER> ::= <LOWER>
        <LOWER> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j'
                  | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't'
                  | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
        <DIGIT> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
        ```

        Args:
        ----
            identifier: The name string to be validated.

        Raises:
        ------
            NameError: If the name is invalid.

        """

    def __init__(self, name):
        """Creates a normalized identifier name.

        The normalized identifier can serve as a basis for name transformation
        to and from other identifier types/conventions.

        Attention:
        ---------
            For convenience, it is allowed to use uppercase letters where
            lowercase letters are expected, as well as '-' in places where '_'
            is allowed. However, to comply with the format mentioned above,
            uppercase letters will be converted to lowercase, and '-' will be
            converted to '_'.

        Args:
        ----
            name: The original name string.

        Raises:
        ------
            NameError: If the name is invalid after normalization.

        """
        name = _normalize(name, name_sep_from="-", name_sep_to="_")
        Identifier.validate_identifier(name)
        self._name = name

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name

    def __eq__(self, other):
        if not isinstance(other, Identifier):
            raise NotImplementedError
        return self._name == other._name

    @property
    def name(self) -> str:
        """The normalized identifier name."""
        return self._name

    def __str__(self) -> str:
        return str(self._name)


class From:
    @staticmethod
    def cli(name: str) -> Identifier:
        """Converts a CLI argument name to an Identifier.

        Args:
        ----
            name: The CLI argument name.

        Returns:
        -------
            The corresponding Identifier.

        """
        raise NotImplementedError

    @staticmethod
    def env(name: str) -> Identifier:
        """Converts an environment variable name to an Identifier.

        Args:
        ----
            name: The environment variable name.

        Returns:
        -------
            The corresponding Identifier.

        """
        raise NotImplementedError

    @staticmethod
    def toml(section: str, property: str) -> Identifier:
        """Converts a property in a TOML section an Identifier.

        Args:
        ----
            section: The TOML section.
            property: The TOML property name.

        Returns:
        -------
            The corresponding Identifier.

        """
        raise NotImplementedError

    @staticmethod
    def pytest(name: str) -> Identifier:
        """Converts a pytest config attribute name to an Identifier.

        Args:
        ----
            name: The pytest argument name.

        Returns:
        -------
            The corresponding Identifier.

        """
        raise NotImplementedError


class To:
    @staticmethod
    def cli(name: Identifier) -> str:
        """Converts an Identifier to a CLI argument name.

        Args:
        ----
            name: The Identifier to convert.

        Returns:
        -------
            The CLI argument name.

        """
        raise NotImplementedError

    @staticmethod
    def env(name: Identifier) -> str:
        """Converts an Identifier to an environment variable name.

        Args:
        ----
            name: The Identifier to convert.

        Returns:
        -------
            The environment variable name format.

        """
        raise NotImplementedError

    @staticmethod
    def toml(name: Identifier) -> str:
        """Converts an Identifier to a TOML property.

        Args:
        ----
            name: The Identifier to convert.

        Returns:
        -------
            The TOML property format.

        """
        raise NotImplementedError

    @staticmethod
    def pytest(name: Identifier) -> str:
        """Converts an Identifier to a pytest config attribute name.

        Args:
        ----
            name: The Identifier to convert.

        Returns:
        -------
            The pytest argument config attribute name.

        """
        raise NotImplementedError
