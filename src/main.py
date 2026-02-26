from configs import TEST_PROMPT
from upload_docs import upload_docs
from query_docs import generate_response
from check_docs import check_docs
from citate_docs import cite_documents


def main():
    print("step 1: upload docs")
    upload_docs()
    print("step 2: check docs")
    check_docs()
    print("step 3: generate response")
    prompt = input("Enter your prompt (or press Enter to use default): ")
    prompt = prompt if prompt.strip() else TEST_PROMPT
    response = generate_response(prompt)
    print(response.text)
    print("\nCitations:")
    citations = cite_documents(response.candidates[0] if response.candidates else None)
    print(citations)


if __name__ == "__main__":
    main()
