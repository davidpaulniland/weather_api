from fastapi.testclient import TestClient
from app.main import app
import json


client = TestClient(app)

def setup_module(module):
    with open("data/sensors.json", "w") as f:
        json.dump([], f)


def test_post_and_query_average():
    client.post("/metrics", json={
        "sensor_id": "sensor_avg",
        "timestamp": "2025-03-29T12:00:00",
        "metrics": {"temperature": 20.0, "humidity": 50}
    })
    client.post("/metrics", json={
        "sensor_id": "sensor_avg",
        "timestamp": "2025-03-30T12:00:00",
        "metrics": {"temperature": 22.0, "humidity": 60}
    })
    response = client.get("/metrics", params=[
        ("sensors", "sensor_avg"),
        ("metrics", "temperature"),
        ("metrics", "humidity"),
        ("stat", "average"),
        ("start", "2025-03-29T00:00:00"),
        ("end", "2025-03-31T00:00:00")
    ])
    assert response.status_code == 200
    result = response.json()
    assert result["temperature"] == 21.0
    assert result["humidity"] == 55.0


def test_min_max_sum():
    client.post("/metrics", json={
        "sensor_id": "sensor_stats",
        "timestamp": "2025-03-29T10:00:00",
        "metrics": {"humidity": 40}
    })
    client.post("/metrics", json={
        "sensor_id": "sensor_stats",
        "timestamp": "2025-03-29T11:00:00",
        "metrics": {"humidity": 60}
    })

    for stat, expected in [("min", 40), ("max", 60), ("sum", 100)]:
        response = client.get("/metrics", params=[
            ("sensors", "sensor_stats"),
            ("metrics", "humidity"),
            ("stat", stat),
            ("start", "2025-03-29T00:00:00"),
            ("end", "2025-03-30T00:00:00")
        ])
        assert response.status_code == 200
        assert response.json()["humidity"] == expected


def test_date_range_no_results():
    response = client.get("/metrics", params=[
        ("sensors", "sensor_avg"),
        ("metrics", "temperature"),
        ("stat", "average"),
        ("start", "2020-01-01T00:00:00"),
        ("end", "2020-01-02T00:00:00")
    ])
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "No data found in the given range or filters."


def test_invalid_short_date_range():
    response = client.get("/metrics", params=[
        ("sensors", "sensor_avg"),
        ("metrics", "temperature"),
        ("stat", "average"),
        ("start", "2025-03-29T00:00:00"),
        ("end", "2025-03-29T01:00:00")
    ])
    assert response.status_code == 400
    assert "at least 1 day" in response.json()["detail"]


def test_invalid_stat_type():
    response = client.get("/metrics", params=[
        ("sensors", "sensor_avg"),
        ("metrics", "temperature"),
        ("stat", "median")
    ])
    assert response.status_code == 422


def test_post_invalid_metrics_type():
    response = client.post("/metrics", json={
        "sensor_id": "bad_sensor",
        "timestamp": "2025-03-29T12:00:00",
        "metrics": {"temperature": "hot"}
    })
    assert response.status_code == 422
