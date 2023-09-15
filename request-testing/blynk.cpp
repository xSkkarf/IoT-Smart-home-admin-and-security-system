// This program reads the data from the messag queue and sends it to blynk app

#include <sys/ipc.h>
#include <sys/msg.h>
#include <curl/curl.h>
#include <iostream>
using namespace std;

// student data to be sent
string db_arr[5][4] = { { "BLA", "bla", "bla", "bla"},
                        { "Mostafa-Ayyad"  , "1", "1.1", "2030" },
                        { "Emad-sakr"      , "2", "2.2", "2025" },
                        { "Ahmed-hasouna"  , "3", "3.3", "2024" },
                        { "Mohamed-Motawei", "4", "4.4", "2022" },
                    };


struct mesg_buffer { 
    long mesg_type; 
    char mesg_text[100];
} message; 


// a function that sends all the student data to blynk app
void snd_st_data(char * msg){
    int id =0;
    try{
        // convert incoming id to integer
        id = stoi(msg);
    }
    catch(...){
        return;
    }
    
    // blynk dashboard token
    string token = "Qpg2pOvWI-xKyqzg_S6AhnxqpgPGqgFq";
    
    
    // loop through student data array and send each one seperately to a specific virtual pin on blynk
    for(int j=0; j<4; j++){
        
        CURL *curl_obj;
        CURLcode res;
        curl_obj = curl_easy_init();
        
        // used pins: 9-12
        string pin = "v" + to_string(9+j);

        // plug in the token, pin number, and array item with index j
        string request_url = 
        "https://blynk.cloud/external/api/update?token="+
        token+"&"+pin + "=" + db_arr[id][j];

        if(curl_obj){
            curl_easy_setopt(curl_obj, CURLOPT_URL, request_url.c_str());
            res = curl_easy_perform(curl_obj);
            if(res != CURLE_OK){
                fprintf(stderr, "curl_easy_perform() failed: %s\n",
                        curl_easy_strerror(res) );
            }
            
        }

        curl_easy_cleanup(curl_obj);
    }



}
  

int main() 
{
    
    curl_global_init(CURL_GLOBAL_ALL);
    


    key_t key;
    int msgid;

    // ftok to generate unique key
    key = ftok("progfile", 60);

    // msgget creates a message queue and returns an id
    msgid = msgget(key, 0666 | IPC_CREAT);

    // msgrcv to receive message
    msgrcv(msgid, &message,
           sizeof(message.mesg_text), 1, MSG_NOERROR | IPC_NOWAIT);     // IPC_NOWAIT returns immediately if no message was found in the message queue

    printf("Blynk reads: %s \n", message.mesg_text);

    snd_st_data(message.mesg_text);


    curl_global_cleanup();
  
    return 0; 
} 
