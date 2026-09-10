(function () {
  const ASPHALT = 0x2d2b2b, PAINT = 0xf3f2f2, RED = 0xec3013, TIRE = 0x141312, GLASS = 0x4a4746;

  function build(THREE, el) {
    const box = (w, h, d, color, x, y, z, parent, rough) => {
      const m = new THREE.Mesh(
        new THREE.BoxGeometry(w, h, d),
        new THREE.MeshStandardMaterial({ color: color, roughness: rough === undefined ? 0.6 : rough, metalness: 0.08 })
      );
      m.position.set(x, y, z);
      parent.add(m);
      return m;
    };
    const wheel = (r, x, y, z, parent) => {
      const m = new THREE.Mesh(
        new THREE.CylinderGeometry(r, r, 0.16, 14),
        new THREE.MeshStandardMaterial({ color: TIRE, roughness: 0.9 })
      );
      m.rotation.x = Math.PI / 2;
      m.position.set(x, y, z);
      parent.add(m);
      return m;
    };

    function semi(trailerColor, cabColor, flatbed) {
      const g = new THREE.Group(), wheels = [];
      if (flatbed) {
        box(2.5, 0.09, 0.86, cabColor, -0.75, 0.44, 0, g);
        box(1.5, 0.3, 0.7, 0xd7d3d3, -0.95, 0.62, 0, g);
        box(0.9, 0.22, 0.62, 0xd7d3d3, -1.05, 0.87, 0, g);
      } else {
        box(2.5, 0.78, 0.9, trailerColor, -0.75, 0.82, 0, g);
        box(2.5, 0.07, 0.84, 0x201e1d, -0.75, 0.41, 0, g);
      }
      box(0.1, 0.24, 0.5, 0x201e1d, -1.55, 0.3, 0, g);
      box(0.62, 0.72, 0.84, cabColor, 0.78, 0.72, 0, g);
      box(0.44, 0.38, 0.8, cabColor, 1.28, 0.55, 0, g);
      box(0.06, 0.28, 0.66, GLASS, 1.5, 0.78, 0, g);
      box(0.34, 0.26, 0.72, GLASS, 1.06, 0.92, 0, g);
      box(0.07, 0.34, 0.07, 0x201e1d, 0.46, 1.25, 0.3, g);
      box(0.07, 0.34, 0.07, 0x201e1d, 0.46, 1.25, -0.3, g);
      box(0.08, 0.3, 0.86, 0x201e1d, 1.53, 0.36, 0, g);
      box(2.3, 0.08, 0.4, 0x201e1d, 0.5, 0.4, 0, g);
      [[-0.1, 0.42], [-0.62, 0.42], [1.3, 0.4]].forEach(function (p) {
        wheels.push(wheel(p[1] * 0.62, p[0], p[1] * 0.62, 0.46, g), wheel(p[1] * 0.62, p[0], p[1] * 0.62, -0.46, g));
      });
      wheels.push(wheel(0.26, -1.0, 0.26, 0.46, g), wheel(0.26, -1.0, 0.26, -0.46, g));
      g.userData.wheels = wheels;
      return g;
    }

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.domElement.style.cssText = 'display:block;width:100%;height:100%';
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(30, 4, 0.1, 200);
    camera.position.set(1.5, 2.6, 8.4);
    camera.lookAt(0, 0.5, 0);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x2d2b2b, 1.15));
    const sun = new THREE.DirectionalLight(0xffffff, 1.5);
    sun.position.set(6, 9, 5);
    scene.add(sun);

    box(60, 0.2, 7.2, ASPHALT, 0, -0.1, 0, scene, 0.95);
    box(60, 0.22, 0.16, PAINT, 0, 0.02, 3.1, scene, 0.8);
    box(60, 0.22, 0.16, PAINT, 0, 0.02, -3.1, scene, 0.8);
    const dashes = [];
    for (let i = -14; i <= 14; i++) dashes.push(box(1.1, 0.21, 0.12, PAINT, i * 2.1, 0.02, 0, scene, 0.8));

    const a = semi(RED, 0xf3f2f2, false);
    a.scale.setScalar(0.62);
    a.position.set(-9, 0, -1.55);
    scene.add(a);

    const b = semi(0xd7d3d3, 0xd7d3d3, true);
    b.scale.setScalar(0.56);
    b.rotation.y = Math.PI;
    b.position.set(9, 0, 1.55);
    scene.add(b);

    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const resize = function () {
      const w = el.clientWidth || 900, h = el.clientHeight || 120;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.fov = w < 700 ? 40 : 30;
      camera.updateProjectionMatrix();
    };
    resize();
    if (window.ResizeObserver) new ResizeObserver(resize).observe(el);

    let last = performance.now(), raf = 0;
    const tick = function (now) {
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      if (!still) {
        a.position.x += dt * 4.2;
        if (a.position.x > 15) a.position.x = -15;
        b.position.x -= dt * 3.1;
        if (b.position.x < -15) b.position.x = 15;
        a.userData.wheels.forEach(function (w) { w.rotation.y -= dt * 14; });
        b.userData.wheels.forEach(function (w) { w.rotation.y += dt * 11; });
        dashes.forEach(function (d) { d.position.x -= dt * 2.2; if (d.position.x < -30) d.position.x += 60; });
      }
      renderer.render(scene, camera);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) cancelAnimationFrame(raf);
      else { last = performance.now(); raf = requestAnimationFrame(tick); }
    });
  }

  class Road3D extends HTMLElement {
    connectedCallback() {
      if (this.dataset.mounted) return;
      this.dataset.mounted = '1';
      const el = this;
      let tries = 0;
      const start = function () {
        if (window.THREE && window.THREE.WebGLRenderer) { build(window.THREE, el); return; }
        if (tries++ < 200) setTimeout(start, 60);
      };
      start();
    }
  }

  if (!customElements.get('road-3d')) customElements.define('road-3d', Road3D);
})();
