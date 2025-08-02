from parsing import parser, chunker

if __name__ == "__main__":
    # Parse PDFs
    policy_folder = "../data/policies"
    policies = parser.extract_all_from_folder(policy_folder, file_type="pdf")
    
    for filename, content in policies.items():
        print(f"\n--- {filename} ---\n")

        chunks = chunker.chunk_text_by_heading(content, source=filename)
        for c in chunks:
            print(f"📌 Chunk ID: {c['chunk_id']}")
            print(f"🔹 Title: {c['title']}")
            print(f"📝 Content:\n{c['content'][:300]}...\n")

    # Parse offer letter (if you want to chunk it too)
    offer_folder = "../data/sample_offer"
    offers = parser.extract_all_from_folder(offer_folder, file_type="docx")

    for filename, content in offers.items():
        print(f"\n--- {filename} ---\n")

        chunks = chunker.chunk_text_by_heading(content, source=filename)
        for c in chunks:
            print(f"📌 Chunk ID: {c['chunk_id']}")
            print(f"🔹 Title: {c['title']}")
            print(f"📝 Content:\n{c['content'][:300]}...\n")
