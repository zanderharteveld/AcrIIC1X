#!/bin/bash
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --cpus-per-task 1
#SBATCH --mem 8000
#SBATCH --time 6:00:00
#SBATCH --array=1-200


ACPT="/home/upmeier/acrII1a_design/mcherry/in/acrIIc1.clean.pdb"
INS="/home/upmeier/acrII1a_design/mcherry/in/mCherry.clean.pdb"

VAR="AcrIIC1_Y70-GSG-mCherry-GSG-A71"
#VAR="AcrIIC1_Q69-mCherry-Y72"

mkdir -p ${VAR}
cd ${VAR}
echo ${VAR}

mkdir ${SLURM_ARRAY_TASK_ID}
cd ${SLURM_ARRAY_TASK_ID}

BP="/home/upmeier/acrII1a_design/mcherry/in/"${VAR}".bp"

SC="score_"${VAR}".sc"
OUT="struc_"${VAR}".silent"

srun /work/lpdi/bin/Rosetta/weekly_/Rosetta/main/source/bin/remodel.linuxiccrelease \
@/home/upmeier/acrII1a_design/mcherry/flags \
-use_input_sc \
-s ${ACPT} \
-database /work/lpdi/bin/Rosetta/weekly_/Rosetta/main/database/ \
-remodel:blueprint ${BP} \
-remodel::num_trajectory 10 \
-remodel::save_top 10 \
-remodel::checkpoint \
-out:file:scorefile  ${SC} \
-out:file:silent ${OUT} \
-run::chain A \
-remodel::domainFusion:insert_segment_from_pdb ${INS} \
>> "log_"${VAR}".txt"

echo "Done"


