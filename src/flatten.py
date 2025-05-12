import pandas as pd



def flatten_parsed_sheets(parsed_sheets: list) -> pd.DataFrame:
    """
    Flattens the parsed sheets data structure into a list of dictionaries,
    with each dictionary representing one row in the final DataFrame.
    
    Args:
        parsed_sheets (list): List of dictionaries representing parsed Excel sheets
        
    Returns:
        pandas.DataFrame: DataFrame with one row per action
    """
    
    flattened_rows = []
    
    for sheet in parsed_sheets:
        for response in sheet['responses']:
            for action_obj in response['actions']:
                # Get the action name (which is the key of the action_obj)
                action_name = list(action_obj.keys())[0]
                action_details = action_obj[action_name]
                
                # Create a flattened row
                flattened_row = {
                    'scenario': sheet['name'],
                    'finding_number': sheet['name'][1],  # Assuming the format is 'f1c2', 'f2c1', etc.
                    'context-level': sheet['context-level'],
                    'tree_depth': sheet['tree_depth'],
                    'num_branches': sheet['num_branches'],
                    'num_responses': sheet['num_responses'],
                    'success': sheet['success'],
                    'category': sheet['category'],
                    'sheet_notes': sheet['notes'],
                    'response_id': response['response_id'],
                    'reasoning_quality': response['reasoning_quality'],
                    'reasoning_notes': response['reasoning_notes'],
                    'reasoning_hallucination': response['reasoning_hallucination'],
                    'action_name': action_name,
                    'usefulness': action_details['usefulness'],
                    'actionability': action_details['actionability'],
                    'duplicate': action_details['dupliacate'],
                    'action_hallucination': action_details['hallucination'],
                    'relevant': action_details['relevant'],
                    'action_notes': action_details['notes']
                }
                
                flattened_rows.append(flattened_row)
    
    # Create DataFrame from the flattened rows
    df = pd.DataFrame(flattened_rows)
    
    return df