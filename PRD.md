# Product Requirements Document (PRD)

## 1. Purpose

The game is a strategy tycoon where players take the role of an AI venture capitalist, developing AI labs specializing in NLP, Computer Vision, and other fields. Players compete to achieve the highest valuation for their labs and aim for the top of the leaderboard. The unique twist is that both humans and reinforcement learning agents (RL agents) can compete for the highest rankings.

## 2. Key Features

### 2.1. Core Gameplay (Phase 1 & 2)

- Lab Creation & Management: Players can create AI labs in various fields (e.g., NLP, CV) and assign resources to research models or products in those fields.
- Resource Generation: Players generate resources over time as income (funds, research points, etc.) which can be spent to improve their labs.
- AI Model Development: Players allocate resources to develop and improve AI models in one or multiple labs, increasing their lab valuation.
- Leaderboard: Players compete based on the combined valuation of their labs, which is tracked in a real-time leaderboard.

### 2.2. AI Agent Gameplay (Phase 3)

- AI Players: Players can train reinforcement learning agents to play the game autonomously. The RL agents use game data to optimize resource allocation and decisions.
- AI vs. Human Interaction: AI agents compete against human players, both aiming to climb the leaderboard based on the same game mechanics.

### 2.3. Multiplayer Aspects (Phase 2 & 3)

- Real-time Leaderboard: A global leaderboard updates in real-time, showing the rankings of all players (human and AI).
- Cross-player Interaction: Players can invest in or sabotage other players' labs, adding a competitive element.

### 2.4. Game Progression (Phase 4)

- Scaling: As the player progresses, the cost and time to develop AI models increase, introducing a strategic layer where resource management becomes essential.
- Achievements: Unlockable achievements for reaching specific milestones (e.g., “First Lab to $1B Valuation”).

## 3. User Experience

- Gameplay Loop: Players are drawn into an engaging tycoon loop, where they generate resources, improve labs, and compete on the leaderboard.
- Progression: Players should feel a sense of progression and achievement as they grow their labs, unlock new AI technologies, and improve their standing on the leaderboard.

## 4. Technical Requirements

### 4.1. Backend

- Server Framework: Rust (Axum) for managing game state and player interactions.
- Database: PostgreSQL to handle persistent data (user accounts, game data, labs, etc.). Redis for caching (optional, as needed for scaling).
- WebSockets: Real-time communication between server and frontend.

### 4.2. Frontend

- Framework: SvelteKit to provide a reactive, real-time web application.
- WebSocket API: For real-time state updates between the frontend and backend.

### 4.3. AI Agents

- Training: PyTorch/TensorFlow for training RL agents.
- Game Simulation: A simplified game environment for training AI agents, possibly using OpenAI Gym.

## 5. Metrics

- Engagement: Time spent in-game and player progression (e.g., lab valuation over time).
- Leaderboard Activity: Frequency of leaderboard changes, distribution of rankings.
- AI Agent Performance: Tracking the success rate of AI agents versus human players.

## 6. Monetization

- In-game purchases: Players can purchase cosmetic items to enhance their experience.
- Donations: Players can donate to the game development fund.
- Premium deployment: Players can pay to have their own AI agents deployed on a server.
