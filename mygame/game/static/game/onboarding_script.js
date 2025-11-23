document.addEventListener("DOMContentLoaded", () => {
  const filename = `/static/game/onboarding_texts_${LANG}.json`;
  console.log("trying to load:", filename);

  fetch(filename)
    .then(async res => {
      const raw = await res.text();
      console.log("status:", res.status);
      console.log("raw response text:", raw);

      if (!res.ok) {
        throw new Error("HTTP " + res.status);
      }

      let data;
      try {
        data = JSON.parse(raw);
      } catch (e) {
        console.error("JSON parse error:", e);
        return;  // ここで終了
      }

      // ここから先は JSON が正しく読めた場合だけ実行
      document.getElementById("title").textContent = data.title;

      document.getElementById("description").innerHTML =
        data.description.replace(/\n/g, "<br>");

      document.getElementById("label_name").textContent = data.label_name;
      document.getElementById("button_create").textContent = data.button_create;
    })
    .catch(err => {
      console.error("読み込み失敗:", err);
    });
});