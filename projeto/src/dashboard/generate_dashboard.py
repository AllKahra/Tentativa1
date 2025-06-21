import json
import webbrowser
from pathlib import Path

TEMPLATE_PATH = Path("dashboard/templates/dashboard.html")
OUTPUT_PATH = Path("dashboard/output.html")

def load_results(json_file):
    with open(json_file, "r") as f:
        lines = f.readlines()
        return [json.loads(line) for line in lines]

def get_recommendation(item):
    # Pode melhorar com base em template ou CWE
    if "cwe" in item.get("info", {}):
        return f"Consultar detalhes em https://cwe.mitre.org/data/definitions/{item['info']['cwe'][0]}.html"
    return "Verificar a documentação oficial e aplicar patches de segurança."

def parse_results(data):
    parsed = []
    for item in data:
        parsed.append({
            "host": item.get("host", "N/A"),
            "severity": item.get("info", {}).get("severity", "info").lower(),
            "name": item.get("info", {}).get("name", "Sem título"),
            "description": item.get("info", {}).get("description", "Sem descrição"),
            "recommendation": get_recommendation(item)
        })
    return parsed

def generate_dashboard(vulns):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("{{DATA_JSON}}", json.dumps(vulns, indent=2))
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard gerado em: {OUTPUT_PATH.resolve()}")
    webbrowser.open(OUTPUT_PATH.resolve().as_uri())

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python generate_dashboard.py caminho_para_arquivo.json")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"Arquivo não encontrado: {json_path}")
        sys.exit(1)

    raw = load_results(json_path)
    structured = parse_results(raw)
    generate_dashboard(structured)
