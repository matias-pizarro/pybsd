# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from systems import Master, DummyMaster, Jail

mpizarro = DummyMaster('mpizarro')
mpizarro.ezjail_admin('list')
