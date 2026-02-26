from configs import TEST_PROMPT
from manage_docs import select_and_copy_files, cleanup_docs
from upload_docs import upload_docs
from query_docs import generate_response
from check_docs import check_docs
from citate_docs import cite_documents

from gemini_client import client


def main():
    try:
        print("step 0: select documents")
        copied = select_and_copy_files()
        if copied:
            print(f"Added {len(copied)} file(s) to docs/: {', '.join(copied)}")
        else:
            print("No new files selected — using existing docs/ contents.")

        print("\nstep 1: upload docs")
        store = upload_docs(copied if copied else None)

        print("\nstep 2: check docs")
        for name in check_docs(store):
            print(name)

        print("\nstep 3: generate response")
        prompt = input("Enter your prompt (or press Enter to use default): ")
        prompt = prompt if prompt.strip() else TEST_PROMPT
        last_chunk = None
        for chunk in generate_response(prompt, store):
            print(chunk.text, end="", flush=True)
            last_chunk = chunk
        print()
        print("\nCitations:")
        citations = cite_documents(
            last_chunk.candidates[0] if last_chunk and last_chunk.candidates else None
        )
        print(citations)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("\nstep 4: cleanup docs")
        cleanup_docs()


if __name__ == "__main__":
    main()
