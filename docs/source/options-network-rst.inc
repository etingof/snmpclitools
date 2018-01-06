
.. _options-network:

Network options
---------------

Maximum retries
+++++++++++++++

The *-r* option specifies how many times the |SNMPTOOL| tool should retry
sending the same request packet till it gives up and reports failure. The
value of zero means that just a single (initial) request will be send. The
default value is 5.

Response timeout
++++++++++++++++

The *-t* option specifies how many seconds the |SNMPTOOL| tool should wait
for the initial request and for each retry to produce any response. Once the
timeout is reached, the |SNMPTOOL| tool will either send a retry or fail.
Default is one second.

.. _snmp-peer-address:
