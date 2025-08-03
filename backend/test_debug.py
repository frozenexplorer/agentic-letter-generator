from embedding.store import VectorStore

store = VectorStore()

queries = [
    "Earned Leave (EL): Planned leave",
    "Leave entitlements for Band L1",
    "Travel policy for Band L1",
    "Work from office policy for Sales team"
]

for q in queries:
    print(f"\n🔎 Query: {q}")
    result = store.similarity_search(q)
    if result["documents"] and result["documents"][0]:
        print("✅ Top Match:", result["documents"][0][0][:300])
    else:
        print("❌ No results")
