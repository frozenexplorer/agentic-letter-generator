from parsing import parser, chunker
from embedding.store import VectorStore

def main():
    docs = []

    # 1. Parse and chunk the PDF policies
    policy_folder = "../data/policies"
    policies = parser.extract_all_from_folder(policy_folder, "pdf")

    for filename, content in policies.items():
        chunks = chunker.chunk_text_by_heading(content, source=filename)
        docs.extend(chunks)

    # 2. Initialize vector store and store chunks
    store = VectorStore()
    store.add_documents(docs)
    print("✅ Documents embedded and stored.")

    # 3. Run a test query
    query = "What is the leave entitlement for L3 employees?"
    results = store.similarity_search(query)

    print("\n🔍 Top Matches for Query:")
    for doc in results["documents"][0]:
        print("--------------------------------------------------")
        print(doc[:400] + "...")
        print("--------------------------------------------------\n")

if __name__ == "__main__":
    main()
