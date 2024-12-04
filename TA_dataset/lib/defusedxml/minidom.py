# -*- coding: utf-8 -*-
# defusedxml
#
# Copyright (c) 2013 by Christian Heimes <christian@python.org>
# Licensed to PSF under a Contributor Agreement.
# See https://www.python.org/psf/license for licensing details.
"""Defused xml.dom.minidom
"""
from __future__ import absolute_import, print_function

from xml.dom.minidom import _do_pulldom_parse

from . import expatbuilder as _expatbuilder
from . import pulldom as _pulldom

__origin__ = "xml.dom.minidom"


def parse(
    file,
    parser=None,
    bufsize=None,
    forbid_dtd=False,
    forbid_entities=True,
    forbid_external=True,
):
    """Parse a file into a DOM by filename or file object."""
    if parser is None and not bufsize:
        return _expatbuilder.parse(
            file,
            forbid_dtd=forbid_dtd,
            forbid_entities=forbid_entities,
            forbid_external=forbid_external,
        )
    else:
        return _do_pulldom_parse(
            _pulldom.parse,
            (file,),
            {
                "parser": parser,
                "bufsize": bufsize,
                "forbid_dtd": forbid_dtd,
                "forbid_entities": forbid_entities,
                "forbid_external": forbid_external,
            },
        )


def parseString(
    string, parser=None, forbid_dtd=False, forbid_entities=True, forbid_external=True
):
    """Parse a file into a DOM from a string."""
    if parser is None:
        return _expatbuilder.parseString(
            string,
            forbid_dtd=forbid_dtd,
            forbid_entities=forbid_entities,
            forbid_external=forbid_external,
        )
    else:
        return _do_pulldom_parse(
            _pulldom.parseString,
            (string,),
            {
                "parser": parser,
                "forbid_dtd": forbid_dtd,
                "forbid_entities": forbid_entities,
                "forbid_external": forbid_external,
            },
        )
