from diet_service import Diet_service
from pydantic import BaseModel , Field
from typing import Literal, Annotated
from fastapi import FastAPI 


app=FastAPI(title="DIET PLANER API")


class Diet_request(BaseModel):
    age:Annotated[int,Field(gt=8,lt=120, title="Your Age", description="Age should be greater than 7")]
    height:Annotated[float, Field(title="Your height", description="height should be in meter ")]
    weight:Annotated[float,Field(gt=25,lt=300 , title="Your weight", description="weight should be greater than 25")]
    goal:Annotated[Literal["cut", "bulk", 'maintain'], Field(title="Goal", description="select your goal")]
    


@app.get("/")
def home():
    return {"message": "Welcome to diet planner API"}


@app.get("/health")
def health():
    return {"Status":"ok","messege":"API in running"}

@app.post("/diet-plan")
def diet_plan(user:Diet_request):
    service=Diet_service(user)

    return {
        "success": True,
        "data":{
            "age":user.age,
            "goal":user.goal,
            "bmi":round(service.bmi(),2),
            "calories":round(service.calories()),
            "protein":round(service.protein(),1),
            "Diet_chart":service.diet_chart()


        }
    }
