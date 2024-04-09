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

def main(template1_path, template2_path):
    params1 = load_template_parameters(template1_path)
    params2 = load_template_parameters(template2_path)

    match, mismatched_params = compare_parameters(params1, params2)
    
    if match:
        print("Parameters match across both templates.")
    else:
        missing_in_1, missing_in_2 = mismatched_params
        print("Parameters do not match across environments")
        if missing_in_1:
            print(f"Parameters in template 2 not found in template 1: {', '.join(missing_in_1)}")
        if missing_in_2:
            print(f"Parameters in template 1 not found in template 2: {', '.join(missing_in_2)}")
        print("#################################################################################################")    
        print("# Please, check ARM parameters files located in environments directory!                         #")
        print("# Make sure that each file have the same parameters and values are correct for each environment #")
        print("#################################################################################################") 

# Paths to your ARM template files
template1_path = 'ArmTemplateOutput/ARMTemplateParametersForFactory.json'
template2_path = 'environments/arm_parameters_prod.json'

# Run the comparison
main(template1_path, template2_path)