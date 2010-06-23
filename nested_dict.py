#!/usr/bin/env python
"""
***************************************
nested dictionaries
***************************************
    **nested_dict** extends `collections.defaultdict <http://docs.python.org/library/collections.html#defaultdict-objects>`_
    to allow dictionaries with multiple levels of nesting to be created on the fly::


        from nested_dict import *

        nd = nested_dict()

        nd["a"]["b"]["c"] = 311
        nd["d"]["e"] = 311

    Each nested level is create magically when accessed, a process known as
    `"auto-vivification" <http://en.wikipedia.org/wiki/Autovivification>`_ in perl.


******************************************************************************
nested dictionaries of sets / lists and other collections
******************************************************************************
    **nested_dict** also extends `defaultdict <http://docs.python.org/library/collections.html#defaultdict-objects>`_
    to allow dictionaries of lists, sets or other collections with a specified level of nesting level.


======================================================================================================================================================
    1) `dict.setdefault <http://docs.python.org/library/stdtypes.html#dict.setdefault>`_: The old-fashioned, ugly way
======================================================================================================================================================
    ::

        d = dict()

        d.setdefault(""1st group", []).append(3)
        d.setdefault(""2nd group", []).append(5)
        d.setdefault(""2nd group", []).append(8)
        d.setdefault(""1st group", []).append(4)
        d.setdefault(""2nd group", []).append(5)

========================================================================================================================================================================================================
    2) `defaultdict <http://docs.python.org/library/collections.html#defaultdict-objects>`_ adds `list <http://docs.python.org/library/stdtypes.html#typesseq>`_\ s automatically when required
========================================================================================================================================================================================================
    ::

        from collections import defaultdict

        dd = defaultdict(list)

        dd["1st group"].append(3)
        dd["2nd group"].append(5)
        dd["2nd group"].append(8)
        dd["1st group"].append(4)
        dd["2nd group"].append(5)

========================================================================================================================================================================================================
    3) ``nested_dict`` adds `list <http://docs.python.org/library/stdtypes.html#typesseq>`_\ s automatically when required for nested dictionaries
========================================================================================================================================================================================================
    ::

        from nested_dict import nested_dict

        # specify two levels of nesting
        nd = nested_dict(2, list)

        nd["1st group"]["subset a"].append(3)
        nd["2nd group"]["subset a"].append(5)
        nd["2nd group"]["subset b"].append(8)
        nd["1st group"]["subset a"].append(4)
        nd["2nd group"]["subset b"].append(5)

        print nd

    gives::

            {'1st group': {'subset a': [3, 4]},
             '2nd group': {'subset b': [8, 5],
                           'subset a': [5]}}


*********************************
More examples:
*********************************

==================================
    "Auto-vivifying" nested dict
==================================
        ::

            nd= nested_dict()
            nd["mouse"]["chr1"]["+"] = 311
            nd["mouse"]["chromosomes"]="completed"
            nd["mouse"]["chr2"] = "2nd longest"
            nd["mouse"]["chr3"] = "3rd longest"

            for k, v in nd.iteritems_flat():
                 print "%-30s=-%20s" % (k,v)

        Gives
            ::

                ('mouse', 'chr3')             =-         3rd longest
                ('mouse', 'chromosomes')      =-           completed
                ('mouse', 'chr2')             =-         2nd longest
                ('mouse', 'chr1', '+')        =-                 311

====================================================================
    Specifying the autovivified object
====================================================================
    If you wish the nested dictionary to hold a collection rather than a scalar,
    you have to write::

            nd["mouse"]["chr2"] = list()
            nd["mouse"]["chr2"].append(12)

    or::

            nd["mouse"]["chr2"] = set()
            nd["mouse"]["chr2"].add(84)

    Which doesn't seem very "auto" at all!

    Instead, specify the collection in the constructor of **nested_dict**::

        # two levels of nesting
        nd2 = nested_dict(2, list)
        nd2["mouse"]["chr2"].append(12)

        # three levels of nesting
        nd3 = nested_dict(3, set)
        nd3["mouse"]["chr2"]["categorised"].add(3)

        # counts
        nd4 = nested_dict(2, int)
        nd4["mouse"]["chr2"]+=4
        nd4["human"]["chr1"]+=3
        nd4["human"]["chr3"]+=4

"""

# This code is copyright (c) 2009 Leo Goodstadt
# All rights reserved.
#
# Boost Software License - Version 1.0 - August 17th, 2003
#
#
# Permission is hereby granted, free of charge, to any person or organization
# obtaining a copy of the software and accompanying documentation covered by
# this license (the "Software") to use, reproduce, display, distribute,
# execute, and transmit the Software, and to prepare derivative works of the
# Software, and to permit third-parties to whom the Software is furnished to
# do so, all subject to the following:
#
# The copyright notices in the Software and this entire statement, including
# the above license grant, this restriction and the following disclaimer,
# must be included in all copies of the Software, in whole or in part, and
# all derivative works of the Software, unless such copies or derivative
# works are solely in the form of machine-executable object code generated by
# a source language processor.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
# SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
# FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

