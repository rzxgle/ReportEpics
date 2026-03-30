def get_label_options():
    return {
        "Afya Bridge": {
            "Q1": {
                "label": "EpicoPI1Legado",
                "quarter": "Q1",
                "year": 2026
            },
            "Q2": {
                "label": "EpicoPI2Legado",
                "quarter": "Q2",
                "year": 2026
            }
        },
        "Afya One": {
            "Q1": {
                "label": "PI1AfyaOne",
                "quarter": "Q1",
                "year": 2026
            },
            "Q2": {
                "label": "PI2AfyaOne",
                "quarter": "Q2",
                "year": 2026
            }
        }
    }
    
def get_products(options):
    return list(options.keys())

def get_cycles(options, product):
    return list(options[product].keys())

def get_selection(options, product, cycle):
    return options[product][cycle]