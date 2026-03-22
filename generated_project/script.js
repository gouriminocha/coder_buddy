// script.js
// Calculator logic implementation
// This script is loaded with the `defer` attribute, so the DOM is already parsed.

;(function () {
  // Expose Calculator globally
  class Calculator {
    /**
     * @param {string} displayId - The id of the display input element (without #)
     * @param {string} buttonsContainerClass - The class of the buttons container (without .)
     */
    constructor(displayId, buttonsContainerClass) {
      // Elements
      this.displayEl = document.getElementById(displayId);
      this.buttonsContainer = document.querySelector(`.${buttonsContainerClass}`);

      // Internal state
      this.currentInput = '';
      this.previousValue = null; // number
      this.operator = null; // '+', '-', '*', '/' or null

      // Bind methods for event listeners (optional but clear)
      this.handleButtonClick = this.handleButtonClick.bind(this);
      this.handleKeyPress = this.handleKeyPress.bind(this);
    }

    /** Append a digit or decimal point to the current input */
    appendDigit(digit) {
      if (digit === '.') {
        // Prevent multiple decimals
        if (this.currentInput.includes('.')) return;
        // If input is empty, prepend a leading zero for nicer UX
        if (this.currentInput === '') this.currentInput = '0';
      }
      this.currentInput += digit;
      this.updateDisplay();
    }

    /** Set the operator (+, -, *, /) */
    setOperator(op) {
      // If there is already a pending operator and the user hasn't entered a new number,
      // just replace the operator.
      if (this.operator && this.currentInput === '') {
        this.operator = op;
        return;
      }

      const value = parseFloat(this.currentInput);
      this.previousValue = isNaN(value) ? 0 : value;
      this.operator = op;
      this.currentInput = '';
    }

    /** Perform calculation based on stored operator and values */
    calculate() {
      if (!this.operator) return; // nothing to calculate
      const current = parseFloat(this.currentInput);
      const right = isNaN(current) ? 0 : current;
      const left = this.previousValue !== null ? this.previousValue : 0;
      let result = 0;

      switch (this.operator) {
        case '+':
          result = left + right;
          break;
        case '-':
          result = left - right;
          break;
        case '*':
          result = left * right;
          break;
        case '/':
          // Guard against division by zero
          result = right === 0 ? 'Error' : left / right;
          break;
        default:
          result = right;
      }

      // Reset state after calculation
      this.currentInput = typeof result === 'number' ? String(result) : result;
      this.previousValue = null;
      this.operator = null;
      this.updateDisplay();
    }

    /** Clear all state and the display */
    clear() {
      this.currentInput = '';
      this.previousValue = null;
      this.operator = null;
      this.updateDisplay();
    }

    /** Delete the last character of the current input */
    delete() {
      if (this.currentInput.length > 0) {
        this.currentInput = this.currentInput.slice(0, -1);
        this.updateDisplay();
      }
    }

    /** Write the current input (or result) to the display element */
    updateDisplay() {
      if (!this.displayEl) return;
      // Show 0 when there is nothing entered for a cleaner UI
      this.displayEl.value = this.currentInput === '' ? '0' : this.currentInput;
    }

    /** Centralised click handler for all calculator buttons */
    handleButtonClick(event) {
      const btn = event.target.closest('button[data-action]');
      if (!btn) return; // click outside a button

      const action = btn.dataset.action;
      const content = btn.textContent.trim();

      switch (action) {
        case 'digit':
          this.appendDigit(content);
          break;
        case 'decimal':
          this.appendDigit('.');
          break;
        case 'add':
          this.setOperator('+');
          break;
        case 'subtract':
          this.setOperator('-');
          break;
        case 'multiply':
          this.setOperator('*');
          break;
        case 'divide':
          this.setOperator('/');
          break;
        case 'equals':
          this.calculate();
          break;
        case 'clear':
          this.clear();
          break;
        case 'backspace':
          this.delete();
          break;
        default:
          // No action needed
          break;
      }
    }

    /** Keyboard support – map keys to calculator actions */
    handleKeyPress(event) {
      const { key } = event;

      // Allow only relevant keys; ignore others to prevent unwanted side effects.
      if (/^[0-9]$/.test(key)) {
        this.appendDigit(key);
        return;
      }

      switch (key) {
        case '.':
          this.appendDigit('.');
          break;
        case '+':
          this.setOperator('+');
          break;
        case '-':
          this.setOperator('-');
          break;
        case '*':
        case 'x': // some keyboards use 'x' for multiplication
          this.setOperator('*');
          break;
        case '/':
          this.setOperator('/');
          break;
        case 'Enter':
        case '=':
          this.calculate();
          break;
        case 'Backspace':
          this.delete();
          break;
        case 'Escape':
          this.clear();
          break;
        default:
          // ignore other keys
          break;
      }
    }
  }

  // Expose the class globally so other scripts or tests can access it
  window.Calculator = Calculator;

  // Instantiate the calculator with the IDs defined in index.html
  const calc = new Calculator('display', 'buttons');

  // Attach event listeners
  if (calc.buttonsContainer) {
    calc.buttonsContainer.addEventListener('click', calc.handleButtonClick);
  }
  document.addEventListener('keydown', calc.handleKeyPress);

  // Initialise display
  calc.updateDisplay();
})();
