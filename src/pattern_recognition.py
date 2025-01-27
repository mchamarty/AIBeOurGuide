import pandas as pd
import numpy as np
import json
import networkx as nx
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import shap
from typing import Dict, List, Tuple, Union
import os
from datetime import datetime, timedelta

# Download necessary NLTK resources
nltk.download('vader_lexicon')


class WorkflowPatternRecognizer:
    def __init__(self, focus_metrics: List[str] = None):
        self.scaler = StandardScaler()
        self.model = XGBClassifier(n_estimators=100)
        self.sia = SentimentIntensityAnalyzer()
        self.graph = nx.Graph()
        self.focus_metrics = focus_metrics or [
            'task_repetition_score',
            'workflow_complexity',
            'data_structure_score',
            'communication_frequency',
            'average_sentiment',
            'stakeholder_dependency',
            'time_spread'
        ]
    
    def extract_features(self, data: Dict) -> pd.DataFrame:
        features = []
        department_data = data.get('department_data', {})
        
        for dept_name, dept in department_data.items():
            if isinstance(dept, dict):
                features.append(self._extract_department_features(dept, dept_name))
        
        return pd.DataFrame(features) if features else pd.DataFrame()
    
    def _extract_department_features(self, dept: Dict, dept_name: str) -> Dict:
        tasks = []
        documents = []
        communications = {'emails': [], 'chats': []}
        
        if 'tasks' in dept:
            tasks.extend(dept['tasks'])
        if 'documents' in dept:
            documents.extend(dept['documents'])
        if 'communications' in dept:
            communications['emails'].extend(dept['communications'].get('emails', []))
            communications['chats'].extend(dept['communications'].get('chats', []))
        
        for team in dept.get('teams', []):
            tasks.extend(team.get('tasks', []))
            documents.extend(team.get('documents', []))
            communications['emails'].extend(team.get('communications', {}).get('emails', []))
            communications['chats'].extend(team.get('communications', {}).get('chats', []))
        
        for project in dept.get('projects', []):
            tasks.extend(project.get('goals', []))
            if 'project_documents_and_contents' in project:
                documents.append(project['project_documents_and_contents'])
            communications['emails'].extend(project.get('communications', {}).get('emails', []))
            communications['chats'].extend(project.get('communications', {}).get('chats', []))
        
        workflow = {
            'tasks': tasks,
            'documents': documents,
            'communications': communications
        }
        
        return self._extract_workflow_features(workflow, dept_name)

    def _extract_workflow_features(self, workflow: Dict, dept_name: str) -> Dict:
        all_metrics = {
            'department_name': dept_name,
            'task_repetition_score': len(workflow['tasks']),
            'workflow_complexity': len(workflow['tasks']) * 2,
            'data_structure_score': len(workflow['documents']),
            'communication_frequency': len(workflow['communications'].get('emails', [])) + len(workflow['communications'].get('chats', [])),
            'average_sentiment': self._analyze_sentiment(workflow['communications']),
            'stakeholder_dependency': self._analyze_graph_dependency(workflow['communications']),
            'time_spread': self._analyze_time_distribution(workflow['communications'])
        }
        return {k: v for k, v in all_metrics.items() if k in self.focus_metrics}
    
    def _analyze_sentiment(self, communications: Dict) -> float:
        sentiments = []
        for chat in communications.get('chats', []):
            if 'content' in chat and chat['content'].strip():
                sentiments.append(self.sia.polarity_scores(chat['content'])['compound'])
        for email in communications.get('emails', []):
            if 'content' in email and email['content'].strip():
                sentiments.append(self.sia.polarity_scores(email['content'])['compound'])
        return np.mean(sentiments) if sentiments else 0.0
    
    def _analyze_graph_dependency(self, communications: Dict) -> float:
        self.graph.clear()
        for email in communications.get('emails', []):
            if email.get('recipients'):
                self.graph.add_edge(email['sender'], email['recipients'][0])
        for chat in communications.get('chats', []):
            if chat.get('recipients'):
                self.graph.add_edge(chat['sender'], chat['recipients'][0])
        centrality = nx.degree_centrality(self.graph)
        return np.mean(list(centrality.values())) if centrality else 0.0
    
    def _analyze_time_distribution(self, communications: Dict) -> float:
        timestamps = []
        for email in communications.get('emails', []):
            if 'timestamp' in email:
                timestamps.append(datetime.fromisoformat(email['timestamp']))
        for chat in communications.get('chats', []):
            if 'timestamp' in chat:
                timestamps.append(datetime.fromisoformat(chat['timestamp']))
        
        if len(timestamps) < 2:
            return 0.0
        
        time_diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
        return np.mean(time_diffs)


# Example Usage
if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, '../data/data_formatted.json')
    output_path = os.path.join(base_path, '../data/results_data.json')
    
    with open(data_path) as f:
        data = json.load(f)
    
    recognizer = WorkflowPatternRecognizer()
    features = recognizer.extract_features(data)
    
    results = {
        "metrics_table": features.to_dict(orient='records'),
        "input_summary": {
            "total_departments": len(data.get('department_data', {})),
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Results exported to results_data.json.")
