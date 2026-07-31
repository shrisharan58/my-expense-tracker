# AI Notes

## 1. Whether the text was produced by AI or by me

I used ChatGPT as an assistant while working on this project. It helped me create the initial structure of the FastAPI project, including the API routes, the Pydantic models, the JSON storage logic, and the basic test cases.

I didn't submit the generated code without reviewing it first. I examined the code, understood how each section worked, made necessary changes, and ensured the project met the requirements of the assignment. I also updated the README, checked the project structure, and resolved any issues that came up during testing.

---

## 2. The things that I verified, tested, or modified and the reasons for doing so

I checked everything myself after finishing the project instead of assuming that the generated code was correct.

Things I verified include:

- I ran the complete test suite using pytest and confirmed that all 13 tests passed.
- I started the FastAPI server using Uvicorn.
- I manually tested the API using the Swagger UI (the '/docs' page).
- I verified that I could create, list, filter by category, and delete expenses successfully.
- I checked that the totals endpoint returned the overall total and the totals grouped by category.
- I tested invalid inputs like negative amounts and empty fields to ensure that the validation worked correctly.
- I confirmed that category filtering operates as expected.
- I ensured that the route `/expenses/totals` is defined before `/expenses/{id}` so that FastAPI can handle the requests properly.
- I reviewed the project files and the README to verify that the setup instructions were accurate.

---

## 3.The AI suggestions that I did not use and the reasons why

I chose not to follow certain AI suggestions.

One suggestion was to use SQLite instead of a JSON file for data storage. I rejected this idea because the assignment specified that a database was not needed and local JSON storage was acceptable.

I also considered adding optional features like Docker support and advanced search capabilities, but I decided to focus on properly finishing and testing all required features before submission.

---

## Additional Notes

Through this project, I became more familiar with FastAPI, developing REST APIs, request validation, and using pytest for automated testing.

If I had more time, I would improve the project by adding user authentication, enhancing error logging, implementing pagination for large numbers of expenses, and using a database backend instead of JSON storage.

The current implementation is suitable for this task, but since it stores data in a JSON file, it is designed for a single-user environment and is not meant for concurrent access.
