# import os
# import json
# import re
# import ijson
# from collections import defaultdict

# INPUT_FILE = "backend/alerts_history.json"
# OUTPUT_DIR = "settlements"

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# def sanitize_filename(name):
#     return re.sub(r'[<>:"/\\|?*]', '', name)

# buffers = defaultdict(list)
# BUFFER_SIZE = 1000

# def flush(settlement):
#     filepath = os.path.join(OUTPUT_DIR, f"{settlement}.json")

#     if os.path.exists(filepath):
#         with open(filepath, "r", encoding="utf-8") as f:
#             existing = json.load(f)
#     else:
#         existing = []

#     existing.extend(buffers[settlement])

#     with open(filepath, "w", encoding="utf-8") as f:
#         json.dump(existing, f, ensure_ascii=False)

#     buffers[settlement].clear()

# with open(INPUT_FILE, "rb") as f:
#     for alert in ijson.items(f, "item"):

#         settlement = sanitize_filename(alert["data"])

#         for field in ["NAME_HE", "NAME_EN", "NAME_AR", "NAME_RU"]:
#             alert.pop(field, None)

#         buffers[settlement].append(alert)

#         if len(buffers[settlement]) >= BUFFER_SIZE:
#             flush(settlement)

# for settlement in list(buffers.keys()):
#     if buffers[settlement]:
#         flush(settlement)

# print("done")




import json

with open('alerts_history.json', encoding='utf8') as file:
    data = json.load(file)

print(type(data))
print(len(data))
string = [str(a) for a in data]
s = set(string)
print(len(s))