# Snake Game 🐍

A classic Snake game built with Python and Pygame featuring **Human vs AI** mode! Control your snake, compete against an AI opponent, eat food to grow longer, and try to achieve the highest score!

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.6.1+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎮 Game Features

- **Two game modes**: Human vs AI (default) or single-player
- **AI opponent** with BFS pathfinding algorithm
- Smooth keyboard controls for human player
- Score tracking with player name input
- **Level progression** - speed increases every 5 points
- Self-collision and wall collision detection
- Pause functionality
- Game over screen with restart option
- Flask API + SQLite leaderboard (top 10 scores)
- Auto-refreshing web leaderboard
- Docker support with X11 forwarding for Linux

## 🎯 How to Play

### Controls
| Key | Action |
|-----|--------|
| ⬆️ Up Arrow | Move snake up |
| ⬇️ Down Arrow | Move snake down |
| ⬅️ Left Arrow | Move snake left |
| ➡️ Right Arrow | Move snake right |
| **P** | Pause the game |
| **Any Key** | Resume the game |
| **R** | Restart game (after game over) |
| **Q** | Quit game |

### Game Rules
1. Control the green snake to eat the red food blocks
2. AI controls the blue snake (in VS mode)
3. Each food eaten increases score by 1.5
4. Both snakes grow longer after eating
5. Game ends if either snake:
   - Hits the wall
   - Collides with its own body
   - Collides with the other snake
6. **Win condition**: Last snake standing wins!
7. Level increases every 5 points, making the game faster

### Game Modes

**Human vs AI Mode** (`VS_AI = True` - default):
- Compete against an AI snake using BFS pathfinding
- AI intelligently navigates toward food while avoiding collisions
- First snake to die loses

**Single-Player Mode** (`VS_AI = False`):
- Classic Snake experience
- Play against yourself to achieve high scores

## 🚀 Quick Start
```bash
# For Ubuntu system
./run.sh --rebuild
```

```text
--rebuild forces a fresh Docker image rebuild (useful after dependency changes).
```

- ✅ Detect if Docker is installed

- ✅ Start Docker daemon if needed

- ✅ Automatically fix permission issues (new!)

- ✅ Clean up port 5000

- ✅ Start the Snake Game

- ✅ Clean up when done

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/boaca926-beep/sneak.git
cd snake-game
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
# or
pip install pygame
```

3. **Start the Flask  API (for leaderboard)**
```bash
python score_api.py
```

3. **In a new terminal, run the game**
```bash
python snake.py
```

## 🐳 Docker Setup (For Linux with X11)

1. **Make the run script executable**
```bash
chmod +x run.sh
```

2. **Start the game**
```bash
./run.sh
```

3. **# Rebuild Docker image if needed**
```bash
./run.sh --rebuild
```

<p align="center">
  <img src="figures/game_end.png" alt="Top-10 scores output" width="400">
  <img src="figures/snake_output.png" alt="Top-10 scores output" width="400">
</p>

3. **Rebuild Docker image if needed**
```bash
./run.sh --rebuild
```

## X11 Security Note
The script uses xhost +local:docker for simplicity. On multi‑user systems, use a more restrictive command:
```bash
xhost +SI:localuser:root
```

## Docker Configuration
The project includes Docker support for consistent development environments, especially useful for Linux systems with GUI forwarding.

### docker-compose.yml Features
- X11 display forwarding for GUI rendering

- Volume mounting for live code updates

- Network host mode for display access

- Environment variables for debugging and X11 configuration

### Manual Docker Commands
```bash
# Build the image
docker build -t snake-game .

