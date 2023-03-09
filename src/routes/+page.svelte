<script>
// @ts-nocheck
import { MetaTags } from 'svelte-meta-tags';
// import { _ } from 'svelte-i18n'
import * as THREE from "three"
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { onMount } from 'svelte';
import { CONSTELLATIONS } from "$lib/constellations.ts"
let data;
let ip;

onMount(async () => {
  const stars_json = await import("../stars.json")
  const stars = stars_json.default
  const scene = new THREE.Scene();
  // scene.background = new THREE.Color(0xf5f5f5);
  scene.background = new THREE.Color(0x050505);

  let size = {
    width: window.innerWidth,
    height: window.innerHeight,
    ratio: window.innerWidth / window.innerHeight,
  }

  const camera = new THREE.PerspectiveCamera(40, size.ratio, 5, 10000)

  const renderer = new THREE.WebGLRenderer( { antialias: true , preserveDrawingBuffer: true } );
  renderer.setSize( size.width, size.height );

  const controls = new OrbitControls(camera, renderer.domElement)

  camera.position.set(0, 0, 1)
  scene.rotation.x = -Math.PI / 2;
  controls.update();
  var sizes = [];
  var positions = [];
  var colors = [];
  var color = new THREE.Color();
  stars.forEach((star) =>{
    positions.push(star.x, star.y, star.z);
    color.setRGB(star.r, star.g, star.b);
    colors.push(Math.abs(color.r-128), Math.abs(color.g-128), Math.abs(color.b-128));
    sizes.push(star.size*10)
  })
  //星座
  var lines = []
  const keys = Object.keys(CONSTELLATIONS);
  keys.forEach((key)=> {
    let lines_arr = CONSTELLATIONS[key]
    CONSTELLATIONS[key].flat().forEach((id) => { //データベースに保存するときにこの処理(id->position)をやっとく
      stars.forEach((star) => {
        if (id == star.id) { lines.push(star.x, star.y, star.z) }
      })
    })
  })
  var material = new THREE.LineBasicMaterial({ color: "#f00" });
  var geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
  var l = new THREE.LineSegments(geometry, material);
  scene.add(l);
  //星全部
  var geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geometry.setAttribute('size', new THREE.Int32BufferAttribute(sizes, 1));
  geometry.computeBoundingSphere();
  var material = new THREE.PointsMaterial({
    size: 5,
    sizeAttenuation: true,
    vertexColors: true,
  });
  let p = new THREE.Points(geometry, material);
  scene.add(p);
  //北極星
  var geometry = new THREE.SphereGeometry(20, 32, 16);
  var material = new THREE.MeshBasicMaterial({ color: "#ff0" });
  var sphere = new THREE.Mesh( geometry, material );
  sphere.position.z = 1000
  scene.add( sphere );
  //星座の絵貼り付ける球
  var geometry = new THREE.SphereGeometry(990, 100, 100); //実装時に990->1000に変える、0.7->0に変える
  var material = new THREE.MeshLambertMaterial({ transparent: true, opacity: 0.7 });
  material.transparent = true
  var sphere = new THREE.Mesh( geometry, material );
  // new THREE.TextureLoader().load("$lib/assets/orion.png")
  scene.add(sphere);
  

  var geometry = new THREE.PlaneGeometry( 10000, 10000 );
  var material = new THREE.MeshBasicMaterial( {color: "#1F365A", side: THREE.DoubleSide} );
  var plane = new THREE.Mesh( geometry, material );
  // plane.rotation.x = Math.PI / 2;
  var rc = new THREE.Raycaster();

  // scene.add( plane );

  // var m = new THREE.Vector2();
  // function onMouseMove(event) {
  //   m.x = event.clientX
  //   m.y = event.clientY
  //   rc.setFromCamera(m, camera);
  //   intscs = rc.intersectObjects()
  // }
  document.body.appendChild( renderer.domElement );
  // renderer.domElement.addEventListener("pointermove", onMouseMove);
  renderer.render(scene, camera);
  function animate() {
    requestAnimationFrame( animate );
    controls.update();
    renderer.render( scene, camera );
  }
  animate()
})
//
</script>
<svelte:head>
  <title>星座</title>
  <MetaTags
  openGraph={{
    type: 'website',
    url: 'https://www.example.com/page',
    // title: $_('page.home.title'),
    // description: $_('page.home.description'),
    title: "星座",
    description: "💫星座です💫"
  }}
/>
</svelte:head>

<div id="container">
  
  
</div>
<style>
	:global(body) {
    /* overflow: hidden; */
		margin: 0;
	}
  #container {
    position: fixed;
    top: 10;
    right: 10;
    width: 80px;
    height: 120px;
    background: "#444";
  }
</style>
