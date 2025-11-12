import type { Component } from "@streamlit/component-v2-lib";

export type ComponentData = {
  text: string;
};

const MyComponent: Component<any, ComponentData> = (args) => {
  const { parentElement, data } = args;

  const rootElement = parentElement.querySelector(".component-root");
  if (!rootElement) {
    throw new Error("Unexpected: root element not found");
  }

  // Set dynamic content
  const heading = rootElement.querySelector("h1");
  if (heading) {
    heading.textContent = `Hello, ${data.text}!`;
  }
};

export default MyComponent;
