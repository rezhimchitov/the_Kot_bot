import json

IDs = [45, 55, 12, 15]
with open('sw_templates.json', 'w') as f:
    f.write(json.dumps(IDs))