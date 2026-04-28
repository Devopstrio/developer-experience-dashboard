import logging
import uuid
import time
import pandas as pd
import numpy as np

class MetricsEngine:
    def __init__(self):
        self.logger = logging.getLogger("metrics-engine")

    def calculate_dora_metrics(self, deployment_data: list, incident_data: list):
        """
        Calculates core DORA metrics from deployment and incident logs.
        """
        # Logic: Aggregate deployment counts and failure rates
        df_deploy = pd.DataFrame(deployment_data)
        df_inc = pd.DataFrame(incident_data)
        
        freq = len(df_deploy) / 30 # Daily frequency over a month
        cfr = (len(df_inc) / len(df_deploy)) * 100 if len(df_deploy) > 0 else 0
        
        return {
            "deployment_frequency": round(freq, 2),
            "change_failure_rate": f"{round(cfr, 2)}%",
            "maturity": "ELITE" if freq > 1 and cfr < 5 else "HIGH" if freq > 0.5 else "MEDIUM"
        }

    def detect_pr_bottlenecks(self, pr_data: list):
        """
        Identifies bottlenecks in the PR review process based on time-to-first-review and review cycles.
        """
        df = pd.DataFrame(pr_data)
        avg_wait = df["wait_time_hours"].mean()
        max_wait = df["wait_time_hours"].max()
        
        return {
            "avg_review_wait_hours": round(avg_wait, 2),
            "critical_bottlenecks": df[df["wait_time_hours"] > 24]["id"].tolist(),
            "recommendation": "Increase reviewer pool for Team A" if avg_wait > 8 else "Healthy"
        }

    def score_flow_efficiency(self, active_time_mins: int, wait_time_mins: int):
        """
        Calculates the ratio of active development time to total lead time.
        """
        total = active_time_mins + wait_time_mins
        if total <= 0:
            return 1.0
            
        efficiency = (active_time_mins / total) * 100
        return {
            "efficiency_percentage": round(efficiency, 2),
            "state": "FLOWING" if efficiency > 60 else "BLOCKED" if efficiency < 20 else "STALLED"
        }

    def predict_attrition_risk(self, sentiment_score: float, wip_count: int, meeting_hours: int):
        """
        Predicts team-level burnout or attrition risk using sentiment and load signals.
        """
        risk_score = (1 - sentiment_score) * 40 + (wip_count * 10) + (meeting_hours * 5)
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": "HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 40 else "LOW",
            "primary_driver": "Workload" if wip_count > 5 else "Sentiment" if sentiment_score < 0.5 else "None"
        }

if __name__ == "__main__":
    engine = MetricsEngine()
    
    # 1. DORA Metrics
    deploys = [{"id": 1, "status": "SUCCESS"}] * 50
    incidents = [{"id": 101, "severity": "HIGH"}] * 2
    print("DORA Metrics:", engine.calculate_dora_metrics(deploys, incidents))
    
    # 2. PR Bottlenecks
    prs = [{"id": "PR-1", "wait_time_hours": 4}, {"id": "PR-2", "wait_time_hours": 36}]
    print("Bottlenecks:", engine.detect_pr_bottlenecks(prs))
    
    # 3. Flow Efficiency
    print("Flow Efficiency:", engine.score_flow_efficiency(1200, 400))
    
    # 4. Attrition Risk
    print("Attrition Risk:", engine.predict_attrition_risk(0.8, 3, 12))
