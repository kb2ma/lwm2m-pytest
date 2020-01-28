These tests exercise RIOT's LwM2M client implementation. The tests are automated with the use of [pytest](https://pytest.org/).

With all of these tests, your confidence in the results will increase by watching the CoAP messages in Wireshark.

Materials
=========

In addition to pytest, you'll need a recent copy of the other projects listed below.

The _Setup_ section below assumes these projects are installed in source code form, not with pip or setup.py. Use your judgement, but notice that some dependent libraries within these projects *are* installed with pip.

RIOT Apps
---------
[riot-apps](https://github.com/kb2ma/riot-apps): Forked from RIOT-OS/applications, use *lwm2m-client* branch. Uses the LwM2M Client app in the `lwm2m-client` directory.

Leshan
-------
[Leshan](https://github.com/eclipse/leshan) is a LwM2M server.

Build and run the demo server as shown in the Leshan [README](https://github.com/eclipse/leshan/blob/master/README.md).


Setup
=====

native2os
---------
Some of these tests use a tap interface to communicate between a native RIOT instance and the Linux desktop. They require an fd00:bbbb::/64 ULA-based network defined on the desktop as:
```
    $ sudo ip tuntap add tap0 mode tap user ${USER}
    $ sudo ip link set tap0 up
    $ sudo ip address add fd00:bbbb::1/64 dev tap0 scope global
```

Some tests do not allow specification of the address, so the test uses the TAP_LLADDR_SUT environment variable for the link local address for the RIOT endpoint, and TAP_LLADR_REMOTE for the address of the OS endopint. You can specify a link local address for tap with:
```
    sudo ip link set dev tap0 address 0:0:bb:bb:0:1
    sudo ip address add fe80::200:bbff:febb:1/64 dev tap0 scope link
```
Notice the REMOTE tap interface address uses host '1', while the SUT address for the RIOT board must use host '2'.

Some tests require environment variables. See `setup_env.sh`. You MUST adapt it to the paths on your machine, but then you can source it with:
```
    $ . setup_env.sh
```
As mentioned in the _Materials_ section, presently the script is based on installation of aiocoap and libcoap in source form.


Running the tests
=================
See the pytest [usage documentation](https://docs.pytest.org/en/latest/usage.html) for variations.
