// ========== 1. Role-Based Registration Toggle ==========
document.addEventListener("DOMContentLoaded", () => {
  const roleSelect = document.querySelector("select[name='role']");
  const citizenFields = document.getElementById("citizen-fields");
  const lawyerFields = document.getElementById("lawyer-fields");

  if (roleSelect) {
    const toggleFields = () => {
      const role = roleSelect.value;
      citizenFields.style.display = role === "citizen" ? "block" : "none";
      lawyerFields.style.display = role === "lawyer" ? "block" : "none";
    };

    toggleFields(); // Initial state
    roleSelect.addEventListener("change", toggleFields);
  }
});

// ========== 2. Smooth Scroll for Navigation ==========
document.querySelectorAll("a[href^='#']").forEach(anchor => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  });
});

// ========== 3. Live Search Filtering (Citizen Dashboard) ==========
const searchInput = document.querySelector(".search input");
const lawyerCards = document.querySelectorAll(".lawyer-card");

if (searchInput && lawyerCards.length > 0) {
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    lawyerCards.forEach(card => {
      const name = card.querySelector("h3").textContent.toLowerCase();
      const spec = card.querySelector("p").textContent.toLowerCase();
      card.style.display = name.includes(query) || spec.includes(query) ? "block" : "none";
    });
  });
}

// ========== 4. Button Ripple Effect ==========
document.querySelectorAll("button").forEach(button => {
  button.addEventListener("click", function (e) {
    const ripple = document.createElement("span");
    ripple.className = "ripple";
    ripple.style.left = `${e.offsetX}px`;
    ripple.style.top = `${e.offsetY}px`;
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});

// ========== 5. Dashboard Card Hover Animation ==========
document.querySelectorAll(".case-card, .lawyer-card").forEach(card => {
  card.addEventListener("mouseenter", () => {
    card.style.transform = "scale(1.02)";
    card.style.transition = "transform 0.3s ease";
  });
  card.addEventListener("mouseleave", () => {
    card.style.transform = "scale(1)";
  });
});