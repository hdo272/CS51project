python test3.py $1
python sharpen3.py
python threshold.py car11s.jpg
tesseract threshed_cut.png out -psm 7
cat out.txt
