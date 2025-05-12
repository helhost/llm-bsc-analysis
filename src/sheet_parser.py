from openpyxl.workbook.workbook import Workbook


def parse_response(data, response_number):
    """
    Parses a single response block from a given data sheet.

    Each response occupies a fixed number of rows in the data.
    Extracts the response ID, reasoning metadata, and a list of actions.

    Args:
        data (list of list): The worksheet data as rows of cell values.
        response_number (int): The index (0-based) of the response to parse.

    Returns:
        dict: A dictionary containing response metadata and associated actions.
    """
    start_row = 12 * response_number + 8  # Finds the starting row of the response section
    response_id = data[start_row+1][1]
    reasoning_quality = data[start_row+4][1]
    reasoning_notes = data[start_row+4][2]
    reasoning_hallucination = data[start_row+4][3]
    actions = []

    for i in range(start_row + 7, 3 + start_row + 7):
        if data[i][0] is None:
            continue
        actions.append({
            data[i][0]: {
                'usefulness': data[i][1],
                'actionability': data[i][2],
                'dupliacate': data[i][3],
                'hallucination': data[i][4],
                'relevant': data[i][5],
                'notes': data[i][6],
            }
        })

    return {
        'response_id': response_id,
        'reasoning_quality': reasoning_quality,
        'reasoning_notes': reasoning_notes,
        'reasoning_hallucination': reasoning_hallucination,
        'actions': actions
    }


def parse_sheet(wb: Workbook, sheet_name: str) -> dict:
    """
    Parses an entire worksheet from a workbook, extracting metadata and responses.

    Reads values from predefined rows to extract sheet-level metadata,
    then iterates over response blocks to collect response data.

    Args:
        wb (Workbook): An openpyxl Workbook object.
        sheet_name (str): The name of the sheet to parse.

    Returns:
        dict: A dictionary containing sheet-level metadata and all parsed responses.
    """
    sheet = wb[sheet_name]

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(row)

    tree_depth = data[0][1]
    num_branches = data[1][1]
    num_responses = data[2][1]
    success = data[3][1]
    context_level = data[4][1]
    category = data[5][1]
    notes = data[6][1]
    responses = []

    for i in range(num_responses if num_responses else 0):
        responses.append(parse_response(data, i))

    return {
        'name': sheet_name,
        'tree_depth': tree_depth,
        'num_branches': num_branches,
        'num_responses': num_responses,
        'success': success,
        'context-level': context_level,
        'category': category,
        'notes': notes,
        'responses': responses
    }
