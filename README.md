
# Named Object Container

# Goal

The project consists in the development of two programs (the client and the server, which are launched on different network stations), the development of a data exchange protocol between them, and the demonstration of the programs' operation.

# About The Container

The server stores named client objects: integers, character strings, etc in the form of a triple <Name, Type, Value>. The client can read, modify objects in the container, and see a list of object names. 

Also both server and client programs form an output file with the system logs.
## Commands

!who - show the name of the program.

!write - add an object in the format <Name, Type, Value> to the container. If the object with the entered name is already in the container, the already existing object will be overwritten.

!read - read an object in the container by its name.

!get - get a sequence of object names. If the container is empty, say so.

!disconnect - disconnect from the server.

Any other command or phrase, written by a client, will be followed by a phrase "Invalid command".
# Start

To start the program, you have to run the server first, then the client. For better experience, I recommend running the server in the IDE and the clients - via Command Prompt by entering the command 

`python your-path-to-the-client.py`

## Small note

In client.py you have to input your IP for the HOST variable.