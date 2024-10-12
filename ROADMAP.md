# Roadmap

## Phase 1: Core Infrastructure (Backend + Frontend Basics)

- [x] Set up the Loco project and server with WebSocket support.
- [ ] Create PostgreSQL tables for players, labs, resources, and models.
- [ ] Build a SvelteKit frontend with a basic UI that connects via WebSocket to the backend.
- [ ] Implement the core gameplay loop (resource generation, lab management, model upgrades).

## Phase 2: Game Logic and Leaderboard

- [ ] Implement valuation mechanics for labs and models.
- [ ] Set up the real-time leaderboard that updates based on lab valuations.
- [ ] Add cross-player interaction features (e.g., investments, sabotage).
- [ ] Optionally integrate Redis for caching leaderboard or live game state.

## Phase 3: AI Agent Integration

- [ ] Create a simplified OpenAI Gym environment for RL agent training.
- [ ] Develop the RL agent using PyTorch/TensorFlow.
- [ ] Allow AI agents to interact with the server via WebSocket, just like human players.
- [ ] Add AI agent data to the leaderboard.

## Phase 4: Game Balance and Testing

- [ ] Balance resource generation rates, model development costs, and lab valuations.
- [ ] Test AI vs. human interactions to ensure fairness and competitive gameplay.
- [ ] Conduct stress tests on the WebSocket infrastructure to ensure scalability.

## Phase 5: Launch and Open Source

- [ ] Prepare for launch by creating a GitHub repository with clear documentation.
- [ ] Open source the project, encouraging community contributions to AI agents or new gameplay mechanics.
