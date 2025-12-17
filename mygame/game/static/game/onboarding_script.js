const RACE_DESC = {
  wolf: "狼：バランス型。探索と戦闘が安定。",
  fox: "狐：魔術寄り。器用でトリッキー。",
  cat: "猫：回避寄り。素早い。",
};

document.addEventListener("DOMContentLoaded", () => {
  // --- modal elements ---
  const overlay = document.getElementById("race_modal_overlay");
  const titleEl = document.getElementById("race_modal_title");
  const descEl = document.getElementById("race_modal_desc");
  const okBtn = document.getElementById("race_modal_ok");
  const cancelBtn = document.getElementById("race_modal_cancel");
  const raceInput = document.getElementById("race_input");

  const form = document.getElementById("create_form");
  const confirmOverlay = document.getElementById("confirm_modal_overlay");
  const confirmText = document.getElementById("confirm_modal_text");
  const confirmOk = document.getElementById("confirm_ok");
  const confirmCancel = document.getElementById("confirm_cancel");

  if (
    !overlay || !titleEl || !descEl || !okBtn || !cancelBtn || !raceInput ||
    !form || !confirmOverlay || !confirmText || !confirmOk || !confirmCancel
  ) {
    console.error("elements missing", {
      overlay, titleEl, descEl, okBtn, cancelBtn, raceInput,
      form, confirmOverlay, confirmText, confirmOk, confirmCancel
    });
    return;
  }

  let selectedRace = null;
  let selectedEl = null;

  function openModal(raceKey) {
    selectedRace = raceKey;
    titleEl.textContent = raceKey;
    descEl.textContent = RACE_DESC[raceKey] ?? "説明未設定";
    overlay.hidden = false;
  }

  function closeModal() {
    overlay.hidden = true;
    selectedRace = null;
  }

  // icon click
  document.querySelectorAll(".race-icon").forEach((img) => {
    img.style.cursor = "pointer";
    img.addEventListener("click", () => {
      const raceKey = img.dataset.race;
      selectedEl = img.closest(".race-option");
      openModal(raceKey);
    });
  });

  // modal close actions
  cancelBtn.addEventListener("click", closeModal);
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closeModal();
  });

  // OK
  okBtn.addEventListener("click", () => {
    if (!selectedRace) return;
    raceInput.value = selectedRace;

    // 既存の選択枠を外す
    document.querySelectorAll(".race-option.is-selected")
      .forEach(el => el.classList.remove("is-selected"));

    // 選択枠を現在選択したものに付ける
    if (selectedEl) selectedEl.classList.add("is-selected");

    closeModal();
    // raceInput.closest("form").submit(); // すぐ送信したいなら
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault(); // ← ここ重要
    if (!raceInput.value) {
      e.preventDefault();
      alert("種族を選択してください");
      return;
    }
    confirmText.textContent =
    `種族「${raceInput.value}」名前：${form.name.value}でキャラクターを生成しますか？`;

    confirmOverlay.hidden = false;
  });

  confirmCancel.addEventListener("click", () => {
    confirmOverlay.hidden = true;
  });

  confirmOverlay.addEventListener("click", (e) => {
    if (e.target === confirmOverlay) confirmOverlay.hidden = true;
  });

  confirmOk.addEventListener("click", () => {
    confirmOverlay.hidden = true;
    form.submit(); // ← ここで本当に送信
  });

  // --- onboarding text fetch ---
  const filename = `/static/game/onboarding_texts_${LANG}.json`;
  fetch(filename)
    .then(async (res) => {
      const raw = await res.text();
      if (!res.ok) throw new Error("HTTP " + res.status);

      const data = JSON.parse(raw);

      document.getElementById("title").textContent = data.title;
      document.getElementById("description").innerHTML = data.description.replace(/\n/g, "<br>");
      document.getElementById("direction_1").textContent = data.direction_1;
      document.getElementById("direction_1_desc").innerHTML = data.direction_1_desc.replace(/\n/g, "<br>");
      document.getElementById("label_name").textContent = data.label_name;
      document.getElementById("button_create").textContent = data.button_create;
    })
    .catch((err) => console.error("読み込み失敗:", err));
});