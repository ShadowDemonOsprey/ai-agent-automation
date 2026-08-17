"""
Knowledge search tool.

Searches the RAG knowledge base and returns the most
relevant document chunks for a query.
"""


from app.rag.service import knowledge_service


def knowledge_search(query: str) -> dict:
    """
    Retrieve relevant knowledge chunks.

    Args:
        query (str):
            Search question or keywords.

    Returns:
        dict:
            Search results or error.
    """

    try:

        result = knowledge_service.search(query)

        if result["result_count"] == 0:

            return {
                "tool": "knowledge_search",
                "query": query,
                "error": "No knowledge found. "
                         "Ingest documents first."
            }

        return {
            "tool": "knowledge_search",
            "query": query,
            "result_count": result["result_count"],
            "results": result["results"],
        }

    except Exception as error:

        return {
            "tool": "knowledge_search",
            "query": query,
            "error": f"Knowledge search failed: {error}",
        }
