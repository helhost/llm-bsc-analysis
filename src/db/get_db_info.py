import sqlite3

from .queries import (
    get_depth,
    get_text,
    get_parent_text,
    get_root_text,
    get_concatenated_text_from_root,
)

def add_db_to_df(cur, df):
    """
    Add database information to the DataFrame.
    """
    # Get the message depth
    df['message_depth'] = df['response_id'].apply(lambda x: get_depth(cur, x))
    
    # Get the message text
    df['message_text'] = df['response_id'].apply(lambda x: get_text(cur, x))
    
    # Get the root text
    df['root_text'] = df['response_id'].apply(lambda x: get_root_text(cur, x))
    
    # Get the parent message text
    df['parent_text'] = df['response_id'].apply(lambda x: get_parent_text(cur, x))
    
    # Get the concatenated text from root
    df['concatenated_text_from_root'] = df['response_id'].apply(lambda x: get_concatenated_text_from_root(cur, x))

    # Get the total length of the concatenated text
    df['concatenated_text_from_root_length'] = df['concatenated_text_from_root'].apply(lambda x: len(x.split()))
    
    return df

