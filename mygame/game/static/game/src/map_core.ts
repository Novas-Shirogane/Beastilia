const svg = document.querySelector<SVGSVGElement>("svg.world-map");
const tip = document.querySelector<HTMLDivElement>("#map-tooltip");
const wrap = document.querySelector(".map-wrap");

if (!svg || !tip) throw new Error("map or tooltip not found");

svg.addEventListener("click", (e: MouseEvent) => {
  const pt = svg.createSVGPoint();
  pt.x = e.clientX;
  pt.y = e.clientY;

  const ctm = svg.getScreenCTM();
  if (!ctm) return; // SVGがDOMに未接続などでnullになることがある

  const p = pt.matrixTransform(ctm.inverse());
  console.log(`x=${p.x.toFixed(1)}, y=${p.y.toFixed(1)}`);
});

svg.addEventListener("mousemove", (e: MouseEvent) => {
  const ctm = svg.getScreenCTM();
  if (!ctm) return;

  const pt = svg.createSVGPoint();
  pt.x = e.clientX;
  pt.y = e.clientY;

  const p = pt.matrixTransform(ctm.inverse());
  console.log(`hover x=${p.x.toFixed(1)}, y=${p.y.toFixed(1)}`);
});

function showTip(target: Element, text: string) {
  const r = target.getBoundingClientRect();
  const w = wrap!.getBoundingClientRect();

  tip!.textContent = text;
  tip!.style.left = `${(r.right - w.left) + 8}px`;
  tip!.style.top  = `${(r.top - w.top) - 8}px`;
  tip!.hidden = false;
}

function hideTip() {
  tip!.hidden = true;
}

svg.querySelectorAll<SVGGElement>("g.node").forEach((node) => {
  const id = node.dataset.id ?? "(unknown)";

  node.addEventListener("mouseenter", (e) => {
    console.log("target:", e.target, "currentTarget:", e.currentTarget);
    const target = e.currentTarget as SVGGElement;
    showTip(target, `ID: ${id}`);
  });

  node.addEventListener("mouseleave", () => {
    hideTip();
  });
});