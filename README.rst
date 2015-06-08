.. note ::

    * Source code at https://github.com/bunbun/nested-dict
    * Documentation at http://nested-dict.readthedocs.org

##############################################################################
``nested_dict``
##############################################################################
``nested_dict`` extends ``defaultdict`` to support python ``dict`` with multiple levels of nested-ness:

*****************************************************************
Drop in replacement for ``dict``
*****************************************************************


  .. <<Python

  .. code-block:: Pycon

    >>> from nested_dict import nested_dict
    >>> nd= nested_dict()
    >>> nd["one"] = "1"
    >>> nd[1]["two"] = "1 / 2"
    >>> nd["uno"][2]["three"] = "1 / 2 / 3"
    >>>
    ... for keys_as_tuple, value in nd.items_flat():
    ...    print ("%-20s == %r" % (keys_as_tuple, value))
    ...
    ('one',)             == '1'
    (1, 'two')           == '1 / 2'
    ('uno', 2, 'three')  == '1 / 2 / 3'

  ..
      Python

    Each nested level is created magically when accessed, a process known as "auto-vivification" in perl.


******************************************************************************
Specifying the contained type
******************************************************************************

    If you want the nested dictionary to hold
        * a collection (like the `set  <https://docs.python.org/2/library/sets.html>`__ in the first example) or
        * a scalar with useful default values such as ``int`` or ``str``.

==============================
*dict* of ``list``\ s
==============================
    .. <<Python

    .. code-block:: Python

            #   nested dict of lists
            nd = nested_dict(2, list)
            nd["mouse"]["2"].append(12)
            nd["human"]["1"].append(12)


    ..
        Python

==============================
*dict* of ``set``\ s
==============================
    .. <<Python

    .. code-block:: Python

            #   nested dict of sets
            nd = nested_dict(2, set)
            nd["mouse"]["2"].add("a")
            nd["human"]["1"].add("b")


    ..
        Python

==============================
*dict* of ``int``\ s
==============================

    .. <<Python

    .. code-block:: Python

            #   nested dict of ints
            nd = nested_dict(2, int)
            nd["mouse"]["2"] += 4
            nd["human"]["1"] += 5
            nd["human"]["1"] += 6

            nd.to_dict()
            #{'human': {'1': 11}, 'mouse': {'2': 4}}


    ..
        Python

==============================
*dict* of ``str``\ s
==============================

    .. <<Python

    .. code-block:: Python

            #   nested dict of strings
            nd = nested_dict(2, str)
            nd["mouse"]["2"] += "a" * 4
            nd["human"]["1"] += "b" * 5
            nd["human"]["1"] += "c" * 6

            nd.to_dict()
            #{'human': {'1': 'bbbbbcccccc'}, 'mouse': {'2': 'aaaa'}}

    ..
        Python

##############################################################################
Iterating through ``nested_dict``
##############################################################################

Iterating through deep or unevenly nested dictionaries is a bit of a pain without recursion.
``nested dict`` allows you to **flatten** the nested levels into `tuple  <https://docs.python.org/2/library/functions.html#tuple>`__\ s before iteration.

You do not need to know beforehand how many levels of nesting you have:

    .. <<Python

    .. code-block:: Python

        from nested_dict import nested_dict
        nd= nested_dict()
        nd["one"] = "1"
        nd[1]["two"] = "1 / 2"
        nd["uno"][2]["three"] = "1 / 2 / 3"

        for keys_as_tuple, value in nd.items_flat():
            print ("%-20s == %r" % (keys_as_tuple, value))

        #   (1, 'two')           == '1 / 2'
        #   ('one',)             == '1'
        #   ('uno', 2, 'three')  == '1 / 2 / 3'

    ..
        Python



nested_dict provides
    * ``items_flat()``
    * ``keys_flat()``
    * ``values_flat()``

(``iteritems_flat()``, ``iterkeys_flat()``, and ``itervalues_flat()`` are python 2.7-style synonyms. )

##############################################################################
Converting to / from dictionaries
##############################################################################

The magic of  ``nested_dict`` sometimes gets in the way (of `pickle  <https://docs.python.org/2/library/pickle.html>`__\ ing for example).

We can convert to and from a vanilla python ``dict`` using
    * ``nested_dict.to_dict()``
    * ``nested_dict constructor``

    .. <<Python

    .. code-block:: Pycon

        >>> from nested_dict import nested_dict
        >>> nd= nested_dict()
        >>> nd["one"] = 1
        >>> nd[1]["two"] = "1 / 2"

        #
        #   convert nested_dict -> dict and pickle
        #
        >>> nd.to_dict()
        {1: {'two': '1 / 2'}, 'one': 1}
        >>> import pickle
        >>> binary_representation = pickle.dumps(nd.to_dict())

        #
        #   convert dict -> nested_dict
        #
        >>> normal_dict = pickle.loads(binary_representation)
        >>> new_nd = nested_dict(normal_dict)
        >>> nd == new_nd
        True

    ..
        Python


##############################################################################
``defaultdict``
##############################################################################
``nested_dict`` extends `collections.defaultdict  <https://docs.python.org/2/library/collections.html#collections.defaultdict>`__

You can get arbitrarily-nested "auto-vivifying" dictionaries using `defaultdict  <https://docs.python.org/2/library/collections.html#collections.defaultdict>`__.

    .. <<Python

    .. code-block:: Python

        from collections import defaultdict
        nested_dict = lambda: defaultdict(nested_dict)
        nd = nested_dict()
        nd[1][2]["three"][4] = 5
        nd["one"]["two"]["three"][4] = 5

    ..
        Python

However, only ``nested_dict`` supports a ``dict`` of ``dict`` of ``sets`` etc.

