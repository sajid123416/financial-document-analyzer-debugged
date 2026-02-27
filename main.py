from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document as analyze_financial_document_task

app = FastAPI(title="Financial Document Analyzer")


def run_crew(query: str, file_path: str = "data/TSLA-Q2-2025-Update.pdf"):
    """Run the analysis crew on the provided query and document path."""
    # NOTE: For simplicity the file_path is currently handled inside the tool
    # via its default argument. It can be threaded through explicitly later.
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document_task],
        process=Process.sequential,
    )

    result = financial_crew.kickoff(inputs={"query": query})
    return result


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(
        default="Analyze this financial document for investment insights"
    ),
):
    """Analyze financial document and provide comprehensive investment insights."""

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate query
        if not query:
            query = "Analyze this financial document for investment insights"

        # Process the financial document with the analysis crew
        response = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}",
        )

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                # Ignore cleanup errors
                pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
