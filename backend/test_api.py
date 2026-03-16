import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_health():
    print("Testing /health endpoint...")
    response = requests.get(f'{BASE_URL}/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_explain():
    print("Testing /explain endpoint...")
    payload = {
        'subject': 'Physics',
        'topic': 'Newton\'s First Law',
        'level': 'beginner'
    }
    response = requests.post(f'{BASE_URL}/explain', json=payload)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Session ID: {data['session_id']}")
        print(f"\nLearning Goal:\n{data['learning_goal']}")
        print(f"\nExplanation:\n{data['explanation'][:200]}...")
        print(f"\nSummary:\n{data['summary']}")
        print(f"\nQuiz Questions: {len(data['quiz'])}")
        for i, q in enumerate(data['quiz'], 1):
            print(f"\n  Q{i}: {q['question']}")
        print()
        return data['session_id']
    else:
        print(f"Error: {response.text}")
        return None

def test_adapt(session_id):
    print("Testing /adapt endpoint...")
    payload = {
        'session_id': session_id,
        'feedback': 'simpler'
    }
    response = requests.post(f'{BASE_URL}/adapt', json=payload)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nAdapted Explanation:\n{data['explanation'][:200]}...")
        print(f"\nUpdated Summary:\n{data['summary']}")
        print(f"\nUpdated Quiz Questions: {len(data['quiz'])}")
        print()
    else:
        print(f"Error: {response.text}")

if __name__ == '__main__':
    print("=" * 60)
    print("AdaptEd Backend API Test")
    print("=" * 60)
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("Start it with: python app.py")
    print("\nStarting tests in 3 seconds...")
    print("=" * 60)
    print()

    time.sleep(3)

    try:
        test_health()
        session_id = test_explain()

        if session_id:
            test_adapt(session_id)

        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to the server.")
        print("Make sure the Flask server is running: python app.py")
    except Exception as e:
        print(f"ERROR: {str(e)}")
