filename=$(basename -- "${1}")
filename="${filename%.*}"
out=out
#out=`mktemp`
mkdir -p ${out}
pdfimages -j ${1} ${out}/${filename}
python3 binarize.py ${out}/${filename}-*.* -o out
