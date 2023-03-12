<script>
// @ts-nocheck
// import { _ } from 'svelte-i18n'
import CanvasEditor from "$lib/components/Editor.svelte"
import * as THREE from "three"
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { onMount } from 'svelte';
import { loadCstl } from "$lib/constellationLoader.ts"

import {Ori, Ari, Gem, Cap} from "$lib/assets/textures.ts"

let drawing="";
let image_input;

onMount(async () => {
  const stars_json = await import("../stars.json")
  const stars = stars_json.default
  const scene = new THREE.Scene();
  scene.background = new THREE.Color("#151515");
  let size = {
    width: window.innerWidth,
    height: window.innerHeight,
    ratio: window.innerWidth / window.innerHeight,
  }
  const camera = new THREE.PerspectiveCamera(50, size.ratio, 1, 10000) //視野角, アスペクト比, near, far

  const renderer = new THREE.WebGLRenderer( { antialias: true , preserveDrawingBuffer: true } );
  renderer.setSize( size.width, size.height );

  const controls = new OrbitControls(camera, renderer.domElement)
  // controls.maxPolarAngle = Math.PI/2;
  controls.minDistance = 1;
  // controls.maxDistance = 100;
  camera.position.set(0, 0, 1)
  scene.rotation.x = -(Math.PI/2); //+(Math.PI*23.4)/(2*90) 地軸
  controls.update();
  //星 処理
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
    var positions = [];
    var colors = [];
    stars.forEach((star) =>{
      if (star.size == i)
        positions.push(star.x, star.y, star.z);
        colors.push(star.r/255, star.g/255, star.b/255);
    })
    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
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
  //星座線 描画
  const CONSTELLATIONS = await import("../constellations.json")
  var lines = []
  const keys = Object.keys(CONSTELLATIONS);
  keys.splice(keys.indexOf("default"), 1);
  function getStarFromId(id) {
    let star_of_id;
    stars.forEach((star) => {
      if (id == star.id) { star_of_id = star }
    })
    return star_of_id
  }
  keys.forEach((key)=> {
    CONSTELLATIONS[key].flat().forEach((id) => { //データベースに保存するときにこの処理(id->position)をやっとく
      let star = getStarFromId(id)
      lines.push(star.x, star.y, star.z)
    })
  })
  var geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
  var material = new THREE.LineBasicMaterial({ color: "#151515" });
  const starLines = new THREE.LineSegments(geometry, material);
  scene.add(starLines);
  //北極星
  var geometry = new THREE.SphereGeometry(20, 32, 16);
  var material = new THREE.MeshBasicMaterial({ color: "#fff" });
  var sphere = new THREE.Mesh( geometry, material );
  sphere.position.z = 1000
  // scene.add( sphere );
  //透明な球
  var geometry = new THREE.SphereGeometry(990, 100, 100);
  var material = new THREE.MeshLambertMaterial({ transparent: true, opacity: 0.8 });
  // const loader = new THREE.TextureLoader();
  // const textures_path = ["Ori", "Cap", "Gem", "Ari"]
  // const textures = []
  var sphere = new THREE.Mesh( geometry, material );
  scene.add(sphere);
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
  document.getElementById("drawtest").addEventListener("click", () => {
    var geometry = new THREE.PlaneGeometry( 300, 300 );
    var material = new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, transparent: true });
    const encoded_canvas = drawing.toDataURL("image/png", 1)
    material.map = new THREE.TextureLoader().load(encoded_canvas)
    var plane = new THREE.Mesh(geometry, material);
    plane.rotation.set(-Math.PI/2, -Math.PI, Math.PI)
    plane.position.set(0,1000,0)
    scene.add(plane);
    const textureRotationFolder = gui.addFolder('Texture Rotation')
    textureRotationFolder.add(plane.rotation, 'x', -Math.PI, Math.PI)
    textureRotationFolder.add(plane.rotation, 'y', -Math.PI, Math.PI)
    textureRotationFolder.add(plane.rotation, 'z', -Math.PI, Math.PI)
    textureRotationFolder.open()
    const texturePositionFolder = gui.addFolder('Texture Position')
    texturePositionFolder.add(plane.position, 'x', -1000, 1000)
    texturePositionFolder.add(plane.position, 'y', -1000, 1000)
    texturePositionFolder.add(plane.position, 'z', -1000, 1000)
    texturePositionFolder.open()
  })
  document.getElementById("picturetest").addEventListener("click", () => {
    const file = image_input.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function (e) {
      var image = new Image()
      image.src = e.target.result
      image.onload = function () {
        var geometry = new THREE.PlaneGeometry( this.width, this.height );
        var material = new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, transparent: true });
        var userImageURL = URL.createObjectURL(file);
        material.map = new THREE.TextureLoader().load(userImageURL)
        var plane = new THREE.Mesh(geometry, material);
        plane.rotation.set(-Math.PI/2, -Math.PI, Math.PI)
        plane.position.set(0,1000,0)
        scene.add(plane);
        const textureRotationFolder = gui.addFolder('Image Texture Rotation')
        textureRotationFolder.add(plane.rotation, 'x', -Math.PI, Math.PI)
        textureRotationFolder.add(plane.rotation, 'y', -Math.PI, Math.PI)
        textureRotationFolder.add(plane.rotation, 'z', -Math.PI, Math.PI)
        textureRotationFolder.open()
        const texturePositionFolder = gui.addFolder('Image Texture Position')
        texturePositionFolder.add(plane.position, 'x', -1000, 1000)
        texturePositionFolder.add(plane.position, 'y', -1000, 1000)
        texturePositionFolder.add(plane.position, 'z', -1000, 1000)
        texturePositionFolder.open()
      };
    };
  })
  const dat = await import('dat.gui')
  const gui = new dat.GUI()
  const cameraFolder = gui.addFolder('Camera lookat')
  cameraFolder.add(camera.position, 'x', -10, 10)
  cameraFolder.add(camera.position, 'y', -10, 10)
  cameraFolder.add(camera.position, 'z', -10, 10)
  const lineFolder = gui.addFolder('Star Lines color(なぜか255で割られてる)')
  lineFolder.add(starLines.material.color, 'r', 0, 1)
  lineFolder.add(starLines.material.color, 'g', 0, 1)
  lineFolder.add(starLines.material.color, 'b', 0, 1)
  lineFolder.open()
  const sceneFolder = gui.addFolder('Scene rotation')
  sceneFolder.add(scene.rotation, 'x', -Math.PI, Math.PI)
  sceneFolder.add(scene.rotation, 'y', -Math.PI, Math.PI)
  sceneFolder.add(scene.rotation, 'z', -Math.PI, Math.PI)
  document.body.appendChild( renderer.domElement );
  renderer.render(scene, camera);
  function animate() {
    controls.update();
    renderer.render( scene, camera );
    requestAnimationFrame( animate );
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
  <CanvasEditor bind:canvas={drawing} bind:im_file={image_input} />
  <button style="position: absolute; z-index: 1; left: calc(4rem + 20px); top: 15px" id="drawtest">お絵描き描画</button>
  <button style="position: absolute; z-index: 1; left: calc(10rem + 20px); top: 15px" id="picturetest">写真描画</button>
  <!-- <DevelopMode /> -->
</div>
<style>
	:global(body) {
    overflow: hidden;
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
