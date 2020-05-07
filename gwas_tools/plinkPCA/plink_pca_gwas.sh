#!/bin/bash
# -*- coding: utf-8 -*-


# AUTHOR : Yui Tomo (https://github.com/t-yui)
# LAST UPDATE : 2019.05.14
# DESC : Pipeline for QC and PCA using fam, bim, bed files
# REQUIREMENT : plink (>= ver. 1.9)
# USAGE : ./plink_pca_gwas.sh -i ${path_to_data}/${data_nama_without_extension} -o ${path_to_output}

<< COMMENTOUT
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
COMMENTOUT

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
