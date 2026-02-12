"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import os
from pathlib import Path
from datetime import datetime, timezone

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.get("/xmgr/export-package")
def export_package(package_name: str = "activities_package"):
    """
    Export activities as a package using XMGR format.
    
    This endpoint exports all activities data as a structured package
    that can be imported or transferred to other systems.
    
    Args:
        package_name: Name of the package to export (default: "activities_package")
    
    Returns:
        JSON response containing the exported package with metadata
    """
    # Create package metadata
    export_data = {
        "package_name": package_name,
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "format": "XMGR",
        "total_activities": len(activities),
        "activities": activities
    }
    
    # Return the package as JSON
    return JSONResponse(
        content=export_data,
        status_code=200,
        headers={
            "X-Package-Name": package_name,
            "X-Export-Format": "XMGR"
        }
    )
