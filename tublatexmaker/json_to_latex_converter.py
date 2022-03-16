def add_pre_and_post_commands(pre: str, latex_body: str, post: str) -> str:
    """Adds the necessary LaTeX commands to text"""
    return pre + latex_body + post
