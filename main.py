import json
import tempfile

from dotenv import load_dotenv
from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import Tone, ReportType
from leea_agent_sdk.context import ExecutionContext
from pydantic import BaseModel, Field
from typing import Type
import leea_agent_sdk.runtime as leea
from leea_agent_sdk.agent import Agent


class Input(BaseModel):
    query: str = Field(description="Query to research")
    tone: Tone = Field(default=Tone.Objective, description="Report tone")
    report_type: ReportType = Field(default=ReportType.ResearchReport, description="Type of report")
    language: str = Field(default='english', description="Language of the report")
    words_count: int = Field(description="Report words count")


class Output(BaseModel):
    report: str = Field(description="Report")


class InternetResearcher(Agent):
    name: str = "Internet researcher"
    description: str = "Makes internet researches"
    input_schema: Type[BaseModel] = Input
    output_schema: Type[BaseModel] = Output

    async def run(self, context: ExecutionContext, input: Input):
        with tempfile.NamedTemporaryFile(suffix=".json") as config:
            config.write(json.dumps({
                'LANGUAGE': input.language,
                'TOTAL_WORDS': input.words_count
            }))
            report = await self._make_report(input, config.name)
            return Output(report=report)

    @staticmethod
    async def _make_report(input: Input, config_path: str):
        researcher = GPTResearcher(
            query=input.query,
            report_type=input.report_type.value,
            config_path=config_path,
            verbose=False
        )
        await researcher.conduct_research()
        return await researcher.write_report()


if __name__ == '__main__':
    load_dotenv()
    leea.start(InternetResearcher())
