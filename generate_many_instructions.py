from generate_instruction import generate_instruction_following_data
import pandas as pd

path = 'Problem to Wolfram Query Example Dataset.xlsx'

def main():
    excel_file = pd.ExcelFile(path)
    sheet_names = excel_file.sheet_names 
    data_path = './data'
    for sheet_name in sheet_names:
        output_dir = data_path + f"/{sheet_name}"
        generate_instruction_following_data(
            output_dir=output_dir, 
            seed_tasks_path=output_dir+f"/seed_tasks.jsonl",
            prompt_path=output_dir+f"/prompt.txt",
            num_instructions_to_generate=100,
            model_name="text-davinci-003",
            num_prompt_instructions=3,
            request_batch_size=5,
            temperature=1.0,
            top_p=1.0,
            num_cpus=16,
            )

if __name__ == "__main__":
    main()
