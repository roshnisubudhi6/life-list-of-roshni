"""Read or write the bird data embedded in index.html.

  python3 tools/birds.py dump  > birds.json   # extract
  python3 tools/birds.py load  < birds.json   # write back into index.html
"""
import json, re, sys
PATH = "index.html"
PAT = re.compile(r'(<script id="data" type="application/json">)(.*?)(</script>)', re.S)

def read():
    return json.loads(PAT.search(open(PATH, encoding="utf-8").read()).group(2))

def write(birds):
    html = open(PATH, encoding="utf-8").read()
    data = json.dumps(birds, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    html = PAT.sub(lambda m: m.group(1) + data + m.group(3), html, count=1)
    open(PATH, "w", encoding="utf-8").write(html)

if __name__ == "__main__":
    if sys.argv[1] == "dump":
        json.dump(read(), sys.stdout, ensure_ascii=False, indent=1)
    else:
        write(json.load(sys.stdin))
