  const svg = document.querySelector('svg.world-map');
  
  svg.addEventListener('click', (e) => {
    const pt = svg.createSVGPoint();
    pt.x = e.clientX; pt.y = e.clientY;
    const p = pt.matrixTransform(svg.getScreenCTM().inverse());
    console.log(`x=${p.x.toFixed(1)}, y=${p.y.toFixed(1)}`);
  });