
##############################################################################
Introduction
##############################################################################
`nested_dict` provides dictionaries with multiple levels of nested-ness:

    .. <<Python

    .. code-block:: Python

        from nested_dict import *

        nd = nested_dict()

        nd["a"]["b"]["c"] = 311
        nd["d"]["e"] = 311

    ..
        Python


Each nested level is created magically when accessed, a process known as "auto-vivification" in perl.

******************************************************************************
Working without `nested_dict`
******************************************************************************

`defaultdict  <https://docs.python.org/2/library/collections.html#collections.defaultdict>`__ from the python `collections  <https://docs.python.org/2/library/collections.html>`__ module provides for one or (with some effort) two levels of nestedness
For example, here is a dictionary of `set  <https://docs.python.org/2/library/sets.html>`__\ s with `defaultdict  <https://docs.python.org/2/library/collections.html#collections.defaultdict>`__ :

For one level of nesting:

    .. <<Python

    .. code-block:: Python

        from collections import defaultdict
        one_level_dict = defaultdict(set)
        one_level_dict["1st group"].add(3)
        one_level_dict["2nd group"].add(4)
        one_level_dict["2nd group"].add(5)

    ..
        Python

For two levels of nesting:

    .. <<Python

    .. code-block:: Python

        from collections import defaultdict
        two_level_dict = defaultdict(lambda: defaultdict(set))
        two_level_dict["1st group"]["A"].add(3)
        two_level_dict["2nd group"]["B"].add(4)
        two_level_dict["2nd group"]["C"].add(5)

    ..
        Python


However, the syntax becomes rapidly more ugly with additional levels of nesting, and it is difficult to mix dictionaries with different levels of nestedness.

##############################################################################
How to use `nested_dict`
##############################################################################

******************************************************************************
Flexible levels of nesting
******************************************************************************

  .. <<Python

  .. code-block:: Python

    from nested_dict import nested_dict
    nd= nested_dict()
    nd["mouse"]["chr1"]["+"] = 311
    nd["mouse"]["chromosomes"]["Y"]["Male"] = True
    nd["mouse"]["chr2"] = "2nd longest"
    nd["mouse"]["chr3"] = "3rd longest"

    for k, v in nd.items_flat():
        print "%-50s==%20r" % (k,v)

  ..
      Python


Gives:

    .. <<Python

    .. code-block:: Python

        ('mouse', 'chr3')                                 ==       '3rd longest'
        ('mouse', 'chromosomes', 'Y', 'Male')             ==                True
        ('mouse', 'chr2')                                 ==       '2nd longest'
        ('mouse', 'chr1', '+')                            ==                 311

    ..
        Python


******************************************************************************
Fixed levels of nesting and set types
******************************************************************************

This is necessary if you want the nested dictionary to hold a collection (like the `set  <https://docs.python.org/2/library/sets.html>`__ in the first example) or scalar such as `int` or `str` with useful default values.

.. <<Python

.. code-block:: Python

        #   nested dict of lists
        nd = nested_dict(2, list)
        nd["mouse"]["2"].append(12)
        nd["human"]["1"].append(12)

        #   nested dict of sets
        nd = nested_dict(2, set)
        nd["mouse"]["2"].add("a")
        nd["human"]["1"].add("b")

        #   nested dict of ints
        nd = nested_dict(2, int)
        nd["mouse"]["2"] += 4
        nd["human"]["1"] += 5
        nd["human"]["1"] += 6

        nd.to_dict()
        #{'human': {'1': 11}, 'mouse': {'2': 4}}


        #   nested dict of strings
        nd = nested_dict(2, str)
        nd["mouse"]["2"] += "a" * 4
        nd["human"]["1"] += "b" * 5
        nd["human"]["1"] += "c" * 6

        nd.to_dict()
        #{'human': {'1': 'bbbbbcccccc'}, 'mouse': {'2': 'aaaa'}}

