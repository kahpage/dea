# =====================================================================
# Helper definitions
# =====================================================================

def is_to_add(obj: str | list | None) -> bool:
    """Basically returns the same as 'if obj:' but also excludes lists of 1 '' element."""
    if isinstance(obj, list):
        if len(obj) > 1:
            return True
        elif len(obj) == 0:
            return False
        else: # 1 elem
            if not isinstance(obj[0], str):
                return True # Keep if not list of str
            if obj[0] == '':
                return False
            return True
    if obj:
        return True
    return False