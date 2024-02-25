"""Listener that stops execution if a test fails."""

ROBOT_LISTENER_API_VERSION = 2

def end_test(name, attrs):
    print("-----" + name + ":" + attrs['longname'] + ":" + attrs['doc'] +"------\n")