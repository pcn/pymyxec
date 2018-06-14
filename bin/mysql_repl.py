#!/usr/bin/env python

# The goal of this is to be the entry point for a zip file that will do the following:

# 1. extract a shared object from the zipfile
# 2. put it into an in-memory file
# 3. symlink the in-memory file to a temporary directory
# 4. add that to LD_LIBRARY_PATH, or invoke dlopen or something.
# 5. This should be done after setting the zip_safe attribute

import os
from ctypes import CDLL
import zipfile
import sys
import time

# https://github.com/n1nj4sec/pupy/issues/298#issuecomment-285494660 has
# returns a tuple of this_pid, and the fd number this lib's data is attached to
def entry(lib_name, internal_lib_path):
    print("You got it")
    print("{}".format(sys.path))
    lib_obj = extract_lib_from_self(internal_lib_path)
    fd_num = build_a_lib(lib_name, lib_obj)
    this_pid = os.getpid()
    print("this pid is {}, lib_fd is {}".format(this_pid, this_pid))
    return this_pid, fd_num

        
def extract_lib_from_self(internal_lib_path):
    me = "/".join(sys.path[0].split('/')[0:2])
    thezip = zipfile.ZipFile(me)
    obj = thezip.open(internal_lib_path)
    print("{}".format(obj))
    return obj
    
        
# Need to get memfd_create(), which is now in the syscall table at 319
# Returns the FD number
def build_a_lib(lib_name, source_bytes):
    memfd_create = 319
    libc = CDLL("libc.so.6")
    print("Lib name is {}".format(lib_name))
    so_file_name = "{}.so".format(lib_name)
    fd = libc.syscall(memfd_create, so_file_name, 0)
    for data in source_bytes:
        os.write(fd, data)
    CDLL("/proc/self/fd/{}".format(fd))
    return fd


def link_a_lib(lib_name, pid, fdnum):
    target_dir = "/tmp/python-{}".format(pid)
    target_lib = "{}/{}".format(target_dir, lib_name)
    try:
        os.mkdir(target_dir)
    except OSError as oe:
        if oe[0] == 17:  # File exists
            pass  # Assume we're building our second 
        else:
            raise
    os.symlink("/proc/{}/fd/{}".format(pid, fdnum),
               target_lib)
    sys.path.append(target_dir)
    
    
import code;
code.interact(local=locals())

# See the README.md for usage
