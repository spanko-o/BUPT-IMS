import re
from urllib.parse import parse_qs

def parse_url(path):
    # 匹配基本路径和可选的参数
    match = re.match(r"^(/[^/]+)(?:/([^/]+=[^/]+))?$", path)
    if not match:
        return None, None

    base_path, params = match.groups()
    query_params = {}

    if params:
        query_params = parse_qs(params)
        query_params = {k: v[0] for k, v in query_params.items()}

    return base_path, query_params