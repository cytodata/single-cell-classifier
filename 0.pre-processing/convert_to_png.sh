for f in `find . -name '*.tiff'`; do
  convert ./"$f" -auto-level -depth 8 ./"${f%.tiff}.png"
done

find . -name "*tiff"  -exec rm {} \;


