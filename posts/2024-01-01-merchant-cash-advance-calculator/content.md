# Merchant Cash Advance to Annual Interest Calculator

In eCommerce, Merchant Cash Advances are common financial offerings. Both Shopify and Amazon have integrated financial offerings based on your sales data. These offers are often quite appealing: borrow $10,000 and payback $11,000 in 6 months.

At face value these offers seem like a fair market rate like 10% in that case. However, it's a bit deceiving.

If you had instead borrowed with a term loan, then as you pay down the principal of the debt the interest payments come down as well.

So, borrowing $10,000 at 10% APY, with monthly payments you'd pay back about $10,530. Not $11,000. That's a big difference!

Here's the calculator to find the equivalent APY rate for a merchant cash advance. Use this to more fairly compare the cost of credit and whether or not you'd be better off with credit cards.

## MCA to Annual Interest Calculator (Monthly Payments)

Enter your merchant cash advance details below:

```html
<div>
  <label for="advance">Advance Amount:</label><br>
  <input type="number" id="advance" placeholder="e.g. 100000"><br>

  <label for="repayment">Total Repayment Amount:</label><br>
  <input type="number" id="repayment" placeholder="e.g. 120000"><br>

  <label for="term">Term (in months):</label><br>
  <input type="number" id="term" placeholder="e.g. 6"><br>

  <button onclick="calculateInterest()">Calculate Interest</button>

  <div class="result" id="result"></div>
</div>
```

```javascript
function calculateInterest() {
  var advance = parseFloat(document.getElementById('advance').value);
  var totalRepayment = parseFloat(document.getElementById('repayment').value);
  var term = parseFloat(document.getElementById('term').value);

  // Validate input values
  if(isNaN(advance) || isNaN(totalRepayment) || isNaN(term) || advance <= 0 || term <= 0) {
    document.getElementById('result').innerText = "Please enter valid positive numbers for all fields.";
    return;
  }

  // Calculate the equal monthly payment from the provided total repayment amount.
  var monthlyPayment = totalRepayment / term;

  // If repayment equals the advance, then no interest is applied.
  if(Math.abs(monthlyPayment * term - advance) < 1e-6) {
    document.getElementById('result').innerText = "No interest (repayment equals principal).";
    return;
  }

  // Define the function for which we want to solve:
  // g(r) = (Monthly Payment * (1 - (1+r)^(-term)) / r) - Advance = 0
  function g(r) {
    return monthlyPayment * (1 - Math.pow(1 + r, -term)) / r - advance;
  }

  // Use binary search to find the monthly rate r such that g(r) is approximately 0.
  var low = 0;
  var high = 1;
  while (g(high) > 0) {
    high *= 2;
    if (high > 1000) break;
  }

  var mid = 0;
  for (var i = 0; i < 100; i++) {
    mid = (low + high) / 2;
    var gm = g(mid);
    if (Math.abs(gm) < 1e-10) {
      break;
    }
    if (gm > 0) {
      low = mid;
    } else {
      high = mid;
    }
  }

  var monthlyRate = mid;
  var annualRate = Math.pow(1 + monthlyRate, 12) - 1;

  var message = "Calculated Monthly Interest Rate: " + (monthlyRate * 100).toFixed(2) + "%\n";
  message += "Equivalent Annual Interest Rate: " + (annualRate * 100).toFixed(2) + "%\n";
  message += "Assumed Equal Monthly Payment: $" + monthlyPayment.toFixed(2) + "\n";
  message += "Total of Monthly Payments: $" + (monthlyPayment * term).toFixed(2);

  document.getElementById('result').innerText = message;
}
```
