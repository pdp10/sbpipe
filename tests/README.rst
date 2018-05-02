To run these tests, the Python package `nose` is required.

::

    # run a simple model simulation using Copasi
    nosetests test_copasi_sim.py --verbose


Test suites:

::

    # run SBpipe test suite:
    nosetests test_suite.py --verbose

    # reproduce the figures in Dalle Pezze and Le Novère, 2017, BMC Systems Biology:
    nosetests test_suite_manuscript.py --verbose

    # run SBpipe tests suite specifically on cluster:
    nosetests test_suite_sge_lsf_clusters.py --verbose

    # run Snakemake workflows for SBpipe:
    nosetests test_suite_snakemake.py --verbose

