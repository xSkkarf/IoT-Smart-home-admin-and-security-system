// This program reads the data from the messag queue and sends it to adafruit cloud service
#include <iostream>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <curl/curl.h>

using namespace std;

struct mesg_buffer { 
    long mesg_type; 
    char mesg_text[100];
} message; 
  
int main() 
{

    key_t key;
    int msgid;

    // ftok to generate unique key
    key = ftok("progfile", 60);

    // msgget creates a message queue and returns an id
    msgid = msgget(key, 0666 | IPC_CREAT);

    // msgrcv to receive message
    msgrcv(msgid, &message,
           sizeof(message.mesg_text), 1, MSG_NOERROR | IPC_NOWAIT);

    // display the message
    printf("Ada reads: %s \n", message.mesg_text);



    CURL *curl;
    CURLcode res;
    curl = curl_easy_init();
    if(curl) {
        // set request type
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
        
        // set URL and protocol
        curl_easy_setopt(curl, CURLOPT_URL, "https://io.adafruit.com/api/v2/xSkkarf/feeds/rfid/data");
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");

        // define headers
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "X-AIO-Key: aio_MmFD05FUXCyl2zP1hbyeFDZ7ftiA");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        
        curl_mime *mime;
        curl_mimepart *part;
        mime = curl_mime_init(curl);
        part = curl_mime_addpart(mime);
        curl_mime_name(part, "value");

        // include the actual message in the request
        curl_mime_data(part, message.mesg_text, CURL_ZERO_TERMINATED);
        curl_easy_setopt(curl, CURLOPT_MIMEPOST, mime);
        res = curl_easy_perform(curl);
        curl_mime_free(mime);
    }
    curl_easy_cleanup(curl);
  
    return 0; 
} 
