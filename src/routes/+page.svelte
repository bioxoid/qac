<script>
// @ts-nocheck
import CanvasEditor from "$lib/components/Editor.svelte"
import * as THREE from "three"
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { onMount } from 'svelte';
import { loadCstl, saveCstl, startQA } from "$lib/requests.ts"

let drawing="";
let canvas_container;
let im_file;
let closed = false;
let mode = "drawing";
onMount(async () => {
  const stars_json = await import("../stars.json")
  const stars = stars_json.default
  const scene = new THREE.Scene();
  scene.background = new THREE.Color("#151515");
  let window_size = {
    width: window.innerWidth,
    height: window.innerHeight,
    ratio: window.innerWidth / window.innerHeight,
  }
  const sheets = await loadCstl();
  var values = sheets.values;
  values.splice(0, 1)
  var constellations = [];
  values.forEach((row) => {
    constellations.push(JSON.parse(row[5]))
  })
  const camera = new THREE.PerspectiveCamera(50, window_size.ratio, 1, 10000) //視野角, アスペクト比, near, far
  camera.rotation.order = "YXZ"
  const renderer = new THREE.WebGLRenderer( { antialias: true , preserveDrawingBuffer: true } );
  renderer.setSize( window_size.width, window_size.height );

  const controls = new OrbitControls(camera, renderer.domElement)
  // controls.maxPolarAngle = Math.PI/2;
  controls.minDistance = 1;
  // controls.maxDistance = 100;
  // var vector = new THREE.Vector3(); // create once and reuse it!
  // var vector = new THREE.Vector3( 0, 0, - 1 );
  // vector.applyQuaternion( camera.quaternion );
  // var angle = vector.angleTo( target.position );

  camera.position.set(0, 0, 1)
  // scene.rotation.x = -(Math.PI/2); //+(Math.PI*23.4)/(2*90) 地軸
  controls.update();
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
  function getStarFromId(id) {
    let star_of_id;
    stars.forEach((star) => {
      if (id == star.id) { star_of_id = star }
    })
    return star_of_id
  }
  // const keys = Object.keys(CONSTELLATIONS); // const keys = Object.keys(CONSTELLATIONS);
  // keys.splice(keys.indexOf("default"), 1);
  // keys.forEach((key)=> {
  //   CONSTELLATIONS[key].flat().forEach((id) => { //データベースに保存するときにこの処理(id->position)をやっとく
  //     let star = getStarFromId(id)
  //     lines.push(star.x, star.y, star.z)
  //   })
  // })
  constellations.flat().flat().forEach((id) => { //データベースに保存するときにこの処理(id->position)をやっとく
      let star = getStarFromId(id)
      lines.push(star.x, star.y, star.z)
    })
    console.log(lines);
  var geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(lines, 3));
  var material = new THREE.LineBasicMaterial({ color: "#15f5f5" });
  const starLines = new THREE.LineSegments(geometry, material);
  scene.add(starLines);
  //透明な球
  var geometry = new THREE.SphereGeometry(990, 100, 100);
  var material = new THREE.MeshLambertMaterial({ transparent: true, opacity: 0.8 });
  var sphere = new THREE.Mesh( geometry, material );
  scene.add(sphere);
  //地面
  var geometry = new THREE.PlaneGeometry( 2000, 2000 );
  var material = new THREE.MeshBasicMaterial( {color: "#1F365A", side: THREE.DoubleSide} );
  var plane = new THREE.Mesh( geometry, material );
  plane.rotation.z = Math.PI / 2;
  // var rc = new THREE.Raycaster();
  // scene.add( plane );
  // var m = new THREE.Vector2();
  // function onMouseMove(event) {
  //   m.x = event.clientX
  //   m.y = event.clientY
  //   rc.setFromCamera(m, camera);
  //   intscs = rc.intersectObjects()
  // }
  // document.getElementById("drawtest").addEventListener("click", () => {
  //   var geometry = new THREE.PlaneGeometry( 300, 300 );
  //   var material = new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, transparent: true });
  //   const encoded_canvas = drawing;
  //   material.map = new THREE.TextureLoader().load(encoded_canvas)
  //   var plane = new THREE.Mesh(geometry, material);
  //   plane.rotation.set(-Math.PI/2, -Math.PI, Math.PI)
  //   plane.position.set(0,1000,0)
  //   scene.add(plane);
  //   const textureRotationFolder = gui.addFolder('Texture Rotation')
  //   textureRotationFolder.add(plane.rotation, 'x', -Math.PI, Math.PI)
  //   textureRotationFolder.add(plane.rotation, 'y', -Math.PI, Math.PI)
  //   textureRotationFolder.add(plane.rotation, 'z', -Math.PI, Math.PI)
  //   textureRotationFolder.open()
  //   const texturePositionFolder = gui.addFolder('Texture Position')
  //   texturePositionFolder.add(plane.position, 'x', -1000, 1000)
  //   texturePositionFolder.add(plane.position, 'y', -1000, 1000)
  //   texturePositionFolder.add(plane.position, 'z', -1000, 1000)
  //   texturePositionFolder.open()
  // })
  // document.getElementById("picturetest").addEventListener("click", () => {
  //   // console.log(camera.getWorldDirection())
  //   const file = image_input.files[0];
  //   var reader = new FileReader();
  //   reader.readAsDataURL(file);
  //   reader.onload = function (e) {
  //     var image = new Image()
  //     image.src = e.target.result
  //     image.onload = function () {
  //       var geometry = new THREE.PlaneGeometry( this.width, this.height );
  //       var material = new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, transparent: true });
  //       var userImageURL = URL.createObjectURL(file);
  //       material.map = new THREE.TextureLoader().load(userImageURL)
  //       var plane = new THREE.Mesh(geometry, material);
  //       plane.rotation.set(-Math.PI/2, -Math.PI, Math.PI)
  //       plane.position.set(0,1000,0)
  //       scene.add(plane);
  //       const textureRotationFolder = gui.addFolder('Image Texture Rotation')
  //       textureRotationFolder.add(plane.rotation, 'x', -Math.PI, Math.PI)
  //       textureRotationFolder.add(plane.rotation, 'y', -Math.PI, Math.PI)
  //       textureRotationFolder.add(plane.rotation, 'z', -Math.PI, Math.PI)
  //       textureRotationFolder.open()
  //       const texturePositionFolder = gui.addFolder('Image Texture Position')
  //       texturePositionFolder.add(plane.position, 'x', -1000, 1000)
  //       texturePositionFolder.add(plane.position, 'y', -1000, 1000)
  //       texturePositionFolder.add(plane.position, 'z', -1000, 1000)
  //       texturePositionFolder.open()
  //     };
  //   };
  // })
  const dat = await import('dat.gui');
  const gui = new dat.GUI()
  const cameraFolder = gui.addFolder('Camera lookat')
  cameraFolder.add(camera.rotation, 'x', -Math.PI, Math.PI)
  cameraFolder.add(camera.rotation, 'y', -Math.PI, Math.PI)
  cameraFolder.add(camera.rotation, 'z', -Math.PI, Math.PI)
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
  document.getElementById("toggle_mode").addEventListener("click", () => {
    mode == "drawing" ? mode = "image" : mode="drawing";
  })
  document.getElementById("btn_toggle_closed").addEventListener("click", (e) => {
    const rect = canvas_container.getBoundingClientRect();
    if (closed) {
      canvas_container.style.left = 0 + "px"
    } else {
      canvas_container.style.left = -rect.width + "px"
    }
    closed = !closed
  })
  document.getElementById("send").addEventListener("click", async() => {
    var img_content;
    var img_size;
    if (mode == "drawing") {
      img_content = drawing;
      img_size = {x: 300, y: 300};
    } else if (mode == "image") {
      var file = await im_file.files[0];
      var reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = async function (e) {
        img_content = e.target.result;
        var img = new Image()
        img.src = e.target.result
        img.onload = async function () {
          img_size = {x: this.width, y: this.height};
        }
      const res = await startQA({image:img_content, angle:[0,0,0], max_mag:8, blur_radius:15, pixel_rate:20000});
      console.log(res[1]);
      saveCstl(
        document.getElementById("name").value,
        "",
        "[" + res[1] + "]",
        img_content,
        "",
        `[${img_size.x}, ${img_size.y}]`
        )
      };
    }
    const circle = 2 * Math.PI * 1000
    const img_deg = circle / 200
    var vector = new THREE.Vector3();
    var cameraVector = camera.getWorldDirection(vector);
    var deg = Math.atan2(cameraVector.y, cameraVector.x);
    var rad = [];
    Object.keys(cameraVector).forEach(key => rad.push(cameraVector[key] * Math.PI));
    console.log(rad);
    // const data = image.data
    // const drawn_pixels = [];
    // const drawn_pixel_ids = [];
    // var row = 0;
    // for (let i=3; i <= data.length; i+=4) {
    //   let pixel_number = Math.floor(i/4);
    //   if (pixel_number>=canvas_size.x*row) { drawn_pixels.push([]); row += 1; }
    //   if (data[i] !== 0) {
    //     drawn_pixels[row-1].push(1)
    //     drawn_pixel_ids.push(pixel_number)
    //   } else {
    //     drawn_pixels[row-1].push(0)
    //   }
    // }
  })
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
  <div id="canvas_container" bind:this={canvas_container}>
    <button id="toggle_mode">🫰</button>
    {#if mode == "drawing"}
    <span>お絵描き</span>
    <CanvasEditor bind:png={drawing}/>
    <!-- <button id="drawtest">お絵描き描画</button> -->
    {:else if mode == "image"}
    <span>画像</span>
    <div>
      <input type="file" accept="image/png" bind:this={im_file}>
    </div>
    <!-- <button id="picturetest">写真描画</button> -->
    {/if}
    <div>
      <label for="name">星座名</label>
      <input id="name" />
      <button id="send">生成</button>
    </div>
  <button id="btn_toggle_closed">{closed? ">": "<"}</button>
  <!-- <DevelopMode /> -->
</div>
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
  #canvas_container {
    border: 2px solid black;
    position: absolute;
    width: 300px;
    height: 400px;
    padding: 10px;
    left: 0px;
    top: 10px;
    background-color: rgba(244, 244, 244, 0.5);
    z-index: 1;
    transition: all 0.3s ease;
}
  #btn_toggle_closed {
  position: absolute;
  top: 0;
  right: -1.2rem;
  border: none;
  background: rgb(244, 244, 244, 0.5);
  width: 1.2rem;
  height: 1.2rem;
  color: white;
}
#btn_toggle_closed:hover {
  background: #333
}
</style>
