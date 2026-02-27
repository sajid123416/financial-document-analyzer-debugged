## Importing libraries and files
import os
from dotenv import load_dotenv

from pypdf import PdfReader

load_dotenv()


"""
Utility tools used by the CrewAI agents.

The main tool used by the crew is `FinancialDocumentTool.read_data_tool`,
which loads and cleans text from a PDF so that the LLM can analyse it.
"""


class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path: str = "data/TSLA-Q2-2025-Update.pdf") -> str:
        """Read and clean text from a PDF file.

        Args:
            path (str, optional): Path of the PDF file.
                Defaults to 'data/TSLA-Q2-2025-Update.pdf'.

        Returns:
            str: Concatenated and lightly cleaned text content of the PDF.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"PDF file not found at path: {path}")

        reader = PdfReader(path)

        full_report = ""
        for page in reader.pages:
            content = page.extract_text() or ""

            # Normalize multiple blank lines
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content.strip() + "\n"

        return full_report.strip()


class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data: str) -> str:
        """Placeholder investment analysis tool.

        Currently this simply normalises whitespace and returns a stub message.
        It can be extended later with real analysis logic if needed.
        """
        processed_data = financial_document_data

        # Clean up the data format (remove duplicate spaces)
        i = 0
        while i < len(processed_data):
            if processed_data[i : i + 2] == "  ":
                processed_data = processed_data[:i] + processed_data[i + 1 :]
            else:
                i += 1

        # TODO: Implement investment analysis logic using `processed_data`
        return "Investment analysis functionality to be implemented"


class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        """Placeholder risk assessment tool.

        Can be extended to create structured risk assessments from the document.
        """
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented"
