# Truco Gaúcho: A Networked Card Game in Python

This project is a complete, object-oriented implementation of the card game **Truco Gaúcho**, a popular variant of Truco played with a 40-card Spanish deck. The game is developed in Python and features a client-server architecture that allows two players to compete online in real-time.

The application includes a graphical user interface (GUI) built with Tkinter and leverages the [DOG (Doing Online Games)](https://www.inf.ufsc.br/~ricardo.silva/dog/) framework to manage network communication, player synchronization, and game state.

## Features

*   **Networked 1v1 Gameplay:** A client-server architecture allows two players to connect to a game server and play against each other remotely.
*   **Complete Game Logic:** Implements all the core rules and betting rounds of Truco Gaúcho, including:
    *   **Truco, Retruco, and Vale 4:** The main bluffing and betting mechanic of the game.
    *   **Envido, Real Envido, and Falta Envido:** The side-bet based on the value of card combinations in a player's hand.
    *   **Flor:** A special hand containing three cards of the same suit, triggering a unique betting round.
*   **Interactive Graphical User Interface:** A clean and functional GUI built with Tkinter displays the game board, player hands, the scoreboard, and interactive pop-ups for challenges and responses.
*   **Real-time Game State Synchronization:** Player moves and game state changes are instantly reflected on both clients' screens through the DOG networking layer.

## Gameplay Overview

Truco Gaúcho is a point-based card game for two players.

*   **Objective:** Be the first player to score 30 points.
*   **The Deck:** A 40-card Spanish deck is used (8s and 9s are removed).
*   **The Hand (`Mão`):** A game is divided into hands. Each hand is worth 1 point initially, but its value can be increased by betting "Truco". A hand consists of up to three rounds (`Rodada`).
*   **The Round (`Rodada`):** In each round, both players play one card. The player with the higher-ranking card wins the round. The first player to win two rounds wins the hand and its corresponding points.
*   **Betting:** Before playing a card, players can challenge each other with bets like "Truco", "Envido", or "Flor" to raise the stakes and score additional points.

## Technical Architecture

The application is built upon a distributed, object-oriented, client-server model.

1.  **Client-Server Model:** Each player runs a client instance of the game. The clients do not communicate directly but through a central DOG server, which relays moves and maintains the match state.
2.  **DOG (Distributed Object Games) Framework:** This project uses the DOG framework as a middleware for network communication.
    *   **`DogActor` and `DogProxy`:** A proxy pattern is used to abstract network complexity. The `DogProxy` on the client side communicates with the remote server via HTTP requests, handling player registration, match initiation, and move synchronization.
    *   **Polling:** A background thread continuously polls the server for updates (e.g., the opponent's move), allowing for asynchronous, real-time gameplay.
3.  **Object-Oriented Design:** The game logic is heavily object-oriented, with classes representing distinct concepts:
    *   **`Partida` (Match):** The main engine that controls the game flow, manages player turns, and enforces rules.
    *   **`Jogador` (Player):** Represents a player's state, including their hand of cards and score.
    *   **`Mesa` (Table):** Manages the deck of cards and the cards played in each round.
    *   **`Carta` (Card):** Represents a single card, with methods for serialization to be sent over the network.
    *   **`Truco`, `Envido`, `Flor`:** Classes that encapsulate the specific logic and point values for each type of bet.
4.  **Event-Driven GUI:**
    *   The **`PlayerInterface`** class is responsible for the entire GUI. It uses Tkinter to create the main window, display cards, show scores, and generate dynamic pop-ups for player actions.
    *   User actions (like clicking a card or a button) trigger methods that send a move to the server via the `DogActor`. In turn, moves received from the server trigger methods that update the GUI to reflect the new game state.

## Technology Stack

*   **Language:** Python 3.10
*   **GUI:** Tkinter (Python's standard library)
*   **Image Handling:** Pillow (Python Imaging Library) for rendering card images with anti-aliasing.
*   **Networking:** DOG (Distributed Object Games) Framework, which uses `requests` for HTTP communication.
*   **Design & Modeling:** The project's requirements and architecture were designed using UML, with diagrams created in Visual Paradigm. (Full diagrams are available in the `.vpp` file in the repository).

## Setup and Usage

Follow these steps to set up and run the game client.

### Prerequisites

*   Python 3.10 or higher.
*   `virtualenv` for creating an isolated Python environment.

### Installation & Execution

1.  **Clone the repository:**
    ```
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```
    # Create the environment
    virtualenv venv

    # Activate it (on Linux/macOS)
    source venv/bin/activate

    # On Windows, use:
    # venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```
    python3 src/truco_gaucho.py
    ```

Upon launching, the application will prompt you for a player name and attempt to connect to the DOG server. Once connected, you can start a new match from the "Jogo" menu.

## Some example diagrams from the .vpp
![image](https://github.com/user-attachments/assets/d8bc7f9a-1164-4a9f-b696-39e7c5b8a229)
![image](https://github.com/user-attachments/assets/7ad8e591-a6f7-4557-8d78-b474ce903459)
![image](https://github.com/user-attachments/assets/c231d3c0-8023-4410-a35a-541a6f82e265)
![image](https://github.com/user-attachments/assets/19b50fac-cc5e-47d3-84ab-bbeb4013a18d)
![image](https://github.com/user-attachments/assets/d4591b92-20cb-47b6-8e75-7c765117e7fd)



