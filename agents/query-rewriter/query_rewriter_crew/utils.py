import re


def extract_sql_tag(text: str) -> str:
    sql_match = re.search(r'<sql>(.*?)</sql>', text, re.DOTALL)
    sql_content = sql_match.group(1) if sql_match else None
    return sql_content

def extract_answer_tag(text: str) -> str:
    answer_match = re.search(r'<answer>(.*?)</answer>', text, re.DOTALL)
    answer_content = answer_match.group(1) if answer_match else None
    return answer_content