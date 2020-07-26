read -p "enter 1 to initialize database (default NO): " dbinit
sudo docker-compose up --no-start
sudo docker-compose start
echo "NVRD containers are running"
dbinit=$dbinit
if ((dbinit==1)); then
    sudo docker exec nvrd-django bash -c "python Back_end/NVRD/manage.py flush --noinput"
    sudo docker exec nvrd-django bash -c "python Back_end/NVRD/manage.py shell < Back_end/NVRD/eval/values.py"
    echo "nvrdb initialsed"
fi
