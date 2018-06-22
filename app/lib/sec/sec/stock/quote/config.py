"""
    quote general configures
"""
# connect timeout in seconds
CONNECT_TIMEOUT = 0.1

# read timeout in seconds
READ_TIMEOUT = 0.2

# timeout tuple for requests
TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)

# kickout condition for hosts continues failed times
KICKOUT = 3

# retry count for get quote when failed
RETRY = 3
