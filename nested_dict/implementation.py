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
        #if sys.hexversion >= 0x03000000:

        for key in self:
            value = self[key]
            # if "<class '__main__._recursive_dict'>" == str(value.__class__):
            if isinstance(value, _recursive_dict):
                for keykey, value in value.iteritems_flat():
                    yield (key,) + keykey, value
            else:
                yield (key,), value

    def iterkeys_flat(self):
        """
        iterate through values with nested keys flattened into a tuple
        """
        for key, value in self.iteritems_flat():
            yield key

    def itervalues_flat(self):
        """
        iterate through values with nested keys flattened into a tuple
        """
        for key, value in self.iteritems_flat():
            yield value

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
        for key in sorted(input_dict.keys()):
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


# _________________________________________________________________________________________
#
#   nested_dict
#
# _________________________________________________________________________________________
class nested_dict(_recursive_dict):
    def __init__(self, *param):
        """
        If parameters
        """
        if not len(param):
            defaultdict.__init__(self, nested_dict)
        else:
            if len(param) in (1, 2):
                if len(param) == 2:
                    level, nested_type = param
                else:
                    level, nested_type = param[0], any_type()
                if not isinstance(level, int):
                    raise Exception("nested_dict should be initialised with the "
                                    "number of nested levels and (optionally) the "
                                    "type held in the nested_dict")
                defaultdict.__init__(self, _nested_levels(level, nested_type))
            else:
                raise Exception(  "nested_dict should be initialised with the number of "
                                  "nested levels and the type held in the nested_dict")
