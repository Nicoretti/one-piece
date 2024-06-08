import io
from enum import IntEnum
from inspect import cleandoc


class ExitCode(IntEnum):
    Success = 0
    Failure = 1


class TextBuffer:
    """Class to manage a text buffer using StringIO."""

    def __init__(self):
        """
        Initializes a new instance of the TextBuffer class.
        """
        self._buffer = io.StringIO()

    def __enter__(self):
        """
        Enters the runtime context related to this object.

        Returns:
            The TextBuffer instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context related to this object.

        Args:
            exc_type: The exception type.
            exc_val: The exception value.
            exc_tb: The traceback object.
        """
        self._buffer.close()

    def append(self, text):
        """
        Appends text to the buffer.

        Args:
            text: The text to append to the buffer.
        """
        self._buffer.write(text)

    def __iadd__(self, other):
        """
        Implements the in-place addition operation.

        Args:
            other: The text to add to the buffer.

        Returns:
            The TextBuffer instance.
        """
        self._buffer.write(other)
        return self

    @property
    def content(self):
        """
        Retrieves the content of the buffer.

        Returns:
            The content of the buffer as a string.
        """
        return self._buffer.getvalue()


def default(args, stdout, stderr):
    err_msg = cleandoc(f"""
    This function is not implemented yet!

        Details:
            Args: {args}

        In case you need more details, consider running the command with the `--debug` flag.
    """)
    raise NotImplementedError(err_msg)