nested_dict_version = "1.0.8"
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
        for key, value in self.iteritems():
            #if "<class '__main__._recursive_dict'>" == str(value.__class__):
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

    def to_dict (self, input_dict = None):
        """
        Converts the nested dictionary to a nested series of standard ``dict`` objects
        """
        #
        # Calls itself recursively to unwind the dictionary.
        # Use to_dict() to start at the top level of nesting
        plain_dict = dict()
        if input_dict == None:
            input_dict = self
        for key, value in input_dict.iteritems():
            if isinstance(value, _recursive_dict):
                #print "recurse", value
                plain_dict[key] = self.to_dict(value)
            else:
                #print "plain", value
                plain_dict[key] = value
        return plain_dict

    def __str__ (self, indent = None):
        """
        string version of self
        """
        import json
        return json.dumps(self.to_dict(), indent = indent)


def _nested_levels (level, nested_type):
    """
    Helper function to create a specified degree of nested dictionaries
    """
    if level > 1:
        return lambda: _recursive_dict(_nested_levels(level - 1,  nested_type))
    return nested_type

#_________________________________________________________________________________________
#
#   nested_dict
#
#_________________________________________________________________________________________
class nested_dict(_recursive_dict):
    def __init__(self, *param):
        """
        If parameters
        """
        if not len(param):
            defaultdict.__init__(self, nested_dict)
        else:
            if len(param) == 2:
                level, nested_type = param
                defaultdict.__init__(self, _nested_levels(level, nested_type))
            else:
                Exception(  "nested_dict should be initialised with the number of nested "
                            "levels and the type held in the nested_dict")






import unittest, os,sys
if __name__ == '__main__':
    exe_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    sys.path.append(os.path.abspath(os.path.join(exe_path,"..", "python_modules")))
    import json

if __name__ == '__main__':
    class test_nested_dict_default(unittest.TestCase):

        #       self.assertEqual(self.seq, range(10))
        #       self.assert_(element in self.seq)
        #       self.assertRaises(ValueError, random.sample, self.seq, 20)



        def test_default(self):
            """
                test a range of nested_dict
            """
            nd = nested_dict()
            nd['new jersey']['mercer county']['plumbers'] = 3
            nd['new jersey']['mercer county']['programmers'] = 81
            nd['new jersey']['middlesex county']['programmers'] = 81
            nd['new jersey']['middlesex county']['salesmen'] = 62
            nd['new york']['queens county']['plumbers'] = 9
            nd['new york']['queens county']['salesmen'] = 36
            all = [tup for tup in nd.iteritems_flat()]
            self.assertEqual(all, [
                                    (('new jersey', 'mercer county', 'programmers'   )   , 81)   ,
                                    (('new jersey', 'mercer county', 'plumbers'      )   , 3)       ,
                                    (('new jersey', 'middlesex county', 'programmers')   , 81),
                                    (('new jersey', 'middlesex county', 'salesmen'   )   , 62)   ,
                                    (('new york', 'queens county', 'salesmen'        )   , 36)        ,
                                    (('new york', 'queens county', 'plumbers'        )   , 9)])

    class test_nested_dict_list(unittest.TestCase):
        def test_list(self):
            """
                test a range of nested_dict
            """
            nd = nested_dict(2, list)
            nd['new jersey']['mercer county'].append('plumbers')
            nd['new jersey']['mercer county'].append('programmers')
            nd['new jersey']['middlesex county'].append('salesmen')
            nd['new jersey']['middlesex county'].append('staff')
            nd['new york']['queens county'].append('cricketers')
            all = [tup for tup in nd.iteritems_flat()]
            print >>sys.stderr, all
            self.assertEqual(all,
                                  [
                                   (('new jersey', 'mercer county'),            ['plumbers', 'programmers']),
                                   (('new jersey', 'middlesex county'),         ['salesmen', 'staff']),
                                   (('new york', 'queens county'),              ['cricketers']),
                                   ])
            all = [tup for tup in nd.itervalues_flat()]
            self.assertEqual(all,
                                  [
                                   ['plumbers', 'programmers'],
                                   ['salesmen', 'staff'],
                                   ['cricketers'],
                                   ])
            all = [tup for tup in nd.iterkeys_flat()]
            self.assertEqual(all,
                                  [
                                      ('new jersey', 'mercer county'),
                                      ('new jersey', 'middlesex county'),
                                      ('new york', 'queens county'),
                                   ])

            self.assertEqual(nd,{   "new jersey": {
                                        "mercer county": [
                                            "plumbers",
                                            "programmers"
                                        ],
                                        "middlesex county": [
                                            "salesmen",
                                            "staff"
                                        ]
                                    },
                                    "new york": {
                                        "queens county": [
                                            "cricketers"
                                        ]
                                    }
                                })

#
#   debug code not run if called as a module
#
if __name__ == '__main__':
    if "--debug" in sys.argv:
        sys.argv.remove("--debug")
    sys.argv.append("--verbose")
    #sys.argv.append("test_nested_dict_list")

    unittest.main()


