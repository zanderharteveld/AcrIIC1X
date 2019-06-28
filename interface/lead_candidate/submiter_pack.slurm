#!/bin/bash
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --cpus-per-task 1
#SBATCH --mem 8000
#SBATCH --time 01:00:00

srun /scratch/hartevel/bin/Rosetta_acrIIa1/main/source/bin/rosetta_scripts.linuxiccrelease @flags_pack \
-s ../../in/acrIIc1_sauCas9hnh_motali.pdb \
-parser:protocol mutateinterface_lead_pack.xml \
-nstruct 5 \
-out:file:silent lead_triple_pack.silent \
-out:prefix lead_triple_pack_. \
-parser:script_vars variant=FQI
