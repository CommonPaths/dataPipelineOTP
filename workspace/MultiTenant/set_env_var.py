#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "DXC Technology"
__copyright__ = "© 2020 DXC Technology Services Company, LLC"
################################################################################

import os
class Env:
    
    def get_env(self,key):
        return os.getenv(key)
