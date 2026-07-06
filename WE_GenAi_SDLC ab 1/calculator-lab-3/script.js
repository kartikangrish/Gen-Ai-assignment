const display = document.querySelector("#display");
const buttons = document.querySelectorAll("button");

let expression = "";

function updateDisplay(value) {
  display.value = value || "0";
}

function appendValue(value) {
  const lastCharacter = expression.slice(-1);
  const operators = ["+", "-", "*", "/"];

  if (operators.includes(value) && operators.includes(lastCharacter)) {
    expression = expression.slice(0, -1) + value;
    updateDisplay(expression);
    return;
  }

  if (value === ".") {
    const currentNumber = expression.split(/[+\-*/]/).pop();
    if (currentNumber.includes(".")) {
      return;
    }
  }

  expression += value;
  updateDisplay(expression);
}

function clearCalculator() {
  expression = "";
  updateDisplay(expression);
}

function deleteLastCharacter() {
  expression = expression.slice(0, -1);
  updateDisplay(expression);
}

function tokenizeExpression(value) {
  const rawTokens = value.match(/\d+(\.\d+)?|\.\d+|[+\-*/]/g) || [];

  if (rawTokens.join("") !== value) {
    throw new Error("Invalid input");
  }

  const tokens = [];

  for (let index = 0; index < rawTokens.length; index += 1) {
    const token = rawTokens[index];
    const previousToken = tokens[tokens.length - 1];

    if (
      token === "-" &&
      (tokens.length === 0 || ["+", "-", "*", "/"].includes(previousToken))
    ) {
      const nextToken = rawTokens[index + 1];

      if (!nextToken || ["+", "-", "*", "/"].includes(nextToken)) {
        throw new Error("Invalid input");
      }

      tokens.push(String(-Number(nextToken)));
      index += 1;
      continue;
    }

    tokens.push(token);
  }

  return tokens;
}

function calculateTokens(tokens) {
  const highPrecedenceTokens = [...tokens];

  for (let index = 0; index < highPrecedenceTokens.length; index += 1) {
    const operator = highPrecedenceTokens[index];

    if (operator !== "*" && operator !== "/") {
      continue;
    }

    const left = Number(highPrecedenceTokens[index - 1]);
    const right = Number(highPrecedenceTokens[index + 1]);

    if (operator === "/" && right === 0) {
      throw new Error("Cannot divide by zero");
    }

    const result = operator === "*" ? left * right : left / right;
    highPrecedenceTokens.splice(index - 1, 3, String(result));
    index -= 1;
  }

  let result = Number(highPrecedenceTokens[0]);

  for (let index = 1; index < highPrecedenceTokens.length; index += 2) {
    const operator = highPrecedenceTokens[index];
    const right = Number(highPrecedenceTokens[index + 1]);

    if (operator === "+") {
      result += right;
    } else if (operator === "-") {
      result -= right;
    } else {
      throw new Error("Invalid input");
    }
  }

  return result;
}

function calculateResult() {
  if (!expression) {
    return;
  }

  try {
    const tokens = tokenizeExpression(expression);
    const result = calculateTokens(tokens);

    if (!Number.isFinite(result)) {
      updateDisplay("Invalid input");
      expression = "";
      return;
    }

    expression = Number.parseFloat(result.toFixed(10)).toString();
    updateDisplay(expression);
  } catch (error) {
    updateDisplay(error.message || "Error");
    expression = "";
  }
}

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const { value, action } = button.dataset;

    if (action === "clear") {
      clearCalculator();
      return;
    }

    if (action === "delete") {
      deleteLastCharacter();
      return;
    }

    if (action === "calculate") {
      calculateResult();
      return;
    }

    appendValue(value);
  });
});

updateDisplay(expression);
