#####################
nested_dict
#####################

.. automodule:: nested_dict

**************************
nested_dict
**************************
.. class:: nested_dict
    
    .. method:: nested_dict.__init__([nested_level, value_type])
    
        :param nested_level: the level of nestedness in the dictionary
        :param collection_type: the type of the values held in the dictionary
       
        For example,::
        
            a = nested_dict(3, list)
            a['level 1']['level 2']['level 3'].append(1)
            
            b = nested_dict(2, int)
            b['level 1']['level 2']+=3
            
        If nested_level and value_type are not defined, the degree of nested-ness is not
        fixed. For example,::
        
            a = nested_dict()
            a['1']['2']['3'] = 3
            a['A']['B'] = 15
        
    .. method:: iteritems_flat()

        iterate through values with nested keys flattened into a tuple

        For example,::
        
            from nested_dict import nested_dict
            a = nested_dict()
            a['1']['2']['3'] = 3
            a['A']['B'] = 15
            
            print list(a.iteritems_flat())
            
        Produces::
        
            [       (('1', '2', '3'),   3), 
                    (('A', 'B'),        15)
            ]

    .. method:: iterkeys_flat()
    
        iterate through values with nested keys flattened into a tuple
        
        For example,::
        
            from nested_dict import nested_dict
            a = nested_dict()
            a['1']['2']['3'] = 3
            a['A']['B'] = 15
            
            print list(a.iterkeys_flat())
            
        Produces::
        
            [('1', '2', '3'), ('A', 'B')]


    .. method:: itervalues_flat()
    
        iterate through values as a single list, without considering the degree of nesting

        For example,::
        
            from nested_dict import nested_dict
            a = nested_dict()
            a['1']['2']['3'] = 3
            a['A']['B'] = 15
            
            print list(a.itervalues_flat())
            
        Produces::
        
            [3, 15]


    .. method:: to_dict()

        Converts the nested dictionary to a nested series of standard ``dict`` objects

        For example,::
        
            from nested_dict import nested_dict
            a = nested_dict()
            a['1']['2']['3'] = 3
            a['A']['B'] = 15
            
            print a.to_dict()
            
        Produces::
            {'1': {'2': {'3': 3}}, 'A': {'B': 15}}

    .. method:: __str__([indent])
    
        The dictionary formatted as a string
        
        :param indent: The level of indentation for each nested level

        For example,::
        
            from nested_dict import nested_dict
            a = nested_dict()
            a['1']['2']['3'] = 3
            a['A']['B'] = 15
            
            print a
            print a.__str__(4)
            
        Produces::

            {"1": {"2": {"3": 3}}, "A": {"B": 15}}
            {
                "1": {
                    "2": {
                        "3": 3
                    }
                },
                "A": {
                    "B": 15
                }
            }            
            
**************************
Acknowledgements
**************************

    Inspired in part from ideas in:
    http://stackoverflow.com/questions/635483/what-is-the-best-way-to-implement-nested-dictionaries-in-python
    contributed by nosklo
    
    Many thanks

**************************
Copyright
**************************
    The code is licensed under the Boost Software License
    http://www.boost.org/LICENSE_1_0.txt
    
    This essentially only asks that the copyright notices in this code be maintained
    for **source** distributions.