# Run with GUI support
xhost +local:docker
docker compose up
docker compose down
xhost -local:docker
```

## 📁 Project Structure
```text
snake-game/
├── snake.py              # Main game implementation
├── score_api.py          # Flask API + SQLite leaderboard
├── leaderboard.html      # Auto‑refreshing web leaderboard
├── my_game.py            # Legacy/alternative game entry point
├── docker-compose.yml    # Docker orchestration
├── Dockerfile            # Docker image definition
├── run.sh                # Quick start script (with Docker & API)
├── inspect_db.sh         # SQLite inspection helper
├── requirements.txt      # Python dependencies (pip)
├── pyproject.toml        # Project metadata (PEP 621)
├── uv.lock               # uv package manager lock file
├── scores.db             # SQLite database (created at runtime)
├── figures/              # Screenshots for README (game_end.png, etc.)
└── scripts/              # Additional helper scripts (if any)
```

## Customization Options
Edit snake.py to modify game behavior:

| Variable | Description | Default |
|----------|-------------|---------|
| VS_AI | Toggle Human vs AI mode | True
| `CELL_SIZE` | Size of each grid cell (pixels) | 30 |
| `GRID_WIDTH` | Number of grid columns | 20 |
| `GRID_HEIGHT` | Number of grid rows | 20 |
| `LEVEL_EVERY` | Points needed to level up | 5 |
| `base_fps` | Starting game speed | 6 (Easy), 10 (Medium), 14 (Hard)|
| `SPEED_INCREMENT` | FPS increase per level| 0.5 |
| `MAX_FPS` | Maximum game speed | base_fps + 5 |

## Color Customization
```python
BLACK = (0, 0, 0)        # Background
GREEN = (0, 200, 0)      # Human snake body
DARK_GREEN = (0, 150, 0) # Human snake border
BLUE = (0, 100, 200)     # AI snake body
DARK_BLUE = (0, 50, 100) # AI snake border
RED = (255, 0, 0)        # Food
GRAY = (50, 50, 50)      # Grid lines
WHITE = (200, 200, 200)  # Text
```

## 🛠️ Development

### Prerequisites

- Python 3.12 or higher

- Pygame 2.6.1+

- Docker (optional, for containerized execution)

- X11 server (for Linux GUI support)

### Environment Variables (Docker)
```bash
DISPLAY=${DISPLAY}              # X11 display for GUI
ENABLE_DEBUG=${ENABLE_DEBUG}    # Debug mode toggle
QT_X11_NO_MITSHM=1              # X11 shared memory fix
LIBGL_ALWAYS_SOFTWARE=1         # Software rendering fallback
```

## 🎯 Future Enhancements
Potential features to add:

- ✅ Pause function (press P, and to resume press any key)
- ✅ Multiple difficulty levels (speed increases over time)
- ✅ High score tracking with persistent storage
- ✅ AI-controlled snake for demo mode
- Power-ups and special food types
- Sound effects and background music
- Two-player mode
- Different maze/wall configurations

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Error response from daemon: Conflict" | docker system prune -a && docker volume prune |
| "Cannot connect to X server" | `xhost +local:docker` and `export DISPLAY=$DISPLAY` |
| Pygame won't install | `sudo apt-get install python3-pygame` (Ubuntu) |
| Game runs too fast/slow | Adjust `FPS` in `snake.py` (higher = faster, lower = slower) |
| Docker GUI not showing | `export LIBGL_ALWAYS_SOFTWARE=1` |
| Leaderboard shows no data | Ensure API is running on `localhost:5000` before opening `leaderboard.html` |
| Port 5000 already in use | `fuser -k 5000/tcp` (Linux) or stop the process using the port |

## Flask API with SQLite that stores the highest scores and allows retrieval of the top 10.
```bash
score_api.py
```

### Run the API
```bash
python score_api.py

# Add a score
#curl -X POST http://localhost:5000/score \
#  -H "Content-Type: application/json" \
#  -d '{"player_name":"Bo","score":350}'

# Get top 10 scores
curl http://localhost:5000/top-scores
```

## Persistent Storage in Docker
Add a volume to docker-compose.yml to keep scores.db across container restarts:
```yaml
volumes:
  - ./data:/app/data
```

## Inspect Database
```bash
# Run SQlite
./inspect_db.sh
```

**Operations**
```sql
.tables          -- should show 'scores'
.schema scores   -- see table structure
SELECT * FROM scores;
```

## Auto‑refreshing leaderboard window

### 1. Create leaderboard.html in the project folder
```bash
leaderboard.html
```
<p align="center">
  <img src="figures/top10_web.png" alt="Top-10 scores output" width="600">
</p>

### 2. Modify snake.py to open the leaderboard
```python
import webbrowser   # add at the top

# ... inside main(), after getting player_name:

# Open the leaderboard window (only once)
leaderboard_path = os.path.join(os.path.dirname(__file__), "leaderboard.html")
webbrowser.open(f"file://{leaderboard_path}", new=2)  # new=2 opens in new tab if possible
```

### 3. Make sure the API is reachable
```bash
- The score-api container must be running and accessible on localhost:5000.

- The docker-compose.yml already maps "5000:5000", so the host can reach it.

- The browser (running on local host) will fetch http://localhost:5000/top-scores without any problem.
```

### 4. Full integration to snake.py
```python
# At the top
import webbrowser
import os

