#!/bin/bash
# -*- coding: utf-8 -*-


# AUTHOR : Yui Tomo (https://github.com/t-yui)
# LAST UPDATE : 2019.05.14
# DESC : Pipeline for QC and PCA using fam, bim, bed files
# REQUIREMENT : plink (>= ver. 1.9)
# USAGE : ./plink_pca_gwas.sh -i ${path_to_data}/${data_nama_without_extension} -o ${path_to_output}


# params for QC
geno=0.02
maf=0.01
hwe=1e-6
indep_pairwise_arg1=50
indep_pairwise_arg2=5
indep_pairwise_arg3=0.2


usage() {
    echo "Usage: $0 [-i <Path & Filename without extention>] [-o <dir>]" 1>&2
    exit 1
}

while getopts :h:i:o: OPT
do
  case ${OPT} in
    "i")
      input=${OPTARG}
    ;;
    "o")
      outdir=${OPTARG}
    ;;
    "h")
      usage
    ;;
    :\?)
      usage
    ;;
  esac
done
if [ "${input}" = "" ]; then
  usage
fi
if [ "${outdir}" = "" ]; then
  outdir=.
fi


filename=`basename ${input}`
resdir=${outdir}/output_PLINK_PCA_${filename}_`date "+%Y%m%d-%H%M%S"`
mkdir ${resdir}


# make result directory
cp -r ${input}.fam ${resdir}/
cp -r ${input}.bim ${resdir}/
cp -r ${input}.bed ${resdir}/


# QC
plink \
    --bfile ${resdir}/${filename} \
    --geno ${geno} \
    --maf ${maf} \
    --hwe ${hwe} \
    --make-bed \
    --out ${resdir}/${filename}_QC |\
    tee -a ${resdir}/logs.txt 2>&1

plink \
    --bfile ${resdir}/${filename}_QC \
    --indep-pairwise ${indep_pairwise_arg1} \
                     ${indep_pairwise_arg2} \
                     ${indep_pairwise_arg3} \
    --out ${resdir}/${filename}_QC_prune |\
    tee -a ${resdir}/logs.txt 2>&1

plink \
    --bfile ${resdir}/${filename}_QC \
    --extract ${resdir}/${filename}_QC_prune.prune.in \
    --make-bed \
    --out ${resdir}/${filename}_prune.prune |\
    tee -a ${resdir}/logs.txt 2>&1

# exec PCA
plink \
    --bfile ${resdir}/${filename}_prune.prune \
    --pca \
    --out ${resdir}/${filename}_pca |\
    tee -a ${resdir}/logs.txt 2>&1