..
    Python



******************************************************************************
Set maximum nesting
******************************************************************************
You can also specify a maximum level of nesting even if you do not want to specify the stored type.
For example, if you know beforehand that your data involves a **maximum** of four nested sub levels, you can add this (very minimal) constraint ahead of time:

.. <<Python

.. code-block:: Python

    nd4 = nested_dict(4)
    # OK: Assign to "string"
    nd4[1][2][3][4]="a"

    # Bad: Five levels is one too many
    nd4[1][2][3]["four"][5]="b"
    #
    # KeyError
    # ----> nd4[1][2][3]["four"][5]="b"
    #
    # KeyError: 'four'
    #


    # OK: Assign to fewer levels is fine
    nd4[1]["two"] = 3

    # But like with normal dicts, you can't "extend a value" later
    nd4[1]["two"][4] = 3

    # TypeError
    # ----> nd4[1]["two"][4] = 3
    #
    # TypeError: 'int' object does not support item assignment

..
    Python


##############################################################################
Iterating `nested_dict()`
##############################################################################


You can use nested iterators to iterate through `nested_dict` just like ordinary python `dict  <https://docs.python.org/2/library/stdtypes.html#typesmapping>`__\ s

    .. <<Python

    .. code-block:: Python

        from nested_dict import nested_dict
        nd= nested_dict()
        nd["mouse"]["chr1"]["+"] = 311
        nd["mouse"]["chromosomes"]="completed"
        nd["mouse"]["chr2"] = "2nd longest"
        nd["mouse"]["chr3"] = "3rd longest"

        for key1, value1 in nd.items():
            for key2, value2 in value1.items():
                print (key1, key2, str(value2))

        #   ('mouse', 'chr3', '3rd longest')
        #   ('mouse', 'chromosomes', 'completed')
        #   ('mouse', 'chr2', '2nd longest')
        #   ('mouse', 'chr1', '{"+": 311}')

    ..
        Python


This is less useful if you do not know beforehand how many levels of nesting you have.

Instead, you can use ``items_flat()``\ , ``keys_flat()``\ , and ``values_flat()``\ . 
(``iteritems_flat()``\ , ``iterkeys_flat()``\ , and ``itervalues_flat()`` are python2.7 style synonyms. )
The `_flat()` functions are just like their normal counterparts except they compress all the nested 
keys into `tuple  <https://docs.python.org/2/library/functions.html#tuple>`__\ s:


    .. <<Python

    .. code-block:: Python

        from nested_dict import nested_dict
        nd= nested_dict()
        nd["mouse"]["chr1"]["+"] = 311
        nd["mouse"]["chromosomes"]="completed"
        nd["mouse"]["chr2"] = "2nd longest"
        nd["mouse"]["chr3"] = "3rd longest"

        for keys_as_tuple, value in nd.items_flat():
            print ("%-30s == %20r" % (keys_as_tuple, value))
        #   ('mouse', 'chr3')              ==        '3rd longest'
        #   ('mouse', 'chromosomes')       ==          'completed'
        #   ('mouse', 'chr2')              ==        '2nd longest'
        #   ('mouse', 'chr1', '+')         ==                  311

    ..
        Python


##############################################################################
Converting back to dictionaries
##############################################################################


It is often useful to convert away the magic of `nested_dict`, for example, to `pickle  <https://docs.python.org/2/library/pickle.html>`__ the dictionary.

Use `nested_dict.to_dict()`


    .. <<Python

    .. code-block:: Python

        from nested_dict import nested_dict
        nd= nested_dict()
        nd["mouse"]["chr1"]["+"] = 311
        nd["mouse"]["chromosomes"]="completed"
        nd.to_dict()
        # {'mouse': {'chr1': {'+': 311}, 'chromosomes': 'completed'}}

    ..
        Python


.. toctree::
   :titlesonly:
   :name: class documentation

   nested_dict.rst
