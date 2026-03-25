from dotenv import load_dotenv
from langchain.globals import set_verbose, set_debug
from langchain_groq.chat_models import ChatGroq
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, BASE_PROJECT_ROOT, list_file

_ = load_dotenv()

set_debug(True)
set_verbose(True)

llm = ChatGroq(model="openai/gpt-oss-120b")


# 🧠 PLANNER
def planner_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]

    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )

    project_name = resp.name.replace(" ", "_").lower()
    project_root = BASE_PROJECT_ROOT / project_name
    project_root.mkdir(parents=True, exist_ok=True)

    return {
        "plan": resp,
        "project_root": str(project_root)
    }


# 🧠 ARCHITECT
def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"]

    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )

    if resp is None:
        raise ValueError("Architect failed")

    resp.plan = plan
    print(resp.model_dump_json())

    return {
        "task_plan": resp,
        "project_root": state["project_root"]  # ✅ KEEP IT
    }


# 🧠 CODER
def coder_agent(state: dict) -> dict:
    coder_state: CoderState = state.get("coder_state")

    if coder_state is None:
        coder_state = CoderState(
            task_plan=state["task_plan"],
            current_step_idx=0,
            project_root=state["project_root"]  # ✅ IMPORTANT
        )

    steps = coder_state.task_plan.implementation_steps

    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]

    # ✅ FIXED read_file call
    existing_content = read_file.run({
        "path": current_task.filepath,
        "project_root": coder_state.project_root
    })

    system_prompt = coder_system_prompt()

    # ✅ VERY IMPORTANT: pass project_root in prompt
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Project root: {coder_state.project_root}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content, project_root) to save your changes."
    )

    coder_tools = [read_file, write_file, list_file]

    react_agent = create_react_agent(llm, coder_tools)

    react_agent.invoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    })

    coder_state.current_step_idx += 1

    return {"coder_state": coder_state}


# 🔁 GRAPH
graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")

agent = graph.compile()


if __name__ == "__main__":
    result = agent.invoke(
        {"user_prompt": "Build a colourful modern todo app in html css and js"},
        {"recursion_limit": 100}
    )
    print("Final State:", result)