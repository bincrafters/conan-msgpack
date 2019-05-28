#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
from conans import tools
import os

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=True)

    if tools.os_info.is_linux and os.getenv("HEADER_ONLY", False) == "1":
        builder.add({}, {"msgpack:header_only" : True}, {}, {})

    builder.run()