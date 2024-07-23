mkdir -p packaging
mkdir -p packaging/layer

cp ../requirements.txt packaging/layer/requirements.txt

for f in ../lambda/*.py ; do 
    name=$(basename $f)
    zip -j -r "packaging/${name%.py}.zip" ../lambda/shared.py ../gateway.py $f
done
