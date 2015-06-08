#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
"""
`nested_dict` provides dictionaries with multiple levels of nested-ness:
"""

################################################################################
#
#   nested_dict.py
#
#   Copyright (c) 2009, 2015 Leo Goodstadt
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#
#################################################################################


from collections import defaultdict

import sys
def flatten_nested_items(dictionary):
    """
    iterate through nested dictionary (with iterkeys() method)
         and return with nested keys flattened into a tuple
    """
    if sys.hexversion < 0x03000000:
        keys = dictionary.iterkeys
        keystr = "iterkeys"
    else:
        keys = dictionary.keys
        keystr = "keys"
    for key in keys():
        value = dictionary[key]
        if hasattr(value, keystr):
            for keykey, value in flatten_nested_items(value):
                yield (key,) + keykey, value
        else:
            yield (key,), value


class _recursive_dict(defaultdict):
    """
    Parent class of nested_dict. Defined separately for _nested_levels to work
    transparently, so dictionaries with a specified (and constant) degree of nestedness
    can be created easily.

    The "_flat" functions are defined here rather than in nested_dict because they work
        recursively.

    """
    def iteritems_flat(self):
        """
        iterate through values with nested keys flattened into a tuple
        """

        for key, value in flatten_nested_items(self):
            yield key, value

    def iterkeys_flat(self):
        """
        iterate through values with nested keys flattened into a tuple
        """
        for key, value in flatten_nested_items(self):
            yield key

    def itervalues_flat(self):
        """
        iterate through values with nested keys flattened into a tuple
        """
        for key, value in flatten_nested_items(self):
            yield value

    items_flat = iteritems_flat
    keys_flat = iterkeys_flat
    values_flat = itervalues_flat



    def to_dict(self, input_dict=None):
        """
        Converts the nested dictionary to a nested series of standard ``dict`` objects
        """
        #
        # Calls itself recursively to unwind the dictionary.
        # Use to_dict() to start at the top level of nesting
        plain_dict = dict()
        if input_dict is None:
            input_dict = self
        for key in input_dict.keys():
            value = input_dict[key]
            if isinstance(value, _recursive_dict):
                # print "recurse", value
                plain_dict[key] = self.to_dict(value)
            else:
                # print "plain", value
                plain_dict[key] = value
        return plain_dict

    def __str__(self, indent=None):
        """
        string version of self
        """
        import json
        return json.dumps(self.to_dict(), indent=indent)


class any_type(object):
    pass


def _nested_levels(level, nested_type):
    """
    Helper function to create a specified degree of nested dictionaries
    """
    if level > 2:
        return lambda: _recursive_dict(_nested_levels(level - 1,  nested_type))
    if level == 2:
        if isinstance(nested_type, any_type):
            return lambda: _recursive_dict()
        else:
            return lambda: _recursive_dict(_nested_levels(level - 1,  nested_type))
    return nested_type


if sys.hexversion < 0x03000000:
    iteritems = dict.iteritems
else:
    iteritems = dict.items

# _________________________________________________________________________________________
#
#   nested_dict
#
# _________________________________________________________________________________________
def nested_dict_from_dict(orig_dict, nd):
    for key, value in iteritems(orig_dict):
        if isinstance(value, (dict,)):
            nd[key] = nested_dict_from_dict(value, nested_dict())
        else:
            nd[key] = value
    return nd

# _________________________________________________________________________________________
#
#   nested_dict
#
# _________________________________________________________________________________________
class nested_dict(_recursive_dict):
    def __init__(self, *param):
        """
        Takes one or two parameters
            1) int, [TYPE]
            1) dict
        """
        if not len(param):
            defaultdict.__init__(self, nested_dict)
            return

        if len(param) == 1:
            # int = level
            if isinstance(param[0], int):
                defaultdict.__init__(self, _nested_levels(param[0], any_type()))
                return
            # existing dict
            if isinstance(param[0], dict):
                defaultdict.__init__(self, nested_dict)
                nested_dict_from_dict(param[0], self)
                return

        if len(param) == 2:
            if isinstance(param[0], int):
                defaultdict.__init__(self, _nested_levels(*param))
                return

        raise Exception("nested_dict should be initialised with either "
                        "1) the number of nested levels and an optional type, or "
                        "2) an existing dict to be converted into a nested dict.")
