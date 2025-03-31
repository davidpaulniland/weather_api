from datetime import datetime

def filter_and_aggregate(data, sensors, metrics, stat, start, end):
    parsed = []
    for row in data:
        if sensors and row["sensor_id"] not in sensors:
            continue
        ts = datetime.fromisoformat(row["timestamp"])
        parsed.append({**row, "parsed_ts": ts})

    if not start and not end and parsed:
        latest_ts = max(row["parsed_ts"] for row in parsed)
        parsed = [row for row in parsed if row["parsed_ts"] == latest_ts]

    filtered = []
    for row in parsed:
        ts = row["parsed_ts"]
        if start and ts < start:
            continue
        if end and ts > end:
            continue
        filtered.append(row)
    if not filtered:
        return {"message": "No data found in the given range or filters."}

    result = {}
    for metric in metrics:
        values = [row["metrics"].get(metric) for row in filtered if metric in row["metrics"]]
        if not values:
            result[metric] = None
        elif stat == "min":
            result[metric] = min(values)
        elif stat == "max":
            result[metric] = max(values)
        elif stat == "sum":
            result[metric] = sum(values)
        elif stat == "average":
            result[metric] = round(sum(values) / len(values), 2)

    return result
