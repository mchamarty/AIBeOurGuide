import pytest
import json
from src.pattern_recognition import WorkflowPatternRecognizer
from datetime import datetime, timedelta
import random

def generate_test_data():
    """Generate synthetic test data aligned with real enterprise sources."""
    now = datetime.now()
    
    return {
        'department_data': [
            {
                'name': 'Engineering',
                'tasks': [
                    {
                        'actions': ['code', 'review', 'deploy'],
                        'input_types': ['requirements'],
                        'output_types': ['software'],
                        'status': 'completed'
                    }
                ],
                'documents': [
                    {
                        'type': 'technical_doc',
                        'structured_fields': ['title', 'content', 'version']
                    }
                ],
                'communications': {
                    'emails': [
                        {
                            'sender': 'eng1',
                            'recipients': ['eng2', 'eng3'],
                            'content': 'Code review completed for module X.',
                            'timestamp': (now - timedelta(days=1)).isoformat()
                        },
                        {
                            'sender': 'eng2',
                            'recipients': ['eng1'],
                            'content': 'Deployment scheduled for tonight.',
                            'timestamp': now.isoformat()
                        }
                    ],
                    'chats': [
                        {
                            'sender': 'eng2',
                            'recipients': ['eng1'],
                            'content': 'Quick sync on deployment steps.',
                            'timestamp': now.isoformat()
                        },
                        {
                            'sender': 'eng3',
                            'recipients': ['eng1', 'eng2'],
                            'content': 'Should we include module Y?',
                            'timestamp': (now - timedelta(hours=2)).isoformat()
                        }
                    ]
                }
            },
            {
                'name': 'Product',
                'tasks': [
                    {
                        'actions': ['design', 'validate', 'document'],
                        'input_types': ['market_research'],
                        'output_types': ['specifications'],
                        'status': 'in-progress'
                    }
                ],
                'documents': [
                    {
                        'type': 'product_doc',
                        'structured_fields': ['title', 'content', 'status']
                    }
                ],
                'communications': {
                    'emails': [
                        {
                            'sender': 'pm1',
                            'recipients': ['pm2'],
                            'content': 'Market research finalized.',
                            'timestamp': (now - timedelta(days=2)).isoformat()
                        }
                    ],
                    'chats': [
                        {
                            'sender': 'pm2',
                            'recipients': ['eng1', 'eng3'],
                            'content': 'Can you review the latest spec doc?',
                            'timestamp': now.isoformat()
                        }
                    ]
                }
            }
        ]
    }

# -------------------------------
# Test Feature Extraction
# -------------------------------
def test_feature_extraction():
    """Test if features are extracted correctly."""
    data = generate_test_data()
    recognizer = WorkflowPatternRecognizer()
    features = recognizer.extract_features(data)
    
    assert len(features) == 2, "Feature extraction should return data for two departments."
    assert all(col in features.columns for col in [
        'task_repetition_score',
        'workflow_complexity',
        'data_structure_score',
        'communication_frequency',
        'average_sentiment',
        'stakeholder_dependency',
        'time_spread'
    ]), "All expected feature columns should be present."

    assert features['task_repetition_score'].iloc[0] > 0, "Task repetition score should be positive."

# -------------------------------
# Test Model Training and Prediction
# -------------------------------
def test_model_training():
    """Test if the model trains without errors."""
    data = generate_test_data()
    labels = [1, 0]  # Engineering: AI-ready, Product: Not ready
    
    recognizer = WorkflowPatternRecognizer()
    recognizer.train(data, labels)
    predictions = recognizer.predict(data)
    
    assert len(predictions) == 2, "Prediction output should match the number of departments."
    assert set(predictions).issubset({0, 1}), "Predictions should only contain 0 or 1."

# -------------------------------
# Test Sentiment Analysis
# -------------------------------
def test_sentiment_analysis():
    """Test if sentiment analysis runs without errors."""
    data = generate_test_data()
    recognizer = WorkflowPatternRecognizer()
    
    dept = data['department_data'][0]
    sentiment = recognizer._analyze_sentiment(dept['communications'])
    
    assert isinstance(sentiment, float), "Sentiment analysis should return a float value."
    assert -1.0 <= sentiment <= 1.0, "Sentiment value should be between -1.0 and 1.0."

# -------------------------------
# Test Graph Dependency
# -------------------------------
def test_graph_dependency():
    """Test if graph dependency analysis works."""
    data = generate_test_data()
    recognizer = WorkflowPatternRecognizer()
    
    dept = data['department_data'][0]
    dependency = recognizer._analyze_graph_dependency(dept['communications'])
    
    assert isinstance(dependency, float), "Graph dependency should return a float value."
    assert dependency >= 0.0, "Dependency score should be non-negative."

# -------------------------------
# Test Time Distribution
# -------------------------------
def test_time_distribution():
    """Test time distribution analysis."""
    data = generate_test_data()
    recognizer = WorkflowPatternRecognizer()
    
    dept = data['department_data'][0]
    time_spread = recognizer._analyze_time_distribution(dept['communications'])
    
    assert isinstance(time_spread, float), "Time distribution should return a float value."
    assert time_spread >= 0.0, "Time spread should be non-negative."
