NUMBER=$(printf "%02d" $1)
NAME="$2"
FILENAME="${NUMBER}/$NAME"
SESSION_COOKIE=$(cat .sessioncookie)

if [ ! -d $NUMBER ]
then
    mkdir $NUMBER

    cp template.py $FILENAME.py
    sed -i '' -e 's|DAY|'"$NUMBER"'|g' $FILENAME.py

    curl 'https://adventofcode.com/2025/day/'$1'/input' -H 'Cookie: session='$SESSION_COOKIE > $NUMBER/input.txt
else
    echo "Directory $NUMBER already exists"
fi
