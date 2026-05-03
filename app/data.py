from datetime import datetime

services = [
    {
        "id": 1,
        "name": "Authentication Service",
        "description": "Handles user authentication and token validation.",
        "owner": "Platform Team",
        "status": "healthy",
        "updated_at": datetime.utcnow(),
    },
    {
        "id": 2,
        "name": "Payments Service",
        "description": "Processes payment requests and billing events.",
        "owner": "Payments Team",
        "status": "degraded",
        "updated_at": datetime.utcnow(),
    },
    {
        "id": 3,
        "name": "Notifications Service",
        "description": "Sends email and webhook notifications.",
        "owner": "Messaging Team",
        "status": "down",
        "updated_at": datetime.utcnow(),
    },
]

incidents = [
    {
        "id": 1,
        "service_id": 2,
        "title": "Increased response latency",
        "description": "Payment requests are slower than expected due to external provider delays.",
        "severity": "medium",
        "resolved": False,
        "created_at": datetime.utcnow(),
    },
    {
        "id": 2,
        "service_id": 3,
        "title": "Notification queue unavailable",
        "description": "The notification worker cannot process pending jobs.",
        "severity": "high",
        "resolved": False,
        "created_at": datetime.utcnow(),
    },
]