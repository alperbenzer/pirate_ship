document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const errorEl = document.getElementById("error");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorEl.textContent = "";

    const username = form.username.value;
    const password = form.password.value;

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
	const res = await fetch("http://pirate-api:8001/login", {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      if (!res.ok) {
        errorEl.textContent = data.detail || "Giriş başarısız";
        return;
      }

      localStorage.setItem("token", data.access_token);
      window.location.href = "calls.html";
    } catch (err) {
      errorEl.textContent = "Sunucuya bağlanılamadı.";
    }
  });
});