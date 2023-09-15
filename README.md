# IoT-Smart-home-admin-and-security-system
- Smart home monitoring system controlled by Blynk web service through a mobile application with a keep-alive system using a socket connection.
- Security system with RFID technology, and motion sensors.

# Request testing
In the request testing folder, the HTTP requests to/from the (Blynk and ADAfruit) cloud services are tested with the help of **inter-process communication** (**message queues**) and a **Bash script** that 
sends dummy readings to a message queue then the message is read by the Blynk and ADAfruit files simultaneously.
