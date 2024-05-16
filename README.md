# Bomb Party

Description of Project:

Our project is based on the online multiplayer game, named "Bomb Party". In the game, players are prompted one by one with a 2 to 3 letter substring, and the current player must respond with a valid word. A valid word is defined as a word that contains the substring, exists in a predefined dictionary, and has not been used by any players in the game. After either a valid word is entered or a timer runs out, the game will prompt the next player with a new substring. 

If a valid word is entered, the player that entered the word will store the letters it has used. If a player uses every letter in the alphabet at least once, the player will gain a life and reset their stored letters for the opportunity to gain more lives.

 If the timer runs out, the player will lose a life, and upon reaching 0 lives, the player will be out of the game. The winner of the game is the last player remaining.

How to Host Game and Connect Players:

1. Launch the server with the command:
   1. "python server.py `<port number>`"
2. Connect up to 5 players to the game server:
   1. "python client.py `<host IP> <port number>`"
3. To begin the game, each player must type start into the command line.
4. The game will now start, and will continue until one player is left alive.
