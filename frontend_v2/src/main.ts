import { Component } from "@streamlit/component-v2-lib";

const MyComponent: Component = (args) => {
    const { data, setStateValue, parentElement } = args;

    const rootElement = document.createElement("div");
    parentElement.appendChild(rootElement);

    const heading = document.createElement("h1");
    heading.textContent = `Hello, ${data.text}!`;
    rootElement.appendChild(heading);

    const button = document.createElement("button");
    button.textContent = "Send message to Python";
    button.onclick = () => {
        setStateValue({ message: "Hello from the frontend!" });
    };
    rootElement.appendChild(button);
};

export default MyComponent;
