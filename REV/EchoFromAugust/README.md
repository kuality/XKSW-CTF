# Echo from August

## Description
An anonymous report claims that a suspicious executable only operates during the month of August.
Upon analysis, it appears to contain hidden code that attempts to initiate a remote connection.
You should extract the IP address and port of the remote control server that this malware tries to connect to, and submit them.

Running the executable directly is dangerous. Perform static analysis only in a safe environment.

## Flag Format
XKSW{IP:Port}

## Level
easy