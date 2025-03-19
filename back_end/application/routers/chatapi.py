from fastapi import APIRouter
from application.models import Chat
from application.testfile import execute_sql_query, get_sql_query,refine_response

router = APIRouter()

@router.post("/get-response")
def get_chat(chat: Chat):
    """
    Handles incoming natural language queries and returns a structured response.
    
    :param chat: User query in natural language
    :return: JSON response with structured query results
    """
    prompt = chat.prompt

    # Generate SQL query using LLM
    sql_query = get_sql_query(prompt)

    # Execute the query and fetch results
    query_result = execute_sql_query(sql_query)

    query_result=refine_response(prompt,query_result)


    # Return the structured response
    return {"query": sql_query, "response": query_result}
