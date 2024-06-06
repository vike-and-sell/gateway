mkdir -p packaging
for f in ../lambda/*.py ; do 
    name=$(basename $f)
    zip -j -r "packaging/${name%.py}.zip" ../gateway.py $f
done
