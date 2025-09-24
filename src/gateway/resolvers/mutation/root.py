from ariadne import MutationType

mutation = MutationType()


@mutation.field("comment")
def resolve_comment_root(*_):
    return {}


@mutation.field("mod")
def resolve_mod_root(*_):
    return {}
