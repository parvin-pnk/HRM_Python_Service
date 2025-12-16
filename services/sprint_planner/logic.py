import pandas as pd
import numpy as np


def predict_velocity(history: np.ndarray):
    return np.mean(history)

def predict_success_rate(utilization: float):
    if utilization > 1.0: return 0.0
    
   
    optimal_utilization = 0.95
    success_rate = 1.0 - 0.7 * abs(utilization - optimal_utilization)
    
    return max(0.4, min(1.0, success_rate)) # Clamp between 40% and 100%

def plan_sprint_greedy(df: pd.DataFrame, capacity: float):
   
    df['value_density'] = df['priority'] / df['effort_hours']
    df_sorted = df.sort_values(by='value_density', ascending=False).reset_index(drop=True)
    
    planned_tasks = []
    current_load = 0
    
    for _, row in df_sorted.iterrows():
        if current_load + row['effort_hours'] <= capacity:
            planned_tasks.append(row)
            current_load += row['effort_hours']
            
    df_planned = pd.DataFrame(planned_tasks)
    utilization = current_load / capacity
    
    return df_planned, current_load, utilization



def generate_sprint_plan_results(tasks: list[dict], history: list[float], capacity: float) -> dict:
   
  
    history_array = np.array(history)
    df_tasks = pd.DataFrame(tasks)
    
   
    predicted_velocity = predict_velocity(history_array)
    
    sprint_capacity = min(capacity, predicted_velocity * 1.05) 
    
    
    df_sprint_plan, total_planned_effort, utilization = plan_sprint_greedy(df_tasks.copy(), sprint_capacity)
    
    predicted_success_rate_value = predict_success_rate(utilization)
    return {
        "planned_tasks": df_sprint_plan[['id', 'title', 'effort_hours']].to_dict('records'),
        "total_effort_planned": round(total_planned_effort, 2),
        "team_velocity_prediction": round(predicted_velocity, 2),
        "predicted_success_rate": round(predicted_success_rate_value * 100, 2)
    }
