from configs import TEST_PROMPT
from manage_docs import select_and_copy_files, cleanup_docs
from upload_docs import upload_docs
from query_docs import generate_response
from check_docs import check_docs
from citate_docs import cite_documents


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
        check_docs(store)

        print("\nstep 3: generate response")
        prompt = input("Enter your prompt (or press Enter to use default): ")
        prompt = prompt if prompt.strip() else TEST_PROMPT
        response = generate_response(prompt, store)
        print(response.text)
        print("\nCitations:")
        citations = cite_documents(
            response.candidates[0] if response.candidates else None
        )
        print(citations)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("\nstep 4: cleanup docs")
        cleanup_docs()


if __name__ == "__main__":
    main()
