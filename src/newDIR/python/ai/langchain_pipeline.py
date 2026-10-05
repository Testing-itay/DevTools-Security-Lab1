"""LangChain pipeline with OpenAI and Anthropic integrations."""

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def build_code_review_chain(provider: str = "openai"):
    """Build an LLM chain for code review using the specified provider."""
    if provider == "anthropic":
        llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.2)
    else:
        llm = ChatOpenAI(model="gpt-4", temperature=0.2)

    prompt = PromptTemplate(
        input_variables=["code", "language"],
        template="Review the following {language} code for security and best practices:\n\n{code}\n\nProvide concise feedback.",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def run_code_review(code: str, language: str = "python", provider: str = "openai") -> str:
    """Run code through the LangChain review pipeline."""
    chain = build_code_review_chain(provider=provider)
    result = chain.invoke({"code": code, "language": language})
    return result.get("text", "")
