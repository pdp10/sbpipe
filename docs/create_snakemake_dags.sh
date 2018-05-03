#!/usr/bin/env bash
#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


SNAKEMAKE_FOLDER="../tests/snakemake"

git clone http://github.com/pdp10/sbpipe_snake.git
mv sbpipe_snake/*.snake ${SNAKEMAKE_FOLDER}
rm -rf sbpipe_snake

cd ${SNAKEMAKE_FOLDER}

# PDF
snakemake -s sbpipe_pe.snake --configfile ir_model_param_estim_for_dag.yaml --dag | dot -Tpdf > sbpipe_pe_snake_dag.pdf
snakemake -s sbpipe_sim.snake --configfile ir_model_stoch_simul.yaml --dag | dot -Tpdf > sbpipe_sim_snake_dag.pdf
snakemake -s sbpipe_ps1.snake --configfile ir_model_ir_beta_inhib_stoch.yaml --dag | dot -Tpdf > sbpipe_ps1_snake_dag.pdf
snakemake -s sbpipe_ps2.snake --configfile ir_model_insulin_ir_beta_dbl_stoch_inhib.yaml --dag | dot -Tpdf > sbpipe_ps2_snake_dag.pdf

# PNG
snakemake -s sbpipe_pe.snake --configfile ir_model_param_estim_for_dag.yaml --dag | dot -Tpng -Gdpi=300 > sbpipe_pe_snake_dag.png
snakemake -s sbpipe_sim.snake --configfile ir_model_stoch_simul.yaml --dag | dot -Tpng -Gdpi=300 > sbpipe_sim_snake_dag.png
snakemake -s sbpipe_ps1.snake --configfile ir_model_ir_beta_inhib_stoch.yaml --dag | dot -Tpng -Gdpi=300 > sbpipe_ps1_snake_dag.png
snakemake -s sbpipe_ps2.snake --configfile ir_model_insulin_ir_beta_dbl_stoch_inhib.yaml --dag | dot -Tpng -Gdpi=300 > sbpipe_ps2_snake_dag.png


rm -f ${SNAKEMAKE_FOLDER}/*.snake

cd -

# moves pdf files
mv ${SNAKEMAKE_FOLDER}/*.pdf images/

# moves png files
mv ${SNAKEMAKE_FOLDER}/*.png images/
