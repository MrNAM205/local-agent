import json
import os
import math

INPUT = "knowledge.json"      # original big file (temporary)
OUT_DIR = "knowledge"
CHUNK_SIZE = 5000             # items per chunk

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        items = list(data.items())
    elif isinstance(data, list):
        items = list(enumerate(data))
    else:
        raise ValueError("Unsupported knowledge.json structure")

    total = len(items)
    chunks = math.ceil(total / CHUNK_SIZE)

    manifest = {"chunks": [], "total_items": total, "chunk_size": CHUNK_SIZE}

    for i in range(chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        chunk_items = dict(items[start:end])

        filename = f"chunk_{i:04d}.json"
        path = os.path.join(OUT_DIR, filename)

        with open(path, "w", encoding="utf-8") as out:
            json.dump(chunk_items, out, indent=2, ensure_ascii=False)

        manifest["chunks"].append(filename)
        print(f"Wrote {filename} with {len(chunk_items)} items")

    manifest_path = os.path.join(OUT_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as m:
        json.dump(manifest, m, indent=2)

    print("Chunking complete.")
    print(f"Total items: {total}, chunks: {chunks}")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
