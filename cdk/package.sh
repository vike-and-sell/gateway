mkdir -p packaging
mkdir -p packaging/layer

cp ../flask/requirements.txt packaging/layer/requirements.txt

for f in ../lambda/*.py ; do 
    name=$(basename $f)
    zip -j -r "packaging/${name%.py}.zip" ../gateway.py $f
done
