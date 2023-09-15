x=0
while true
do
    # run this to use the actual readings from the RFID module
    #python3 rfr.py | ./send
    #

     #run this to use test data
     echo $((x+1)) | ./send
     x=$((x+1))
     x=$((x%4))



    ./blynk & ./ada

    sleep 4
done
