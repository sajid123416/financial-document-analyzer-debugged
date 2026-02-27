## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier
from tools import FinancialDocumentTool

"""
Task definitions for the Financial Document Analyzer.

These tasks coordinate how the agents should use the PDF reading tool and how
they should structure their responses.
"""


# Main analysis task used by the API
analyze_financial_document = Task(
    description=(
        "Carefully read the financial document provided via the tool and the "
        "user's question: {query}. Based on the contents of the document, "
        "summarise the company's financial position, key performance drivers, "
        "and any notable trends or risks. Always explain your reasoning and "
        "avoid giving personalised investment advice."
    ),
    expected_output=(
        "A clear, structured analysis that includes:\n"
        "- A short overview of the document and what period it covers\n"
        "- Key financial highlights (revenue, profitability, cash flow, etc.)\n"
        "- Important qualitative information (strategy, guidance, major events)\n"
        "- A balanced discussion of risks and uncertainties\n"
        "- A concise conclusion summarising the overall picture"
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)


investment_analysis = Task(
    description=(
        "Using the insights from the financial document and the user's query "
        "{query}, provide high‑level, educational commentary on how an "
        "investor might think about this company or situation. Do **not** "
        "give personalised recommendations; instead, discuss general factors "
        "that investors often consider."
    ),
    expected_output=(
        "A short, educational discussion that:\n"
        "- Highlights factors that can influence investment decisions\n"
        "- Mentions both potential opportunities and risks\n"
        "- Clearly states that this is not personal financial advice\n"
        "- Encourages the user to do further research or consult a "
        "qualified professional"
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)


risk_assessment = Task(
    description=(
        "From the perspective of a risk analyst, review the financial "
        "document and the user's query {query} to identify key risks, "
        "uncertainties and scenarios that could affect the company or "
        "situation described."
    ),
    expected_output=(
        "A structured risk assessment that:\n"
        "- Lists major risk categories (e.g., market, operational, financial)\n"
        "- Briefly explains each risk and what could drive it\n"
        "- Distinguishes between short‑term and long‑term considerations\n"
        "- Avoids exaggeration and focuses on balanced, realistic scenarios"
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)


verification = Task(
    description=(
        "Check whether the provided document appears to be a financial or "
        "business document suitable for analysis, and describe what kind of "
        "information it contains."
    ),
    expected_output=(
        "A brief verification note that:\n"
        "- States whether the document looks like a financial/business "
        "document\n"
        "- Mentions the main types of content it includes\n"
        "- Notes any limitations or concerns about using it for analysis"
    ),
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)
