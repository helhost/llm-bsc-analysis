def get_depth(cur,response_id):
    cur.execute("""WITH RECURSIVE message_hierarchy AS (
        SELECT id, parent_id, 0 AS depth
        FROM message
        WHERE HEX(id) = ?
        UNION ALL

        SELECT m.id, m.parent_id, mh.depth + 1
        FROM message m
        JOIN message_hierarchy mh ON m.id = mh.parent_id
    )
    SELECT ((MAX(depth)+1)/2) AS message_depth FROM message_hierarchy;""", (response_id.replace('-','').upper(),))
    return cur.fetchone()[0]

def get_text(cur,response_id):
    cur.execute("""
                SELECT text FROM message WHERE HEX(id) = ?
                """, (response_id.replace('-','').upper(),))
    return cur.fetchone()

def get_root_text(cur,response_id):
    cur.execute("""
        WITH RECURSIVE message_hierarchy AS (
            SELECT id, parent_id, text
            FROM message
            WHERE HEX(id) = ?

            UNION ALL

            SELECT m.id, m.parent_id, m.text
            FROM message m
            JOIN message_hierarchy mh ON HEX(m.id) = HEX(mh.parent_id)
        )
        SELECT text
        FROM message_hierarchy
        WHERE parent_id IS NULL
        LIMIT 1;
    """, (response_id.replace('-', '').upper(),))
    result = cur.fetchone()
    return result[0] if result else None

def get_parent_text(cur,response_id):
    cur.execute("""
                SELECT text FROM message WHERE id = (SELECT parent_id FROM message WHERE HEX(id) = ?)
                """, (response_id.replace('-','').upper(),))
    return cur.fetchone()

def get_concatenated_text_from_root(cur,response_id):
    cur.execute("""
        WITH RECURSIVE message_hierarchy AS (
            SELECT id, parent_id, text
            FROM message
            WHERE HEX(id) = ?

            UNION ALL

            SELECT m.id, m.parent_id, m.text
            FROM message m
            JOIN message_hierarchy mh ON HEX(m.id) = HEX(mh.parent_id)
        )
        SELECT HEX(id), text
        FROM message_hierarchy;
    """, (response_id.replace('-', '').upper(),))
    
    all_rows = cur.fetchall()
    # Reverse to go root → current
    all_rows = all_rows[::-1]

    # Remove the last item (which corresponds to the original message ID)
    texts = [text for _, text in all_rows[:-1]]
    return "".join(texts)

