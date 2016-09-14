# Documentation auto-generation
In order to generate the complete documentation for sb_pipe, the following packages must be installed: 

- python-sphinx
- pandoc

Instruction for generating and cleaning sb_pipe documentation are provided below.

To generate the source code documentation:
```
$ ./gen_doc.sh
```

To clean the documentation:
```
$ ./clean_doc.sh
```

If new folders containing new Python modules are added, it is necessary to update the sys.path in *source/conf.py* to include these additional paths. 
