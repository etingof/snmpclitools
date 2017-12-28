.. _options-debug:

Debugging options
-----------------

Release information
+++++++++++++++++++

The *-V* flag reports version information for the |SNMPTOOL| tool and its underlying
libraries.

Debug mode
++++++++++

The *-d* option prints out raw SNMP packets in hex.

The *-D* option lets you debug one or more specific SNMP sub-systems. The required
argument can be one or more (comma-separated) tokens:

* *io*         - report input/output activity and raw data being exchanged
* *dsp*        - report high-level SNMP engine operation
* *msgproc*    - report SNMP message processing subsystem operation
* *secmod*     - report SNMP security subsystem operation
* *mibbuild*   - report MIB files loading and processing
* *mibview*    - report MIB browser initialization and operation (manager role MIB use)
* *mibinstrum* - report MIB instrumentation operation (agent role MIB use)
* *acl*        - report MIB access control subsystem operation
* *proxy*      - report built-in SNMP proxy operation
* *app*        - report SNMP standard application operation
* *all*        - all of the above (verbose!)

You can also negate the token by prepending it with the *!* sign.
