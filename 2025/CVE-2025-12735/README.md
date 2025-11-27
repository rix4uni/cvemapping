# safe-expr-eval Documentation

Complete documentation for the `safe-expr-eval` library - A secure expression evaluator and drop-in replacement for expr-eval.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [API Reference](#api-reference)
5. [Supported Operations](#supported-operations)
6. [Advanced Usage](#advanced-usage)
7. [Security](#security)
8. [Examples](#examples)
9. [Migration Guide](#migration-guide)
10. [Troubleshooting](#troubleshooting)

---

## Introduction

`safe-expr-eval` is a secure expression parser and evaluator designed as a drop-in replacement for the vulnerable `expr-eval` library. It provides safe expression evaluation without using JavaScript's `eval()` or `Function()` constructor, protecting against code injection attacks (CVE-2025-12735).

### Key Features

- 🔒 **100% Secure** - No eval() or Function() constructors
- 🔄 **Drop-in Replacement** - Compatible API with expr-eval
- 📘 **TypeScript Support** - Full type definitions included
- ⚡ **Zero Dependencies** - Lightweight and self-contained
- ✅ **Well-tested** - Comprehensive test coverage
- 🎯 **Modern** - ES2020+ support

---

## Installation

```bash
npm install safe-expr-eval
```

### Requirements

- Node.js >= 14.0.0
- npm or yarn

---

## Quick Start

### Basic Evaluation

```javascript
const { Parser } = require('safe-expr-eval');

const parser = new Parser();
const result = parser.evaluate('2 + 3 * 4');
console.log(result); // 14
```

### With Variables

```javascript
const parser = new Parser();
const expr = parser.parse('price * quantity');

console.log(expr.evaluate({ price: 10, quantity: 5 })); // 50
console.log(expr.evaluate({ price: 20, quantity: 3 })); // 60
```

### Using TypeScript

```typescript
import { Parser, Values } from 'safe-expr-eval';

const parser = new Parser();
const variables: Values = { x: 10, y: 20 };
const result = parser.evaluate('x + y', variables);
console.log(result); // 30
```

---

## API Reference

### Parser Class

#### `new Parser()`

Creates a new parser instance.

```javascript
const parser = new Parser();
```

#### `parser.parse(expression: string)`

Parses an expression and returns an object with an `evaluate()` method.

**Parameters:**
- `expression` (string): The expression to parse

**Returns:** Object with `evaluate(variables?: Values)` method

**Example:**
```javascript
const expr = parser.parse('x * 2 + 1');
console.log(expr.evaluate({ x: 5 })); // 11
```

#### `parser.evaluate(expression: string, variables?: Values)`

Evaluates an expression directly (shorthand for parse + evaluate).

**Parameters:**
- `expression` (string): The expression to evaluate
- `variables` (object, optional): Variable values

**Returns:** Evaluation result

**Example:**
```javascript
parser.evaluate('10 + 5'); // 15
parser.evaluate('x + y', { x: 10, y: 5 }); // 15
```

#### `parser.functions`

Object containing custom functions available in expressions.

**Example:**
```javascript
parser.functions.square = (x) => x * x;
parser.evaluate('square(5)'); // 25
```

#### `parser.consts`

Object containing constants available in expressions.

**Example:**
```javascript
parser.consts.PI = 3.14159;
parser.evaluate('PI * 2'); // 6.28318
```

### Standalone Functions

#### `evaluate(expression: string, variables?: Values)`

Evaluates an expression directly without creating a parser instance.

**Example:**
```javascript
const { evaluate } = require('safe-expr-eval');
console.log(evaluate('2 + 3')); // 5
```

#### `compile(expression: string)`

Compiles an expression into a reusable function.

**Returns:** Function that accepts variables and returns the result

**Example:**
```javascript
const { compile } = require('safe-expr-eval');
const fn = compile('a * b + c');

console.log(fn({ a: 2, b: 3, c: 1 })); // 7
console.log(fn({ a: 5, b: 2, c: 10 })); // 20
```

---

## Supported Operations

### Arithmetic Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `10 - 4` | `6` |
| `*` | Multiplication | `3 * 4` | `12` |
| `/` | Division | `15 / 3` | `5` |
| `%` | Modulo | `10 % 3` | `1` |

**Operator Precedence:**
1. Parentheses `()`
2. Multiplication, Division, Modulo `*`, `/`, `%`
3. Addition, Subtraction `+`, `-`

**Examples:**
```javascript
parser.evaluate('2 + 3 * 4');     // 14 (not 20)
parser.evaluate('(2 + 3) * 4');   // 20
parser.evaluate('10 / 2 + 3');    // 8
```

### Comparison Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `==` | Equal | `5 == 5` | `true` |
| `!=` | Not equal | `5 != 3` | `true` |
| `>` | Greater than | `10 > 5` | `true` |
| `<` | Less than | `3 < 7` | `true` |
| `>=` | Greater or equal | `5 >= 5` | `true` |
| `<=` | Less or equal | `3 <= 7` | `true` |

**Examples:**
```javascript
parser.evaluate('age >= 18', { age: 21 });           // true
parser.evaluate('price < 100', { price: 85 });       // true
parser.evaluate('status == "active"', { status: "active" }); // true
```

### Logical Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `and` | Logical AND | `true and false` | `false` |
| `or` | Logical OR | `true or false` | `true` |
| `not` | Logical NOT | `not true` | `false` |

**Precedence:** `not` > `and` > `or`

**Examples:**
```javascript
parser.evaluate('(5 > 3) and (10 < 20)');        // true
parser.evaluate('(age >= 18) and (hasLicense)', { age: 21, hasLicense: true }); // true
parser.evaluate('not (x > 10)', { x: 5 });       // true
```

### Data Types

#### Numbers
```javascript
parser.evaluate('42');        // Integer
parser.evaluate('3.14');      // Float
parser.evaluate('-5');        // Negative
parser.evaluate('10 + 5.5');  // Mixed: 15.5
```

#### Strings
```javascript
parser.evaluate('"hello"');                    // "hello"
parser.evaluate("'world'");                    // 'world'
parser.evaluate('name == "John"', { name: "John" }); // true
```

#### Booleans
```javascript
parser.evaluate('true');         // true
parser.evaluate('false');        // false
parser.evaluate('x and y', { x: true, y: false }); // false
```

#### Variables
```javascript
parser.evaluate('x', { x: 42 });                    // 42
parser.evaluate('user.age', { 'user.age': 25 });    // 25
parser.evaluate('price * quantity', { price: 10, quantity: 5 }); // 50
```

---

## Advanced Usage

### Custom Functions

Register custom functions to use in expressions:

```javascript
const parser = new Parser();

// Math functions
parser.functions.abs = Math.abs;
parser.functions.round = Math.round;
parser.functions.max = Math.max;
parser.functions.min = Math.min;
parser.functions.sqrt = Math.sqrt;

parser.evaluate('abs(-10)');              // 10
parser.evaluate('round(3.7)');            // 4
parser.evaluate('max(5, 10, 3)');         // 10
parser.evaluate('sqrt(16)');              // 4
```

### Custom Business Logic Functions

```javascript
parser.functions.calculateTax = (amount, rate) => amount * rate;
parser.functions.applyDiscount = (price, discount) => price * (1 - discount);

parser.evaluate('calculateTax(100, 0.15)'); // 15
parser.evaluate('applyDiscount(price, 0.2)', { price: 100 }); // 80
```

### Constants

Define reusable constants:

```javascript
const parser = new Parser();

parser.consts.PI = Math.PI;
parser.consts.E = Math.E;
parser.consts.TAX_RATE = 0.15;
parser.consts.MAX_QUANTITY = 100;

parser.evaluate('PI * 2');                           // 6.283185...
parser.evaluate('price * (1 + TAX_RATE)', { price: 100 }); // 115
```

### Complex Expressions

```javascript
const parser = new Parser();
parser.functions.max = Math.max;
parser.functions.min = Math.min;
parser.consts.SHIPPING_BASE = 5;

// Shipping cost calculation
const shippingExpr = 'SHIPPING_BASE + max(0, weight - 1) * 2';
console.log(parser.evaluate(shippingExpr, { weight: 3 })); // 9

// Discount calculation with tiers
const discountExpr = 'total * min(0.3, years * 0.05)';
console.log(parser.evaluate(discountExpr, { total: 100, years: 3 })); // 15
```

### Compiled Expressions for Performance

When evaluating the same expression multiple times with different values:

```javascript
const { compile } = require('safe-expr-eval');

// Compile once
const calculatePrice = compile('price * quantity * (1 - discount) * (1 + tax)');

// Use many times (faster than parsing each time)
console.log(calculatePrice({ price: 100, quantity: 2, discount: 0.1, tax: 0.15 }));
console.log(calculatePrice({ price: 50, quantity: 5, discount: 0.2, tax: 0.15 }));
console.log(calculatePrice({ price: 75, quantity: 3, discount: 0, tax: 0.15 }));
```

---

## Security

### Why safe-expr-eval is Secure

1. **No eval()**: Never uses JavaScript's dangerous `eval()` function
2. **No Function constructor**: Doesn't dynamically create executable code
3. **Tokenization & AST**: Expressions are parsed into tokens and evaluated safely
4. **Type safety**: Built with TypeScript for additional guarantees
5. **No prototype pollution**: Proper object handling prevents prototype attacks

### Vulnerability in expr-eval (CVE-2025-12735)

The original `expr-eval` library is vulnerable to arbitrary code execution:

```javascript
// ❌ VULNERABLE (expr-eval)
const Parser = require('expr-eval').Parser;
const parser = new Parser();

// Attacker can inject malicious code
parser.evaluate('process.exit()'); // Executes arbitrary code!
parser.evaluate('require("fs").readFileSync("/etc/passwd")'); // Reads files!
```

### How safe-expr-eval Protects You

```javascript
// ✅ SAFE (safe-expr-eval)
const { Parser } = require('safe-expr-eval');
const parser = new Parser();

// These will throw errors instead of executing code
parser.evaluate('process.exit()');     // Error: Undefined variable
parser.evaluate('require("fs")');      // Error: Undefined function
parser.evaluate('eval("1+1")');        // Error: Undefined function
```

### Best Practices

1. **Validate Input Length**
```javascript
function safeEvaluate(expr, vars) {
  if (expr.length > 1000) {
    throw new Error('Expression too long');
  }
  return parser.evaluate(expr, vars);
}
```

2. **Whitelist Functions**
```javascript
const parser = new Parser();
// Only expose safe functions
parser.functions.abs = Math.abs;
parser.functions.min = Math.min;
parser.functions.max = Math.max;
// Don't expose dangerous functions
```

3. **Sanitize Variables**
```javascript
function evaluateWithSafeVars(expr, userVars) {
  const safeVars = {
    x: Number(userVars.x) || 0,
    y: Number(userVars.y) || 0
  };
  return parser.evaluate(expr, safeVars);
}
```

4. **Error Handling**
```javascript
try {
  const result = parser.evaluate(userExpression, variables);
  console.log('Result:', result);
} catch (error) {
  console.error('Invalid expression:', error.message);
  // Don't expose error details to users
  return { error: 'Invalid expression' };
}
```

---

## Examples

### E-commerce Price Calculation

```javascript
const { Parser } = require('safe-expr-eval');
const parser = new Parser();

parser.consts.TAX_RATE = 0.15;
parser.consts.SHIPPING_FLAT = 5;
parser.functions.min = Math.min;
parser.functions.max = Math.max;

const priceExpr = parser.parse(`
  (price * quantity * (1 - discount)) * (1 + TAX_RATE) + 
  SHIPPING_FLAT + max(0, weight - 1) * 2
`);

const order1 = {
  price: 50,
  quantity: 2,
  discount: 0.1,
  weight: 3
};

console.log(priceExpr.evaluate(order1)); // Total with tax and shipping
```

### Business Rules Validation

```javascript
const parser = new Parser();

const eligibilityRule = parser.parse(
  'age >= 18 and income > 30000 and credit_score >= 650'
);

const applicant = {
  age: 25,
  income: 45000,
  credit_score: 720
};

if (eligibilityRule.evaluate(applicant)) {
  console.log('Applicant is eligible');
} else {
  console.log('Applicant is not eligible');
}
```

### Dynamic Form Validation

```javascript
const parser = new Parser();

const rules = [
  { field: 'age', rule: 'age >= 18', message: 'Must be 18 or older' },
  { field: 'salary', rule: 'salary > 0', message: 'Salary must be positive' },
  { field: 'email', rule: 'email != ""', message: 'Email is required' }
];

function validateForm(formData) {
  const errors = [];
  
  for (const { field, rule, message } of rules) {
    try {
      if (!parser.evaluate(rule, formData)) {
        errors.push({ field, message });
      }
    } catch (error) {
      errors.push({ field, message: 'Invalid field' });
    }
  }
  
  return errors;
}

const formData = {
  age: 16,
  salary: 50000,
  email: 'user@example.com'
};

console.log(validateForm(formData)); // [{ field: 'age', message: 'Must be 18 or older' }]
```

### Loyalty Discount Calculator

```javascript
const parser = new Parser();
parser.functions.min = Math.min;
parser.functions.max = Math.max;

const discountExpr = parser.parse(`
  total * min(0.3, max(0.05, loyalty_years * 0.03))
`);

console.log(discountExpr.evaluate({ total: 100, loyalty_years: 2 }));  // $6
console.log(discountExpr.evaluate({ total: 100, loyalty_years: 10 })); // $30
```

### Conditional Feature Flags

```javascript
const parser = new Parser();

const featureFlags = {
  'premium_feature': 'is_premium and account_age > 30',
  'beta_feature': 'is_beta_tester or (is_premium and opt_in)',
  'discount_eligible': 'purchases > 5 and loyalty_years >= 1'
};

function hasFeature(featureName, userContext) {
  const rule = featureFlags[featureName];
  if (!rule) return false;
  
  try {
    return parser.evaluate(rule, userContext);
  } catch {
    return false;
  }
}

const user = {
  is_premium: true,
  account_age: 45,
  is_beta_tester: false,
  opt_in: true,
  purchases: 8,
  loyalty_years: 2
};

console.log(hasFeature('premium_feature', user)); // true
console.log(hasFeature('beta_feature', user));    // true
```

---

## Migration Guide

### From expr-eval to safe-expr-eval

Migration is simple - just change the import:

**Before (expr-eval):**
```javascript
const { Parser } = require('expr-eval');
```

**After (safe-expr-eval):**
```javascript
const { Parser } = require('safe-expr-eval');
```

The API is 100% compatible, so your existing code will work without changes.

### API Compatibility

| Feature | expr-eval | safe-expr-eval |
|---------|-----------|----------------|
| `new Parser()` | ✅ | ✅ |
| `parser.parse()` | ✅ | ✅ |
| `parser.evaluate()` | ✅ | ✅ |
| `parser.functions` | ✅ | ✅ |
| `parser.consts` | ✅ | ✅ |
| Custom functions | ✅ | ✅ |
| Variables | ✅ | ✅ |
| Security | ❌ | ✅ |

---

## Troubleshooting

### Common Issues

#### "Undefined variable" Error

**Problem:**
```javascript
parser.evaluate('x + y'); // Error: Undefined variable: x
```

**Solution:**
```javascript
parser.evaluate('x + y', { x: 10, y: 5 }); // 15
```

#### "Unexpected token" Error

**Problem:**
```javascript
parser.evaluate('2 + * 3'); // Error: Unexpected token
```

**Solution:** Check your expression syntax is correct:
```javascript
parser.evaluate('2 + 3'); // 5
```

#### "Undefined function" Error

**Problem:**
```javascript
parser.evaluate('sqrt(16)'); // Error: Undefined function: sqrt
```

**Solution:** Register the function first:
```javascript
parser.functions.sqrt = Math.sqrt;
parser.evaluate('sqrt(16)'); // 4
```

#### Floating Point Precision

**Problem:**
```javascript
parser.evaluate('0.1 + 0.2'); // 0.30000000000000004
```

**Solution:** Round results when needed:
```javascript
parser.functions.round = (x, decimals = 2) => {
  return Math.round(x * Math.pow(10, decimals)) / Math.pow(10, decimals);
};
parser.evaluate('round(0.1 + 0.2, 2)'); // 0.3
```

---

## Performance Tips

1. **Use `compile()` for repeated evaluations**
```javascript
// Slow: Parsing every time
for (let i = 0; i < 1000; i++) {
  parser.evaluate('x * 2 + 1', { x: i });
}

// Fast: Parse once, use many times
const fn = compile('x * 2 + 1');
for (let i = 0; i < 1000; i++) {
  fn({ x: i });
}
```

2. **Reuse Parser instances**
```javascript
// Create once, reuse
const parser = new Parser();
parser.functions.abs = Math.abs;

// Use many times
parser.evaluate('abs(x)', { x: -5 });
parser.evaluate('abs(y)', { y: -10 });
```

3. **Cache parsed expressions**
```javascript
const cache = new Map();

function evaluateWithCache(expr, vars) {
  if (!cache.has(expr)) {
    cache.set(expr, parser.parse(expr));
  }
  return cache.get(expr).evaluate(vars);
}
```

---

## Contributing

Contributions are welcome! Please visit our GitHub repository:
https://github.com/alecasg555/safe-expr-eval

## License

MIT License - See LICENSE file for details

## Author

**Alejandro Castrillon** - [GitHub](https://github.com/alecasg555)

---

**Developed by Alejandro Castrillon**
