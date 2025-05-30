"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

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
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu", "amelia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Participate in plays and improve your acting skills",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["charlotte@mergington.edu", "harper@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["elijah@mergington.edu", "james@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["benjamin@mergington.edu", "lucas@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn and practice tennis with fellow students",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["grace@mergington.edu", "henry@mergington.edu"]
    },
    "Swimming Team": {
        "description": "Join the swimming team and compete in swim meets",
        "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["ella@mergington.edu", "jackson@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn photography techniques and capture amazing moments",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["scarlett@mergington.edu", "logan@mergington.edu"]
    },
    "Music Band": {
        "description": "Play instruments and perform in the school band",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["zoe@mergington.edu", "nathan@mergington.edu"]
    },
    "Debate Club": {
        "description": "Engage in debates and improve public speaking skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["hannah@mergington.edu", "samuel@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build robots and participate in robotics competitions",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["leo@mergington.edu", "chloe@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


def validate_student_email(email: str) -> bool:
    """Validate that the email belongs to a Mergington student."""
    return email.lower().endswith("@mergington.edu")


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate email format
    if not validate_student_email(email):
        raise HTTPException(status_code=400, detail="Invalid student email domain. Must use @mergington.edu")
    
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    
    # Persist to database if using MongoDB
    if USE_DATABASE:
        try:
            activities_collection.update_one(
                {"_id": activity_name},
                {"$push": {"participants": email}}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database update failed: {str(e)}")
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate email format
    if not validate_student_email(email):
        raise HTTPException(status_code=400, detail="Invalid student email domain. Must use @mergington.edu")
        
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    # Remove student
    activity["participants"].remove(email)
    try:
        activities_collection.update_one(
            {"_id": activity_name},
            {"$pull": {"participants": email}}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database update failed: {str(e)}")
    
    return {"message": f"Unregistered {email} from {activity_name}"}


# Optional: Add a database switch
USE_DATABASE = False  # Set to True to use MongoDB

if USE_DATABASE:
    from pymongo import MongoClient

    client = MongoClient("mongodb://localhost:27017/")
    db = client["mergington"]
    activities_collection = db["activities"]

    # Replace in-memory activities with database logic
    def get_activities_from_db():
        return {activity["_id"]: activity for activity in activities_collection.find()}

    activities = get_activities_from_db()
