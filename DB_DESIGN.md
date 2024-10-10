# Database Design

## 1. Players Table

Stores information about human players and AI players.

```sql
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    is_ai BOOLEAN DEFAULT FALSE,  -- Differentiates human and AI players
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 2. Labs Table

Represents the labs created by each player.

```sql
CREATE TABLE labs (
    lab_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
    lab_name VARCHAR(100) NOT NULL,
    field VARCHAR(50),  -- E.g., NLP, Computer Vision
    valuation DECIMAL(15,2) DEFAULT 0.00,  -- Lab valuation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 3. Resources Table

Tracks resources (e.g., funds, research points) each player owns.

```sql
CREATE TABLE resources (
    resource_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
    funds DECIMAL(15,2) DEFAULT 0.00,
    research_points INT DEFAULT 0,  -- Points for developing AI models
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. Models Table

Tracks AI models developed by players in their labs.

```sql
CREATE TABLE models (
    model_id SERIAL PRIMARY KEY,
    lab_id INT REFERENCES labs(lab_id) ON DELETE CASCADE,
    model_name VARCHAR(100) NOT NULL,
    field VARCHAR(50),  -- NLP, CV, etc.
    level INT DEFAULT 1,  -- Level of the model (higher = better)
    value DECIMAL(15,2) DEFAULT 0.00,  -- Value contribution to the lab
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 5. Leaderboard Table

Tracks the real-time leaderboard of players based on their total lab valuations.

```sql
CREATE TABLE leaderboard (
    leaderboard_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
    total_valuation DECIMAL(15,2) DEFAULT 0.00,  -- Total valuation across all labs
    rank INT DEFAULT 0,  -- Player rank on the leaderboard
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 6. AI Agent Table

Stores metadata for AI agents.

```sql
CREATE TABLE ai_agents (
    ai_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
    training_data JSONB,  -- Serialized training data for the RL agent
    performance_metrics JSONB,  -- Performance stats (e.g., win/loss record)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
