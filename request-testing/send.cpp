// This program takes the readings of the RFID module and sends it to a message queue so that both blynk and adafruit programs cand send the data simultaneously 

#include <iostream>
#include <sys/ipc.h> 
#include <sys/msg.h> 
#include <string.h>
#define arr_size 4

using namespace std;
  
// structure for message queue 
struct mesg_buffer { 
    long mesg_type; 
    char mesg_text[100]; 
} message; 


// function to search for the id in the data array
bool is_id(double id, int *arr){
    for(int i=0; i< arr_size; i++){
        if(id == *(arr+i)){
            return 1;
        }
    }
    return 0;
}


  
int main() 
{ 
    int ids[4] = {1,2,3,4};

    key_t key; 
    int msgid;
  
    // ftok to generate unique key 
    key = ftok("progfile", 60); 
  
    // msgget creates a message queue and returns an id
    msgid = msgget(key, 0666 | IPC_CREAT);
    message.mesg_type = 1; 
    

    // char array to take input from user and proccess it
    char temp[100];

    // variable to pass to the id search function with the data from RFID
    double res;
    try{
        printf("Write Data : "); 

        // takes RFID data through a pipe from rfr.py
        scanf("%s", temp);

        // convert string data to integer
        res = stoi(temp);

    }
    catch(...){
        // if the stoi function throws an error (a character passed to it), the following message is printed and the main returns with an error code 1
        cout << "Please enter the correct ID." << endl;
        return 1;
    }
    
    
    // check if id is found in the data array
    if(is_id(res, ids)){
        // copy temp contents to the message queue buffer struct
        strcpy(message.mesg_text, temp);

        // send the message twice to be read by blynk.cpp and ada.cpp and then popped from the message queue
        cout << "Data send is : " << message.mesg_text << ", Error code : " << msgsnd(msgid, &message, sizeof(message.mesg_text), 0) << endl;
        cout << "Data send is : " << message.mesg_text << ", Error code : " << msgsnd(msgid, &message, sizeof(message.mesg_text), 0) << endl;
    }
    else{
        cout << "ID not found" << endl;

        // send not found in the message queue
        strcpy(message.mesg_text,"ID-not-found");
        message.mesg_text, msgsnd(msgid, &message, sizeof(message.mesg_text), 0);
        message.mesg_text, msgsnd(msgid, &message, sizeof(message.mesg_text), 0);
    }
  
    
  
    return 0; 
} 
