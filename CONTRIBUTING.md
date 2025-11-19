# Contributing to st-transformers-js

First off, thank you for considering contributing to `st-transformers-js`. It's people like you that make the open source community such a great place.

## Where to start?

If you have an idea for a new feature or have found a bug, please open an issue on the [GitHub repository](https://github.com/yourusername/st-transformers-js/issues). This will allow us to discuss the proposed changes and ensure that they are in line with the project's goals.

## Development Setup

To get started with the development of `st-transformers-js`, you will need to have the following installed on your system:

-   Python 3.7+
-   Node.js 16+
-   npm 8+

Once you have these installed, you can follow these steps to set up the development environment:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/st-transformers-js.git
    cd st-transformers-js
    ```

2.  **Install the Python dependencies:**
    ```bash
    pip install -e .
    ```

3.  **Install the frontend dependencies:**
    ```bash
    cd frontend_v2
    npm install
    ```

4.  **Build the frontend assets:**
    ```bash
    ./build_script.sh
    ```

5.  **Run the tests:**
    ```bash
    python -m pytest
    ```

6.  **Run the demo application:**
    ```bash
    streamlit run demo_app_v2.py
    ```

## Submitting a Pull Request

When you are ready to submit a pull request, please make sure that you have done the following:

-   **Run the tests:** All of the tests must pass.
-   **Update the documentation:** If you have made any changes to the API, please update the `README.md` file accordingly.
-   **Add a changelog entry:** Add a new entry to the `CHANGELOG.md` file that describes the changes you have made.

Once you have done all of this, you can submit a pull request. We will review it as soon as possible and provide you with feedback.

Thank you for your contribution!
