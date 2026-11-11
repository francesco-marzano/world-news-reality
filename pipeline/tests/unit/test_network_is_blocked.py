import socket

import pytest
from pytest_socket import SocketBlockedError


@pytest.mark.filterwarnings("ignore:A test tried to use socket")
def test_tests_cannot_open_sockets() -> None:
    """Guards the rule "tests run on fixtures, never on live feeds"."""
    with pytest.raises(SocketBlockedError):
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
