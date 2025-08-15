let scene, camera, renderer;

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.z = 0;

    renderer = new THREE.WebGLRenderer({canvas: document.getElementById("sky")});
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function raDecToXYZ(alt, az) {
    const altRad = alt * Math.PI/180;
    const azRad = az * Math.PI/180;
    const x = Math.cos(altRad) * Math.sin(azRad);
    const y = Math.sin(altRad);
    const z = Math.cos(altRad) * Math.cos(azRad);
    return {x, y, z};
}

function renderStars(stars) {
    stars.forEach(s => {
        const geo = new THREE.SphereGeometry(0.02, 8, 8);
        const mat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const star = new THREE.Mesh(geo, mat);
        const pos = raDecToXYZ(s.alt, s.az);
        star.position.set(pos.x, pos.y, pos.z);
        scene.add(star);
    });
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

navigator.geolocation.getCurrentPosition(pos => {
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;
    const time = new Date().toISOString();

    fetch(`/stars?lat=${lat}&lon=${lon}&time=${time}`)
        .then(res => res.json())
        .then(data => {
            init();
            renderStars(data);
        });
});
