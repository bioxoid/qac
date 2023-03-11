<script>
// @ts-nocheck
// import { _ } from 'svelte-i18n'
import CanvasEditor from "$lib/components/Editor.svelte"
import * as THREE from "three"
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { onMount } from 'svelte';
import { CONSTELLATIONS } from "$lib/constellations.ts"

import {Ori, Ari, Gem, Cap} from "$lib/assets/textures.ts"

let data;
let ip;
let drawing = ""

onMount(async () => {
  const stars_json = await import("../stars.json")
  const stars = stars_json.default
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x151515);

  let size = {
    width: window.innerWidth,
    height: window.innerHeight,
    ratio: window.innerWidth / window.innerHeight,
  }

  const camera = new THREE.PerspectiveCamera(50, size.ratio, 5, 10000)

  const renderer = new THREE.WebGLRenderer( { antialias: true , preserveDrawingBuffer: true } );
  renderer.setSize( size.width, size.height );

  const controls = new OrbitControls(camera, renderer.domElement)
  // controls.maxPolarAngle = Math.PI/2;
  controls.minDistance = 1;
  // controls.maxDistance = 100;
  camera.position.set(0, 0, 1)
  scene.rotation.x = -(Math.PI/2); //+(Math.PI*23.4)/(2*90) 地軸
  controls.update();
  //星座 処理
  // var sizes = [];
  // var positions = [];
  // var colors = [];
  // stars.forEach((star) =>{
  //   positions.push(star.x, star.y, star.z)
  //   colors.push(star.r/255, star.g/255, star.b/255)
  //   sizes.push(star.size)
  // })
  // 星全部
  for (let i=10; 0<=i; i--) {
    var sizes = [];
    var positions = [];
    var colors = [];
    stars.forEach((star) =>{
      if (star.size == i)
        positions.push(star.x, star.y, star.z);
        colors.push(star.r/255, star.g/255, star.b/255);
        // sizes.push(star.size);
    })
    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(colors), 3));
    // geometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));
    geometry.computeBoundingSphere();
    var material = new THREE.PointsMaterial({
      size: i,
      sizeAttenuation: true,
      vertexColors: true,
      depthWrite:true
    });
    let points = new THREE.Points(geometry, material);
    scene.add(points);
  }
  // stars.forEach((star) => {
  //   const geometry = new THREE.CircleGeometry( star.size, 32 );
  //   const material = new THREE.MeshBasicMaterial( { color: (star.r/255, star.g/255, star.b/255) } );
  //   const circle = new THREE.Mesh( geometry, material );
  //   circle.position.x = star.x
  //   scene.add( circle );
  // })
  //星座線 描画
  var lines = []
  const keys = Object.keys(CONSTELLATIONS);
  function getStarFromId(id) {
    var star_of_id;
    var isFound = false;
    stars.forEach((star) => {
      if (!isFound && id == star.id) { isFound = true; star_of_id = star }
    })
    return star_of_id
  }
  keys.forEach((key)=> {
    let lines_arr = CONSTELLATIONS[key]
    CONSTELLATIONS[key].flat().forEach((id) => { //データベースに保存するときにこの処理(id->position)をやっとく
      let star = getStarFromId(id)
      lines.push(star.x, star.y, star.z)
    })
  })
  var geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
  var material = new THREE.LineBasicMaterial({ color: "#FED75D" });
  const starLines = new THREE.LineSegments(geometry, material);
  scene.add(starLines);
  //北極星
  var geometry = new THREE.SphereGeometry(20, 32, 16);
  var material = new THREE.MeshBasicMaterial({ color: "#fff" });
  var sphere = new THREE.Mesh( geometry, material );
  sphere.position.z = 1000
  // scene.add( sphere );
  //透明な球 星座絵のテクスチャ貼るかも
  var geometry = new THREE.SphereGeometry(990, 100, 100); //実装時に990->1000に変える、0.7->0に変える
  var material = new THREE.MeshLambertMaterial({ transparent: true, opacity: 0.8 });
  // const loader = new THREE.TextureLoader();
  // const textures_path = ["Ori", "Cap", "Gem", "Ari"]
  // const textures = []
  var sphere = new THREE.Mesh( geometry, material );
  scene.add(sphere);
  //
  // var geometry = new THREE.PlaneGeometry(100, 100*.75);
  // var material = new THREE.MeshLambertMaterial({map: loader.load("https://i.imgur.com/afCUu06.png")});
  // var orion = new THREE.Mesh(geometry, material);
  // const position_of_star_of_ori = CONSTELLATIONS["Ori"][0][0];
  // const orion_position = getStarFromId(position_of_star_of_ori)
  // scene.add(orion);
  //地面
  // var geometry = new THREE.PlaneGeometry( 10000, 10000 );
  // var material = new THREE.MeshBasicMaterial( {color: "#1F365A", side: THREE.DoubleSide} );
  // var plane = new THREE.Mesh( geometry, material );
  // plane.rotation.x = Math.PI / 2;
  // var rc = new THREE.Raycaster();

  // scene.add( plane );

  // var m = new THREE.Vector2();
  // function onMouseMove(event) {
  //   m.x = event.clientX
  //   m.y = event.clientY
  //   rc.setFromCamera(m, camera);
  //   intscs = rc.intersectObjects()
  // }
  const dat = await import('dat.gui')
  const gui = new dat.GUI()
  // const starFolder = gui.addFolder('Star')
  // starFolder.add(points.rotation, 'x', 0, Math.PI * 2)
  // starFolder.add(points.rotation, 'y', 0, Math.PI * 2)
  // starFolder.add(points.rotation, 'z', 0, Math.PI * 2)
  // starFolder.open()
  // const cameraFolder = gui.addFolder('Camera lookat')
  // cameraFolder.add(camera.position, 'z', 0, 10)
  // cameraFolder.open()
  const lineFolder = gui.addFolder('Star Lines color(なぜか255で割られてる)')
  lineFolder.add(starLines.material.color, 'r', 0, 1)
  lineFolder.add(starLines.material.color, 'g', 0, 1)
  lineFolder.add(starLines.material.color, 'b', 0, 1)
  // lineFolder.open()
  const sceneFolder = gui.addFolder('Scene rotation')
  sceneFolder.add(scene.rotation, 'x', -Math.PI, Math.PI)
  sceneFolder.add(scene.rotation, 'y', -Math.PI, Math.PI)
  sceneFolder.add(scene.rotation, 'z', -Math.PI, Math.PI)
  document.body.appendChild( renderer.domElement );
  // renderer.domElement.addEventListener("pointermove", onMouseMove);
  renderer.render(scene, camera);
  function animate() {
    requestAnimationFrame( animate );
    controls.update();
    renderer.render( scene, camera );
  }
  animate()
});
</script>
<svelte:head>
  <title>量子星座生成アプリ</title>
  <meta property="og:url" content="https://qac.vercel.app/">
  <meta property="og:title" content="量子星座生成アプリ">
  <meta property="og:description" content="💫量子アニーリングを使ってあなたのお絵描きから星座を生成するアプリです💫">
  <meta property="og:image" content="">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta property="twitter:domain" content="qac.vercel.app">
  <meta property="twitter:url" content="https://qac.vercel.app/">
  <meta name="twitter:title" content="量子星座生成アプリ">
  <meta name="twitter:description" content="💫量子アニーリングを使ってあなたのお絵描きから星座を生成するアプリです💫">
  <meta name="twitter:image" content="">
</svelte:head>

<div id="container">
  <CanvasEditor bind:canvas={drawing}  />
  <!-- <DevelopMode /> -->
</div>
<style>
	:global(body) {
    /* overflow: hidden; */
		margin: 0;
	}
  /* #container {
    position: fixed;
    top: 10;
    right: 10;
    width: 500px;
    height: 500px;
  } */
</style>
