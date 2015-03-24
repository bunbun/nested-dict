# nested\_dict #
is a python library which extends collections.defaultdict to allow dictionaries with multiple levels of nesting to be created on the fly:
```
    from nested_dict import *

    nd = nested_dict()

    nd["a"]["b"]["c"] = 311                      
    nd["d"]["e"] = 311                      
```

Each nested level is create magically when accessed, a process known as “auto-vivification” in perl.

# Documentation #
is available [on google code](http://nested-dict.googlecode.com/hg/doc/build/html/index.html) or at http://wwwfgu.anat.ox.ac.uk/~lg/oss/nested_dict/
# Installation #

Run
```
    easy_install -U nested_dict
```

or download source and run
```
    ./setup.py install
```
