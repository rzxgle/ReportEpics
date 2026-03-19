DONE_STATUS = [
    "Pronto para Prod",
    "Prod",
    "Concluído"
]

IGNORED_STATUS = [
    "Inválido",
    "Cancelado"
]

def is_done(status):
    return status in DONE_STATUS

def is_ignored(status):
    return status in IGNORED_STATUS