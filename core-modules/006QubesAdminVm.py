#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# The Qubes OS Project, http://www.qubes-os.org
#
# Copyright (C) 2010  Joanna Rutkowska <joanna@invisiblethingslab.com>
# Copyright (C) 2013  Marek Marczykowski <marmarek@invisiblethingslab.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#

from qubes.qubes import QubesNetVm,register_qubes_vm_class
from qubes.qubes import defaults
from qubes.qubes import QubesException,dry_run,vmm
import psutil

class QubesAdminVm(QubesNetVm):

    # In which order load this VM type from qubes.xml
    load_order = 10

    def get_attrs_config(self):
        attrs = super(QubesAdminVm, self).get_attrs_config()
        attrs.pop('kernel')
        attrs.pop('kernels_dir')
        attrs.pop('kernelopts')
        attrs.pop('uses_default_kernel')
        attrs.pop('uses_default_kernelopts')
        return attrs

    def __init__(self, **kwargs):
        super(QubesAdminVm, self).__init__(qid=0, name="dom0", netid=0,
                                             dir_path=None,
                                             private_img = None,
                                             template = None,
                                             maxmem = 0,
                                             vcpus = 0,
                                             label = defaults["template_label"],
                                             **kwargs)

    @property
    def xid(self):
        return 0

    @property
    def libvirt_domain(self):
        raise ValueError("Dom0 do not have libvirt object")

    @property
    def type(self):
        return "AdminVM"

    def is_running(self):
        return True

    def get_power_state(self):
        return "Running"

    def get_mem(self):
        return psutil.virtual_memory().total/1024

    def get_mem_static_max(self):
        return vmm.libvirt_conn.getInfo()[1]

    def get_cputime(self):
        # TODO: measure it somehow
        return 0

    def get_disk_usage(self, file_or_dir):
        return 0

    def get_disk_utilization(self):
        return 0

    def get_disk_utilization_private_img(self):
        return 0

    def get_private_img_sz(self):
        return 0

    @property
    def ip(self):
        return "10.137.0.2"

    def start(self, **kwargs):
        raise QubesException ("Cannot start Dom0 fake domain!")

    def suspend(self):
        return

    def verify_files(self):
        return True

register_qubes_vm_class(QubesAdminVm)
