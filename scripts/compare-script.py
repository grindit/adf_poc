import argparse
import json

def load_template_parameters(template_path):
    """Load parameters from an ARM template JSON file."""
    with open(template_path, 'r') as file:
        template = json.load(file)
    return template.get('parameters', {})

def compare_parameters(params1, params2):
    """Compare two sets of ARM template parameters."""
    params1_names = set(params1.keys())
    params2_names = set(params2.keys())

    if params1_names == params2_names:
        return True, None
    else:
        missing_in_1 = params2_names - params1_names
        missing_in_2 = params1_names - params2_names
        return False, (missing_in_1, missing_in_2)

def main(source_path, target_path):
    source_params = load_template_parameters(source_path)
    target_params = load_template_parameters(target_path)

    match, mismatched_params = compare_parameters(source_params, target_params)
    
    if match:
        print("Parameters match across both templates.")
    else:
        missing_in_1, missing_in_2 = mismatched_params
        print("### Parameters Check: Parameters do not match across environments ###")
        if missing_in_1:
            print(f"Parameters in template 2 not found in template 1: {', '.join(missing_in_1)}")
        if missing_in_2:
            print(f"Parameters in template 1 not found in template 2: {', '.join(missing_in_2)}")
        print("#################################################################################################")    
        print("# Please, check ARM parameters files located in environments directory!                         #")
        print("# Make sure that each file have the same parameters and values are correct for each environment #")
        print("#################################################################################################") 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare ARM parameters between two templates.")
    parser.add_argument('-source', type=str, required=True, help='The path to the source ARM parameters file')
    parser.add_argument('-target', type=str, required=True, help='The path to the target ARM parameters file')

    args = parser.parse_args()
    main(args.source, args.target)