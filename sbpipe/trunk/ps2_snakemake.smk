
rule make_preproc_dir


rule preproc:
    input:
        dir="Models/",
        model="Models/insulin_receptor.cps"
    output:
        dir="preproc"
    run:
        SBPIPE = os.environ["SBPIPE"]
        sys.path.insert(0, SBPIPE)
        from sbpipe.trunk.preproc import copasi_preproc
        copasi_preproc(input.dir, output.dir, os.path.basename(input.model), str(1))
