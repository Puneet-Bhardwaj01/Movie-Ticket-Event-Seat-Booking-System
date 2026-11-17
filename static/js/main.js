document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("seat-form");
  if (!form) return;
  const checks = [...form.querySelectorAll('input[name="seats"]')];
  const seatText = document.getElementById("selected-seats");
  const totalText = document.getElementById("total-price");
  function update() {
    const chosen = checks.filter(c => c.checked);
    seatText.textContent = chosen.length ? chosen.map(c => c.value).join(", ") : "None";
    const total = chosen.reduce((sum, c) => sum + Number(c.dataset.price), 0);
    totalText.textContent = "₹" + total.toFixed(2);
    checks.forEach(c => { if (!c.checked) c.disabled = chosen.length >= 10; });
  }
  checks.forEach(c => c.addEventListener("change", update));
  form.addEventListener("submit", e => {
    if (!checks.some(c => c.checked)) { e.preventDefault(); alert("Please select at least one seat."); }
  });
  update();
});
