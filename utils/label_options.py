def get_label_options():
    return {
        "Afya Bridge": {
            "Q1": {
                "labels": ["EpicoPI1Legado"],
                "quarter": "Q1",
                "year": 2026,
                "display_name": "Quarter 1",
                "description": "Ciclo Q1 Afya Bridge"
            },
            "Q2": {
                "labels": ["EpicoPI2Legado", "LegadoTransbordoP126"],
                "quarter": "Q2",
                "year": 2026,
                "display_name": "Quarter 2",
                "description": "Ciclo Q2 Afya Bridge"
            }
        },
        "Afya One": {
            "Q1": {
                "labels": ["PI1AfyaOne"],
                "quarter": "Q1",
                "year": 2026,
                "display_name": "Quarter 1",
                "description": "Ciclo Q1 Afya One"
            },
            "Q2": {
                "labels": ["PI2AfyaOne"],
                "quarter": "Q2",
                "year": 2026,
                "display_name": "Quarter 2",
                "description": "Ciclo Q2 Afya One"
            }
        }
    }
    
def get_products(options):
    return list(options.keys())

def get_cycles(options, product):
    return list(options[product].keys())

def get_selection(options, product, cycle):
    return options[product][cycle]