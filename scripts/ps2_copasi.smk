
rule all:
    input:
        file="*.pdf"


rule preproc:
    input:
        file="Models/insulin_receptor.cps"
    output:
        file="preproc/insulin_receptor_1.cps"
    run:
        SBPIPE = os.environ["SBPIPE"]
        sys.path.insert(0, SBPIPE)
        from sbpipe.snakemake.preproc import copasi_preproc
        copasi_preproc(input.file, output.file)


rule gen_data:
    input:
        file="preproc/insulin_receptor_1.cps"
    output:
        file="preproc/insulin_receptor_1.csv"
    run:
        SBPIPE = os.environ["SBPIPE"]
        sys.path.insert(0, SBPIPE)
        from sbpipe.snakemake.generate_data import run_copasi_model
        print(input.file)
        run_copasi_model(input.file)


rule ps2_postproc:
    input:
        file="preproc/insulin_receptor_1.csv"
    output:
        file="postproc/insulin_receptor_1.csv"
    run:
        SBPIPE = os.environ["SBPIPE"]
        sys.path.insert(0, SBPIPE)
        from sbpipe.snakemake.ps2_postproc import generic_postproc
        generic_postproc(input.file, output.file, 10)


rule ps2_analysis:
    input:
        file="postproc/insulin_receptor_1.csv"
    output:
        file="plots/insulin_receptor_1__tp_1.png"
    shell:
        "Rscript --vanilla /home/pdp/local_software/sbpipe/sbpipe/snakemake/ps2_analysis.r insulin_receptor "
        "InsulinPercent IRbetaPercent postproc plots 10"


rule ps2_latex_report:
    input:
        file="plots/insulin_receptor_1__tp_1.png",
        outputdir='',
        sim_plots_folder='plots',
        filename_prefix='',
        model_noext='insulin_receptor',
        scanned_par1='InsulinPercent',
        scanned_par2='IRbetaPercent'
    output:
        file="*.pdf"
    run:
        SBPIPE = os.environ["SBPIPE"]
        sys.path.insert(0, SBPIPE)
        from sbpipe.report.latex_reports import latex_report_ps2
        latex_report_ps2({input.outputdir}, {input.sim_plots_folder}, {input.filename_prefix}, {input.model_noext},
                     {input.scanned_par1}, {input.scanned_par2})