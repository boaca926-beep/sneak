"""
Data Quality Rule Engine for Snake Game Scores
Monitors data quality metrics and enforces governance rules
"""

import re
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass  # Simple data holder
class QualityRule:
    """Data quality rule definition"""

    name: str
    description: str
    severity: Severity
    check_type: str  # completeness, uniqueness, consistency, accuracy, timeliness
    query: str
    threshold: float
    active: bool = True


@dataclass  # Simple data holder
class QualityResult:
    """Result of quality rule execution"""

    rule_name: str
    passed: bool
    score: float
    threshold: float
    severity: str
    message: str
    timestamp: datetime
    affected_rows: int = 0


# Service / orchestrator class, containing behavior and logic
class DataQualityChecker:
    """Main data quality monitoring system"""

    def __init__(self, db_path: str = "scores.db"):
        self.db_path = db_path
        self.quality_history_table = "quality_checks_history"
        self._init_history_table()

        # Load quality rules
        self.rules = self._load_default_rules()

    def _init_history_table(self):
        """Initialize table to store quality check history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.quality_history_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rule_name TEXT,
                passed BOOLEAN,
                score REAL,
                threshold REAL,
                severity TEXT,
                message TEXT,
                affected_rows INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def _load_default_rules(self) -> List[QualityRule]:
        """Load default data quality rules"""
        rules = [
            QualityRule(
                name="completeness_player_name",
                description="Player name should never be NULL or empty",
                severity=Severity.CRITICAL,
                check_type="completeness",
                query="""
                    SELECT COUNT(*) as total,
                        SUM(CASE WHEN player_name IS NULL OR player_name = 'Player' THEN 1 ELSE 0 END) as null_count
                    FROM scores
                """,
                threshold=0.95,  # 95% completeness required
            )
        ]
        return rules

    def load_rules_from_yaml(self, yaml_path: str):
        """Load quality rules from YAML configuration"""
        pass

    def execute_rule(self, rule: QualityRule) -> QualityResult:
        """Execute a single quality rule"""
        if not rule.active:
            return QualityResult(
                rule_name=rule.name,
                passed=True,
                score=1.0,
                threshold=rule.threshold,
                severity=rule.severity.value,
                message="Rule inactive - skipped",
                timestamp=datetime.now(),
            )

        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(rule.query, conn)
            conn.close()

            if len(df) == 0:
                score = 1.0
                affected_rows = 0
                passed = score >= rule.threshold
            else:
                total = df.iloc[0]["total"]
                invalid = df.iloc[0].get("null_count", 0)

                affected_rows = invalid if "invalid" in locals() else 0
                valid = total - invalid if total > 0 else 0
                score = valid / total if total > 0 else 1.0
                passed = score >= rule.threshold

            message = f"Quality score: {score:.2%} (threshold: {rule.threshold:.2%})"
            if not passed:
                message += f" - {affected_rows} records affected"

            return QualityResult(
                rule_name=rule.name,
                passed=passed,
                score=score,
                threshold=rule.threshold,
                severity=rule.severity.value,
                message=message,
                timestamp=datetime.now(),
                affected_rows=affected_rows,
            )

        except Exception as e:
            logger.error(f"Error executing rule {rule.name}: {e}")
            return QualityResult(
                rule_name=rule.name,
                passed=False,
                score=0.0,
                threshold=rule.threshold,
                severity=rule.severity.value,
                message=f"Error: {e}",
                timestamp=datetime.now(),
            )

    def run_all_checks(self) -> List[QualityResult]:
        """Execute all active quality rules"""
        results = []

        for rule in self.rules:
            logger.info(f"Executing rule: {rule.name}")
            result = self.execute_rule(rule)
            results.append(result)

            # Store to history
            self._store_result(result)

            # Log alert for crtical failures
            if not result.passed and result.severity == Severity.CRITICAL.value:
                self._send_alert(result)

        return results

    def _store_result(self, result: QualityResult):
        """Store quality check result in history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {self.quality_history_table}
            (rule_name, passed, score, threshold, severity, message, affected_rows, check_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                result.rule_name,
                result.passed,
                result.score,
                result.threshold,
                result.severity,
                result.message,
                result.affected_rows,
                result.timestamp,
            ),
        )
        conn.commit()
        conn.close()

    def _send_alert(self, result: QualityResult):
        """Send alert for critical quality failures"""
        pass

    def get_quality_summary(self, days: int = 7) -> Dict:
        """Get quality summary for last N days"""
        pass

    def _calculate_trend(self) -> str:
        """Calculate quality trend"""
        pass
