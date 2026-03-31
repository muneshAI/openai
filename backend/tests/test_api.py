from datetime import date


def register_and_login(client):
    payload = {'email': 'fit@example.com', 'password': 'StrongPass1!', 'timezone': 'UTC'}
    client.post('/auth/register', json=payload)
    token = client.post('/auth/login', json={'email': payload['email'], 'password': payload['password']}).json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_workout_flow_and_score(client):
    headers = register_and_login(client)
    response = client.post(
        '/workouts',
        json={
            'date': str(date.today()),
            'type': 'P90X',
            'duration': 45,
            'intensity': 4,
            'calories': 380,
            'notes': 'Felt strong',
            'completed': True,
        },
        headers=headers,
    )
    assert response.status_code == 200

    dashboard = client.get('/score/dashboard', headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()['workout_done_today'] is True

    score = client.get('/score', headers=headers)
    assert score.status_code == 200
    assert score.json()['score'] >= 5


def test_reminder_settings_update(client):
    headers = register_and_login(client)
    response = client.put(
        '/reminders/settings',
        json={'reminders_enabled': False, 'reminder_time': '07:30:00', 'timezone': 'America/New_York'},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()['reminders_enabled'] is False
