import pandas as pd
from enum import Enum
import os

class Categories(Enum):
    GRAPH_POLY_IDENTIFY_ZEROS = 'Graph Poly + Identify Zeros'
    LIN_QUAD_EQN = 'Systems of Lin+Quad Equations'
    TANGENT_TO_CIRCLES = 'Tangents to Circles'
    LOCAL_MIN_MAX = 'Local Minima and Maxima'
    SYS_LIN_EQN = 'Systems of Linear Equations'
    LIN_INEQ_SYS = 'Linear Inequality Systems'
    INTERSECTIONS_OF_LINES = 'Intersections of Lines'
    X_Y_INTERCEPTS = 'X Intercepts, Y Intercepts'

path = 'Problem to Wolfram Query Example Dataset.xlsx'




context_dict = {
    Categories.GRAPH_POLY_IDENTIFY_ZEROS : "graphing polynomials and identifying zeros",
    Categories.LIN_QUAD_EQN : "graphing systems of linear and quadratic equations",
    Categories.TANGENT_TO_CIRCLES : "finding tangents to circles",
    Categories.LOCAL_MIN_MAX : "finding local minima and local maxima",
    Categories.SYS_LIN_EQN : "solving systems of linear equations",
    Categories.LIN_INEQ_SYS : "solving systems of linear inequalities",
    Categories.INTERSECTIONS_OF_LINES : "finding intersections between lines",
    Categories.X_Y_INTERCEPTS : "finding X Intercepts and Y Intercepts",
}


sheet_of_interest = 'Local Minima and Maxima'

def construct_prompt(context):
    """ Creates a prompt """
    introduction = f"""You are asked to come up with a set of 20 diverse task instructions on {context} along with their corresponding wolfram alpha query. These task instructions will be given to a GPT model and we will evaluate the GPT model for completing the instructions.
    """

    requirement = """
Here are the requirements:
1. Try not to repeat the verb for each instruction to maximize diversity.
2. The language used for the instruction also should be diverse. For example, you should combine questions with imperative instrucitons.
3. The type of instructions should be diverse.
4. A GPT language model should be able to complete the instruction. For example, do not ask the assistant to create any visual or audio output. For another example, do not ask the assistant to wake you up at 5pm or set a reminder because it cannot perform any action.
5. The instructions should be in English.
7. You should generate an appropriate input to the instruction. The input field should contain a specific example provided for the instruction. It should involve realistic data and should not contain simple placeholders. The input should provide substantial content to make the instruction challenging but should ideally not exceed 100 words.
8. The output should be an appropriate response to the instruction and the input. Make sure the output is less than 100 words.
9. Do not generate classification tasks. For example, do not generate tasks such as "Does f(x)=2x have any 0 intercepts?"
10. The queries should be interpretable by wolfram alpha's natural language API. For example, do not put a statement like "the intersection is (1, 0)" for the query
11. Limit each wolfram alpha query to at most 20 words
12. Instructions and their wolfram alpha queries should not involve imaginary numbers
13. Express them in the form {"problem": <problem>, "query": <query> }

List of 10 tasks:
"""

    prompt = introduction + requirement
    return prompt

def format_problem_query_pair(problem, query, id):
    """ formats a problem-query pair as {"problem": "<problem>", "query": "<query>"} """
    instance = f' "instances": [{{"input": "", "output": "{query}" }}] '

    return f'{{"id": "seed_task_{id}", "name": "", "instruction": "{problem}", {instance}, "is_classification": false }}'

    # return r'{"problem": ' + f'"{problem}", ' + r'"query": ' + f'"{query}"' + "}"
    # return r'{"problem": ' + f'"{problem}"' + "}"

def read_through_dataframe(df):
    """ Creates a list of problem query pairs by iterating through rows of pd dataframe """
    problem_col, query_col = df.columns
    problem_query_pairs = []
    for i, row in df.iterrows():
        problem_query_pair = format_problem_query_pair(row[problem_col], row[query_col], i)
        problem_query_pairs.append(problem_query_pair)
    return problem_query_pairs
    

def output_prompt(problem_query_pairs):
    """ Prints out the prompt and the list of examples to use """
    # print (prompt)
    # for pair in problem_query_pairs:
    #     print(pair)
    # print()
    return '\n'.join(problem_query_pairs)


def setup_directory(data_path, name):
    """sets up directory with name"""
    if name in os.listdir(data_path) or name == "":
        return f'./data/{name}'

    new_directory_path = f'./data/{name}'
    os.mkdir(new_directory_path)
    return new_directory_path

def write_to_directory(directory_path, data, prompt):
    json_file = open(f"{directory_path}/seed_tasks.jsonl", 'w')
    json_file.write(data)
    prompt_file = open(f"{directory_path}/prompt.txt", 'w')
    prompt_file.write(prompt)



def main():
    excel_file = pd.ExcelFile(path)

    

    # can change to be a list of selected categories (e.g ["X Intercepts, Y Intercepts"])
    sheet_names = excel_file.sheet_names 
    data_path = './data'
    for sheet_name in sheet_names:
        print (sheet_name)
        df = excel_file.parse(sheet_name)
        problem_query_pairs = read_through_dataframe(df)
        data = output_prompt(problem_query_pairs)

        prompt = construct_prompt(context_dict[Categories(sheet_name)])

        dir_path = setup_directory(data_path, sheet_name)
        write_to_directory(dir_path, data, prompt)


if __name__ == "__main__":
    main()