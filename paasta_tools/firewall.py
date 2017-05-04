# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import errno
import fcntl
import os.path
import random

MAC_ADDRESS_PREFIX = ('02', '52')


def reserve_unique_mac_address(lock_directory):
    """ Pick and reserve a unique mac address for a container
    returns (mac_address, lockfile)
    where the mac address is a string in the form of 00:00:00:00:00:00
    and lockfile is a file object that holds an exclusve lock
    """
    for x in range(100):
        random_hex = hex(random.getrandbits(32))
        mac_address = ':'.join(
            MAC_ADDRESS_PREFIX + (
                random_hex[2:4],
                random_hex[4:6],
                random_hex[6:8],
                random_hex[8:10]
            )
        )

        lock_filepath = os.path.join(lock_directory, mac_address)
        lock_file = obtain_lock(lock_filepath)
        if lock_file is not None:
            return (mac_address, lock_file)

    return None  # TODO


def obtain_lock(lock_filepath):
    """ Open and obtain a flock on the parameter. Returns a file if successful, None if not
    """
    lock_file = open(lock_filepath, 'w')
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_file
    except IOError as err:
        if err.errno != errno.EAGAIN:
            raise
        lock_file.close()
        return None
