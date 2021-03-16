if [ ! -d "recordings" ]
then
mkdir recordings
echo "recordings directory created..."
fi
if [ ! -d "data" ]
then
mkdir data
echo "data directory created..."
fi
python3 main.py