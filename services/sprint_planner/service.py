from services.sprint_planner.logic import generate_sprint_plan_results

def plan_sprint_service(input_data):
    tasks_list = [task.model_dump() for task in input_data.available_tasks]

    results = generate_sprint_plan_results(
        tasks=tasks_list,
        history=input_data.historical_velocity,
        capacity=input_data.team_capacity_raw
    )

    return results