# Inside main(), after player_name is known:
leaderboard_url = f"file://{os.path.abspath('leaderboard.html')}"
webbrowser.open(leaderboard_url)
```
## Data pipe-lin report (Airflow)
✅ Clean data = Accurate leaderboard

✅ Automatic reports - "Top player of the week" emails

✅ Cheat detection - Flags suspicious scores automatically

✅ Backups - Your data is safe in cloud storage

✅ Professional skills - This is how real companies (Netflix, Uber, Airbnb) handle data

## How to evolve this project toward data engineering

-Replace SQLite with PostgreSQL (or use both). Add Docker Compose service for Postgres. Show you can connect to a production‑grade database.

- Add a data pipeline: every time a score is submitted, also write to a raw log table. Create a scheduled job (e.g., inside the API) that aggregates daily top scores into a summary table (leaderboard snapshot).

- Implement a simple ETL script: export scores to a CSV/Parquet file, or load them into a second database for analytics.

- Use environment‑aware config – expand to load different configs for dev/prod.

- Add metrics / monitoring: track number of scores per hour, average score, etc. Expose via a new /stats endpoint.

- Containerize with Airflow (complex but impressive): create a DAG that runs deduplication SQL every hour instead of at game start.
  1. Create required folders
  ```bash
  mkdir -p airflow/{dags,logs,plugins} data
  ```
  2. Update requirements.txt
  ```bash
  echo     "apache-airflow==2. 8.1" >>
  requirements.txt
  echo  "psycopg2-binary" >> requirements.txt
  echo "pandas" >> requirements.txt
  echo "pyarrow" >>   requirements.txt #   For Parquet export
  ```
  3. Update docker-compose.yml
  ```yaml
  version: '3.8'

  services:
    # Existing Snake Game service
    snake-game:
      build: .
      container_name: snake-game
      environment:
        - DISPLAY=${DISPLAY}
        - QT_X11_NO_MITSHM=1
        - LIBGL_ALWAYS_SOFTWARE=1
        - ENABLE_DEBUG=${ENABLE_DEBUG:-0}
      volumes:
        - /tmp/.X11-unix:/tmp/.X11-unix:rw
        - ./scores.db:/app/scores.db
        - ./data:/app/data  # For Airflow to access
      network_mode: host
      stdin_open: true
      tty: true
      command: python snake.py

    # Existing Score API
    score-api:
      build: .
      container_name: score-api
      ports:
        - "5000:5000"
      volumes:
        - ./scores.db:/app/scores.db
        - ./data:/app/data
      environment:
        - DATABASE_URL=sqlite:///app/scores.db
      command: python score_api.py

    # New: PostgreSQL for Airflow metadata
    postgres:
      image: postgres:13
      container_name: airflow-postgres
      environment:
        - POSTGRES_USER=airflow
        - POSTGRES_PASSWORD=airflow
        - POSTGRES_DB=airflow
      volumes:
        - postgres_data:/var/lib/postgresql/data
      ports:
        - "5432:5432"
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U airflow"]
        interval: 10s
        timeout: 5s
        retries: 5

    # New: Redis for Airflow executor
    redis:
      image: redis:7.2
      container_name: airflow-redis
      ports:
        - "6379:6379"
      healthcheck:
        test: ["CMD", "redis-cli", "ping"]
        interval: 10s
        timeout: 5s
        retries: 5

    # New: Airflow Webserver
    airflow-webserver:
      image: apache/airflow:2.8.1
      container_name: airflow-webserver
      depends_on:
        - postgres
        - redis
      environment:
        - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
        - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
        - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
        - AIRFLOW__CELERY__BROKER_URL=redis://:@redis:6379/0
        - AIRFLOW__WEBSERVER__RBAC=True
        - AIRFLOW__CORE__LOAD_EXAMPLES=False
        - _PIP_ADDITIONAL_REQUIREMENTS=psycopg2-binary pandas sqlalchemy
      volumes:
        - ./airflow/dags:/opt/airflow/dags
        - ./airflow/logs:/opt/airflow/logs
        - ./airflow/plugins:/opt/airflow/plugins
        - ./data:/opt/airflow/data
        - ./scores.db:/opt/airflow/scores.db
      ports:
        - "8080:8080"
      command: webserver
      healthcheck:
        test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
        interval: 30s
        timeout: 10s
        retries: 5

    # New: Airflow Scheduler
    airflow-scheduler:
      image: apache/airflow:2.8.1
      container_name: airflow-scheduler
      depends_on:
        - postgres
        - redis
        - airflow-webserver
      environment:
        - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
        - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
        - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
        - AIRFLOW__CELERY__BROKER_URL=redis://:@redis:6379/0
        - _PIP_ADDITIONAL_REQUIREMENTS=psycopg2-binary pandas sqlalchemy
      volumes:
        - ./airflow/dags:/opt/airflow/dags
        - ./airflow/logs:/opt/airflow/logs
        - ./airflow/plugins:/opt/airflow/plugins
        - ./data:/opt/airflow/data
        - ./scores.db:/opt/airflow/scores.db
      command: scheduler

    # New: Airflow Worker
    airflow-worker:
      image: apache/airflow:2.8.1
      container_name: airflow-worker
      depends_on:
        - postgres
        - redis
        - airflow-webserver
      environment:
        - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
        - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
        - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
        - AIRFLOW__CELERY__BROKER_URL=redis://:@redis:6379/0
        - _PIP_ADDITIONAL_REQUIREMENTS=psycopg2-binary pandas sqlalchemy
      volumes:
        - ./airflow/dags:/opt/airflow/dags
        - ./airflow/logs:/opt/airflow/logs
        - ./airflow/plugins:/opt/airflow/plugins
        - ./data:/opt/airflow/data
        - ./scores.db:/opt/airflow/scores.db
      command: celery worker

  volumes:
    postgres_data:
  ```

  **Create Airflow DAG for Score Deduplication**
  Create ```bash
  airflow/dags/snake_game_pipeline.py```

  ```python
  from datetime import datetime, timedelta
  from airflow import DAG
  from airflow.operators.python import PythonOperator
  from airflow.operators.bash import BashOperator
  from airflow.operators.email import EmailOperator
  from airflow.models import Variable
  import sqlite3
  import pandas as pd
  from pathlib import Path
  import logging

  default_args = {
      'owner': 'data_engineer',
      'depends_on_past': False,
      'start_date': datetime(2024, 1, 1),
      'email_on_failure': True,
      'email_on_retry': False,
      'email': ['admin@snakegame.com'],
      'retries': 1,
      'retry_delay': timedelta(minutes=5)
  }

  def deduplicate_scores(**context):
      """Remove duplicate scores based on (player_name, score, timestamp)"""
      db_path = '/opt/airflow/scores.db'

      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()

      # Find and remove duplicates
      cursor.execute("""
          DELETE FROM scores
          WHERE rowid NOT IN (
              SELECT MIN(rowid)
              FROM scores
              GROUP BY player_name, score, timestamp
          )
      """)

      deleted_count = cursor.rowcount
      conn.commit()
      conn.close()

      logging.info(f"Removed {deleted_count} duplicate score entries")

      # Push to XCom for downstream tasks
      context['task_instance'].xcom_push(key='deleted_duplicates', value=deleted_count)

      return deleted_count

  def create_daily_aggregates(**context):
      """Create daily aggregated stats"""
      db_path = '/opt/airflow/scores.db'

      conn = sqlite3.connect(db_path)

      # Daily aggregates query
      query = """
      CREATE TABLE IF NOT EXISTS daily_stats AS
      SELECT
          DATE(timestamp) as game_date,
          COUNT(*) as total_games,
          COUNT(DISTINCT player_name) as unique_players,
          MAX(score) as highest_score,
          AVG(score) as avg_score,
          MIN(score) as lowest_score,
          SUM(CASE WHEN score >= 100 THEN 1 ELSE 0 END) as high_score_games
      FROM scores
      WHERE timestamp >= datetime('now', '-1 day')
      GROUP BY DATE(timestamp)
      """

      df = pd.read_sql_query(query, conn)
      conn.close()

      logging.info(f"Daily aggregates created: {len(df)} records")

      # Save to CSV for backup
      output_path = Path('/opt/airflow/data/daily_stats.csv')
      df.to_csv(output_path, index=False)

      context['task_instance'].xcom_push(key='daily_stats_count', value=len(df))

      return len(df)

  def check_score_anomalies(**context):
      """Detect suspicious high scores (> 1000)"""
      db_path = '/opt/airflow/scores.db'

      conn = sqlite3.connect(db_path)
      query = """
      SELECT player_name, score, timestamp
      FROM scores
      WHERE score > 1000
      ORDER BY score DESC
      LIMIT 10
      """

      anomalies = pd.read_sql_query(query, conn)
      conn.close()

      if len(anomalies) > 0:
          logging.warning(f"Found {len(anomalies)} anomalous high scores!")
          # Save anomalies report
          anomalies.to_csv('/opt/airflow/data/anomalies.csv', index=False)

          context['task_instance'].xcom_push(key='anomalies_found', value=len(anomalies))
          return len(anomalies)
      return 0

  def export_to_analytics_db(**context):
      """Export scores to a separate analytics database (Parquet format)"""
      db_path = '/opt/airflow/scores.db'

      conn = sqlite3.connect(db_path)

      # Load all scores
      df = pd.read_sql_query("SELECT * FROM scores ORDER BY timestamp DESC", conn)
      conn.close()

      # Save as Parquet for better analytics
      parquet_path = f'/opt/airflow/data/scores_{datetime.now().strftime("%Y%m%d")}.parquet'
      df.to_parquet(parquet_path, index=False)

      logging.info(f"Exported {len(df)} records to {parquet_path}")

      return parquet_path

  # Define the DAG
  dag = DAG(
      'snake_game_data_pipeline',
      default_args=default_args,
      description='Data pipeline for Snake Game scores',
      schedule_interval='@hourly',  # Run every hour
      catchup=False,
      tags=['snake_game', 'etl', 'deduplication']
  )

  # Define tasks
  t1 = PythonOperator(
      task_id='deduplicate_scores',
      python_callable=deduplicate_scores,
      dag=dag
  )

  t2 = PythonOperator(
      task_id='create_daily_aggregates',
      python_callable=create_daily_aggregates,
      dag=dag
  )

  t3 = PythonOperator(
      task_id='check_score_anomalies',
      python_callable=check_score_anomalies,
      dag=dag
  )

  t4 = PythonOperator(
      task_id='export_to_analytics_db',
      python_callable=export_to_analytics_db,
      dag=dag
  )

  # Optional: Send email report
  t5 = EmailOperator(
      task_id='send_weekly_report',
      to=['data_team@snakegame.com'],
      subject='Snake Game Weekly Report',
      html_content="""
      <h3>Snake Game Data Pipeline Report</h3>
      <p>Weekly statistics for the Snake Game leaderboard.</p>
      <p>Check Airflow UI for detailed metrics.</p>
      """,
      dag=dag,
      trigger_rule='all_success'
  )

  # Set dependencies
  t1 >> [t2, t3] >> t4 >> t5
  ```

  4. Create the DAG files in airflow/dags/

  5. Start the system, update run.sh
    ```bash
    docker-compse up -d
    ```
  6. Initialize Airflow (first time only)
  ```bash
   docker-compose run airflow-webserver airflow db init
     docker-compose run airflow-webserver airflow users create \
         --username admin --password admin --firstname Admin \
         --lastname User --role Admin --email admin@example.com
  ```

  **Setup Cloud Backup (If needed)**
  ```python
  from datetime import datetime, timedelta
  from airflow import DAG
  from airflow.operators.bash import BashOperator
  from airflow.operators.python import PythonOperator
  import boto3
  from pathlib import Path

  default_args = {
      'owner': 'data_engineer',
      'depends_on_past': False,
      'start_date': datetime(2024, 1, 1),
      'retries': 2,
      'retry_delay': timedelta(minutes=5)
  }

  def upload_to_s3():
      """Upload scores database to S3 backup"""
      s3_client = boto3.client(
          's3',
          aws_access_key_id=Variable.get('aws_access_key'),
          aws_secret_access_key=Variable.get('aws_secret_key')
      )

      bucket_name = 'snake-game-backups'
      file_name = f'scores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'

      s3_client.upload_file(
          '/opt/airflow/scores.db',
          bucket_name,
          f'backups/{file_name}'
      )

      # Clean up old backups (keep last 30 days)
      # Implementation for cleanup...

  dag = DAG(
      'snake_game_cloud_backup',
      default_args=default_args,
      description='Backup scores to cloud storage',
      schedule_interval='@daily',
      catchup=False
  )

  backup_task = PythonOperator(
      task_id='upload_to_s3',
      python_callable=upload_to_s3,
      dag=dag
  )
  ```

  **Initialize Airflow**
  ```bash
    # Start all services
    docker-compose up -d postgres redis

    # Wait for postgres to be ready
    sleep 10

    # Initialize Airflow database
    docker-compose run airflow-webserver airflow db init

    # Create admin user
    docker-compose run airflow-webserver airflow users create \
        --username admin \
        --password admin \
        --firstname Snake \
        --lastname Game \
        --role Admin \
        --email admin@snakegame.com

    # Start all Airflow services
    docker-compose up -d
  ```

  7. Access Airflow UI
  ```bash
  UI at https://localhost:8080
  Username: admin
  Password: admin
  ```

  ** Update score_api.py
  ```python
    from datetime import datetime
    import sqlite3
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    def init_db():
        conn = sqlite3.connect('scores.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                game_version TEXT DEFAULT '1.0',
                deduplicated BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    @app.route('/score', methods=['POST'])
    def add_score():
        data = request.json
        player_name = data.get('player_name')
        score = data.get('score')

        conn = sqlite3.connect('scores.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scores (player_name, score, timestamp) VALUES (?, ?, ?)",
            (player_name, score, datetime.now())
        )
        conn.commit()
            conn.close()

            return jsonify({"message": "Score added successfully"}), 201

        # Rest of your existing code...
    ```
  ** Monitoring Script
  Create ```bash
  scripts/monitor_airflow.sh
  ```

  ```bash
    #!/bin/bash

    echo "=== Airflow Pipeline Status ==="
    echo "Webserver: http://localhost:8080"
    echo ""

    echo "Recent DAG Runs:"
    docker exec airflow-webserver airflow dags list-runs -d snake_game_data_pipeline -o table

    echo ""
    echo "Task Instances (last hour):"
    docker exec airflow-webserver airflow tasks list snake_game_data_pipeline --tree

    echo ""
    echo "Database Stats:"
    sqlite3 scores.db "SELECT COUNT(*) as total_scores, COUNT(DISTINCT player_name) as unique_players FROM scores;"
  ```

  8. Turn ON the DAG (toggle button next to 'snake_game_data_pipeline')

- Push to cloud storage: after the game is closed, automatically upload scores.db to S3 or Google Cloud Storage.
## Add a Desktop short-cut with icon
**Create $HOME/.local/share/applications/snake-game.desktop with:**
```bash
Version=1.0
Name=Snake Game
Comment=Play the Snake Game in a Docker container
Exec=gnome-terminal --working-directory=$HOME/Desktop/sneak -- bash -c "./run.sh; echo 'Press Enter to exit...'; read"
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Game;
StartupNotify=true
```

**Update the script**
```bash
update-desktop-database ~/.local/share/applications/
# Change ownership
chmod +x ~/.local/share/applications/snake-game.desktop
```

**Add a Desktop short-cut with icon**
```bash
cp ~/.local/share/applications/snake-game.desktop ~/Desktop/
# Test run
gtk-launch snake-game.desktop
```
Replace gnome-terminal with xterm if needed. Place a custom snake-icon.png in ~/.local/share/icons/.

**Update the desktop database:**
```bash
update-desktop-database ~/.local/share/applications/
chmod +x ~/.local/share/applications/snake-game.desktop
```

**Add a Desktop shortcut:**
```bash
cp ~/.local/share/applications/snake-game.desktop ~/Desktop/
# Test run
gtk-launch snake-game.desktop
```
## Docker Cleanup
### Deep clean of Docker resources
docker system prune -a && docker volume prune

### Or use the alias (add to ~/.bashrc)
alias docker-clean='docker system prune -a && docker volume prune'

## For Data Engineer
```bash
- Replace SQLite with PostgreSQL - Add Docker Compose service for Postgres

- Add data pipeline - Write scores to raw log table, create scheduled aggregations

- Implement ETL script - Export scores to CSV/Parquet or load to analytics DB

- Add metrics/monitoring - Track scores per hour, average score via /stats endpoint

- Containerize with Airflow - Create DAGs for deduplication and analytics

- Cloud storage integration - Auto-upload scores.db to S3/GCS
```

## For ML/AI Engineer
```bash
For ML / AI Engineer

- Train RL agent - Use reinforcement learning to train a better snake AI

- Deploy model API - Serve pre-trained models with Docker

- Model retraining pipeline - Trigger retraining when new scores arrive

- Compare AI strategies - Implement and benchmark different pathfinding algorithms
```

## Note
- Human and AI move at the same speed (same FPS)

Both snakes score 1.5 points per food (keeps competition fair)

AI uses BFS for optimal pathfinding - it's quite challenging!

To make the AI easier, add random movement or longer path selection
