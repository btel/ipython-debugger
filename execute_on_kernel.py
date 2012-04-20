#!/usr/bin/env python
#coding=utf-8
"""Executes expression on kernel using ZMQ messaging. Requires the
security file to start connection to an exisiting kernel (in
.ipython/profile_default/security/kernel-*.json).

How to run:
-----------
1. Run ipython kernel. Kernel is started automatically when running
   notebook or qtconsole.

   For example:
       
       > ipython qtconsole

2. Copy the name of kernel security file.
  
   The name of this file is printed to stdout when running ipython.
   For example, the previous command should have printed:

       [IPKernelApp] To connect another client to this kernel, use:
       [IPKernelApp] --existing kernel-52706.json
   
   kernel-XXXX.json is what we are looking for (the name may slightly
   differ for notebook interface).

3. Run this script with the security file as an argument.

   The security file is normally located in the 
   $HOME/.ipython/profile_default/secruity directory. Therefore you
   should run this script via:

       > python execute_on_kernel.py $HOME/.ipython/profile_default/secruity/kernel-XXXX.json

    Where kernel-XXXX.json is the file name of the previous step.

4. Check whether the expression was executed in the ipyhton fronted
  (see `expr` variable below).

   In [1]: print my_funny_variable
   Out[1]: 1 

Links:
------

    websockets: http://www.artima.com/weblogs/viewpost.jsp?thread=339100
    ZeroMQ: http://www.zeromq.org/intro:read-the-manual
    Messaging in IPython: http://ipython.org/ipython-doc/rel-0.12/development/messaging.html#messaging

"""

expr = "my_funny_variable = 1"

import json
from IPython.zmq import session
import zmq

import sys
_, kernel_conf = sys.argv
with open(kernel_conf) as f:
    kernel_data = json.load(f)

print kernel_data
key = kernel_data['key']
url = "tcp://{ip}:{shell_port}".format(**kernel_data)

zmq.DEALER = zmq.XREQ

c = zmq.Context()
request_socket = c.socket(zmq.DEALER)
request_socket.connect(url)

sess = session.Session(key=key)

msg_content = dict(code=expr, 
                   silent=False, 
                   user_variables=[], 
                   user_expressions={})

sess.send(request_socket, 'execute_request',msg_content)


