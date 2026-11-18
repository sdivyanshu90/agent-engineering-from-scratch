def agreement(rows):
    if not rows:return 0.0
    return sum(row['human']==row['score'] for row in rows)/len(rows)
