import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your frontend to make requests to the API
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define the fraud parameter model with an id field
class FraudParameter(BaseModel):
    id: int
    parameter: str
    description: str
    example: str

    class Config:
        orm_mode = True
        # Ensures id is excluded from request body for POST and PUT, while it's included in the response.

class FraudParameterNonID(BaseModel):
    parameter: str
    description: str
    example: Optional[str] = None

    class Config:
        orm_mode = True

# Load the fraud parameters from the JSON file
def load_fraud_parameters():
    try:
        with open("./fraud_parameters.json", "r") as f:
            return json.load(f)  # This returns a list of dictionaries
    except FileNotFoundError:
        return []

# Save the fraud parameters to the JSON file
def save_fraud_parameters(parameters):
    with open("./fraud_parameters.json", "w") as f:
        json.dump(parameters, f, indent=4)

# Endpoint to get fraud parameters
@app.get("/fraud_parameters", response_model=List[FraudParameter])
async def get_fraud_parameters():
    parameters = load_fraud_parameters()
    return parameters

# Add a new fraud parameter
@app.post("/fraud_parameters", response_model=FraudParameterNonID)
async def add_fraud_parameter(param: FraudParameterNonID):
    parameters = load_fraud_parameters()
    new_id = max([p['id'] for p in parameters], default=0) + 1
    param_dict = param.dict()
    param_dict['id'] = new_id
    parameters.append(param_dict)
    save_fraud_parameters(parameters)
    return param_dict

# Edit an existing fraud parameter
@app.put("/fraud_parameters/{param_id}", response_model=FraudParameterNonID)
async def edit_fraud_parameter(param_id: int, param: FraudParameterNonID):
    parameters = load_fraud_parameters()
    existing_param = next((p for p in parameters if p['id'] == param_id), None)
    if not existing_param:
        raise HTTPException(status_code=404, detail="Parameter not found")
    
    # Update without overwriting id
    updated_data = param.dict(exclude_unset=True)
    existing_param.update(updated_data)
    save_fraud_parameters(parameters)
    return existing_param

# Remove a fraud parameter
@app.delete("/fraud_parameters/{param_id}")
async def remove_fraud_parameter(param_id: int):
    parameters = load_fraud_parameters()
    
    # Find the parameter by id
    parameter_to_delete = next((p for p in parameters if p['id'] == param_id), None)
    if not parameter_to_delete:
        raise HTTPException(status_code=404, detail="Parameter not found")
    
    # Delete the parameter
    parameters = [p for p in parameters if p['id'] != param_id]
    save_fraud_parameters(parameters)
    return {"message": "Parameter removed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)