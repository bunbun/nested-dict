#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

import sys, os
if not sys.version_info[0:2] >= (2,5):
    sys.stderr.write("Requires Python later than 2.5\n")
    sys.exit(1)
    
# quickly import the latest version of nested_dict
sys.path.insert(0, os.path.abspath(os.path.join("src")))
import nested_dict
sys.path.pop(0)
    
    
if sys.version_info[0:2] >= (2,5):
    module_dependencies = []
else:
    module_dependencies = []


from setuptools import setup, find_packages
setup(
        name='nested_dict',
        version=nested_dict.nested_dict_version, #major.minor[.patch[.sub]]
        description='Defaultdict extension for dictionaries with multiple levels of nesting',
        long_description=\
"""     
(Documentation hosted at http://wwwfgu.anat.ox.ac.uk/~lg/oss/nested_dict .)
    
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
    **nested_dict** also extends `collections.defaultdict <http://docs.python.org/library/collections.html#defaultdict-objects>`_ 
    to allow dictionaries of lists, sets or other collections with a specified level of nesting level.
    
        
==================================================
    1) The old fashioned way using ugly syntax
==================================================
    ::

        d = dict()
        
        d.setdefault(""1st group", []).append(3)
        d.setdefault(""2nd group", []).append(5)
        d.setdefault(""2nd group", []).append(8)
        d.setdefault(""1st group", []).append(4)
        d.setdefault(""2nd group", []).append(5)
        
====================================================================================================
    2) ``default_dict`` adds ``list``\ s automatically when required
====================================================================================================    
    ::
    
        from collections import defaultdict

        dd = defaultdict(list)

        dd["1st group"].append(3)
        dd["2nd group"].append(5)
        dd["2nd group"].append(8)
        dd["1st group"].append(4)
        dd["2nd group"].append(5)
    
====================================================================================================
    3) ``nested_dict`` adds ``list``\ s automatically when required for nested dictionaries
====================================================================================================        
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

""",
        author='Leo Goodstadt',
        author_email='pypi@llew.org.uk',
        #url='http://ruffus.googlecode.com',
        #download_url = "http://http://code.google.com/p/ruffus/download",
    
        #install_requires = module_dependencies, #['multiprocessing>=1.0', 'json' ], #, 'python>=2.5'],
        #setup_requires   = module_dependencies, #['multiprocessing>=1.0', 'json'],    #, 'python>=2.5'],

        
        classifiers=[
                    'Intended Audience :: End Users/Desktop',
                    'Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved',
                    'Programming Language :: Python',
                    'Topic :: Scientific/Engineering',
                    'Topic :: Software Development :: Libraries',
                    ],
        license = "Boost",
        keywords = "make task pipeline parallel bioinformatics science",


        #packages = find_packages('src'),    # include all packages under src
        #package_dir = {'':'src'},           #packages are under src
        #packages=['nested_dict'],
        #package_dir={'': 'src'},
        py_modules = ['nested_dict'],

        include_package_data = True,    # include everything in source control
        #package_data = {
        #    # If any package contains *.txt files, include them:
        #    '': ['*.TXT'],                                \
        #}


     )

#setup.py
#   src/
#       nested_dict.py
#   doc/
#   CHANGES.txt
#   README.txt
#   USAGE.txt
#
#  http://pypi.python.org/pypi
#  http://docs.python.org/distutils/packageindex.html
#   
# 
# 
#   python setup.py register
# python setup.py sdist  upload --formats=gztar,zip
# python setup.py bdist --format=rpm,gztar,zip,wininst sdist --format=gztar,zip upload
# python setup.py sdist --format=gztar,zip upload
