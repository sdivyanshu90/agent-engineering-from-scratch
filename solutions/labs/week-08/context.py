from forgeagent.context import ContextItem,estimate_tokens,select_context,compact
def select(items,query,budget,now): return select_context(items,query,token_budget=budget,now=now)
