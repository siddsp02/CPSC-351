# Data Transfer Document

### Client Interaction

The client will do form validation and then send data to the server using JSON.


### Server Interaction

**POST** requests will return JSON.
**GET** request will return HTML.

## Sequence of Events
1. User inputs values into initial form
    - These will be validated using HTML and Javascript
2. If Validation succeeds:
    - Render graph in D3.js
    - Send data so that server has session storage of automata
3. If Validation Fails:
    - Show user invalid inputs and let them try again

**Graph is rendered now**

1. Form is displayed which allows user to test input string against automata.
2. User inputs string (for now, any string), send string to server.
3. If string is valid, send string to server, otherwise, show invalid input state to user.
4. Server will take string, and *walk* through the constructed automata.
5. Have loop count to ensure not infinite *walking*. (1000 ?, 10000?)
6. Trace state path and place in list. Return list in as list to client.
7. Client will animate rendered graph based on response on the server.


