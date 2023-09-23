from langchain.chat_models import AzureChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class MultipleChoiceQuestion:
    def __init__(self):
        llm = AzureChatOpenAI(
            deployment_name="cda-t01",
            model_name="gpt-35-turbo",
            max_tokens=512
        )

    def generate(self, text, question_num):
        response_schemas = [
            ResponseSchema(
                name="question", description="A multiple choice question generated from input text snippet."),
            ResponseSchema(
                name="options", description="Possible choices for the multiple choice question."),
            ResponseSchema(
                name="answer", description="Correct answer for the question.")
        ]
        output_parser = StructuredOutputParser.from_response_schemas(
            response_schemas)
        format_instructions = output_parser.get_format_instructions()
        prompt = ChatPromptTemplate(messages=[HumanMessagePromptTemplate.from_template("""Given a text input, generate multiple choice questions
                    from it along with the correct answer.
                    \n{format_instructions}\n{user_prompt}""")],
                                    input_variables=["user_prompt"],
                                    partial_variables={"format_instructions": format_instructions})
        user_query = prompt.format_prompt(user_prompt=text)
        user_query_output = self.llm(user_query.to_messages())
        print(user_query_output.content)
        return 'json.loads(response.text)'
