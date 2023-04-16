<script>
// @ts-nocheck
import CanvasEditor from "$lib/components/Editor.svelte"
import * as THREE from "three"
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { onMount } from 'svelte';
import { loadCstl, saveCstl, startQA } from "$lib/requests"

let drawing="";
let canvas_container;
let im_file;
let closed = false;
let isWaiting = false;
let isGenerataed = false;
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
  const constellations_data = await loadCstl();
  console.log(constellations_data);
  var constellations = [];
  var zodiac_positions = []
  var xarr=[];
  let orion = null;
  constellations_data.forEach((c) => {
    const [img_width, img_height] = [c["image_size"]["width"], c["image_size"]["height"]]
    var geometry = new THREE.PlaneGeometry(img_width, img_height);
    var material = new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, transparent: true });
    material.map = new THREE.TextureLoader().load(c["image"])
    var plane = new THREE.Mesh(geometry, material);
    const [x, y, z] = [c["image_coord"][0], c["image_coord"][1], c["image_coord"][2]];
    plane.position.set(x*1.001, y*1.001, z*1.001)
    //画像の目標姿勢を計算
    const place_vector = [x, y, z]
    const radian_around_y = Math.acos(z / Math.sqrt(x ** 2 + z ** 2)) * (x / Math.abs(x))
    const rotate_around_y = (vector, radian)=>{
      const [x, y, z] = vector
      const cos = Math.cos(radian)
      const sin = Math.sin(radian)
      return [cos * x + sin * z, y, -sin * x + cos * z]
    }
    const [_, y_in_zy, z_in_zy] = rotate_around_y(place_vector, -radian_around_y)
    const target_attitude = rotate_around_y([0., z_in_zy, -y_in_zy], radian_around_y)
    //x 軸まわり→y 軸周りの順に回転させながら回転角を計算
    const radian_around_x = Math.acos(z / Math.sqrt(y ** 2 + z ** 2)) * (y / Math.abs(y))
    const rotate_around_x = (vector, radian)=>{
      const [x, y, z] = vector
      const cos = Math.cos(radian)
      const sin = Math.sin(radian)
      return [x, cos * y - sin * z, sin * y + cos * z]
    }
    const [__, ___, z_in_zx] = rotate_around_x(place_vector, radian_around_x)
    const radian_around_y_in_zx = Math.acos(z_in_zx / Math.sqrt(x ** 2 + z_in_zx ** 2)) * (x / Math.abs(x))
    //目標姿勢を回転させて z 軸周りの回転角を計算
    const attitude_rotated_around_x = rotate_around_x(target_attitude, radian_around_x)
    const attitude_on_z = rotate_around_y(attitude_rotated_around_x, -radian_around_y_in_zx)
    const radian_around_z = Math.acos(attitude_on_z[1] / Math.sqrt(attitude_on_z[0] ** 2 + attitude_on_z[1] ** 2)) * (attitude_on_z[0] / Math.abs(attitude_on_z[0]))
    xarr.push({
      name: c["name"],
      x: Math.floor(x),
      y: Math.floor(y),
      z: Math.floor(z),
      x_degree: Math.round(radian_around_x * 180 / Math.PI),
      y_degree: Math.round(radian_around_y_in_zx * 180 / Math.PI),
      z_degree: Math.round(radian_around_z * 180 / Math.PI),
    });
    plane.rotation.x = -radian_around_x
    plane.rotation.y = radian_around_y_in_zx
    plane.rotation.z = -radian_around_z
    plane.name = c["name"]
    if (c["name"] == "オリオン") {orion = plane;}
    zodiac_positions.push({x: [x-img_width/2,x+img_width/2], y: [y-img_width/2,y+img_width/2], z:[z-img_width/2,z+img_width/2]})
    scene.add(plane);
    constellations.push(c["connected_stars"])
  })
  console.log(xarr);
  const camera = new THREE.PerspectiveCamera(50, window_size.ratio, 10, 10000) //視野角, アスペクト比, near, far
  camera.rotation.order = "YXZ"
  const renderer = new THREE.WebGLRenderer( { antialias: true , preserveDrawingBuffer: true } );
  renderer.setSize( window_size.width, window_size.height );

  const controls = new OrbitControls(camera, renderer.domElement)
  controls.minDistance = 1;
  controls.zoomSpeed = 1.5
  // controls.maxPolarAngle = Math.PI/2;
  // controls.maxDistance = 100;
  camera.position.set(0, 0, 0)
  // camera.translateZ(+100)
  camera.lookAt(0,100,0)
  controls.update();
  //ああああああ
<<<<<<< HEAD
  // var geometry = new THREE.BoxGeometry(5, 2000, 5);// 立方体
  // var material = new THREE.MeshBasicMaterial({color: "#ff0"});// 影が表示される
  // var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  // cube.position.y = 1000
  // scene.add(cube);
  // var geometry = new THREE.BoxGeometry(5, 2000, 5);// 立方体
  // var material = new THREE.MeshBasicMaterial({color: "#990"});// 影が表示される
  // var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  // cube.position.y = -1000
  // scene.add(cube);
  // var geometry = new THREE.BoxGeometry(2000, 5, 5);// 立方体
  // var material = new THREE.MeshBasicMaterial({color: "#0f0"});// 影が表示される
  // var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  // cube.position.x = 1000
  // scene.add(cube);
  // var geometry = new THREE.BoxGeometry(2000, 5, 5);// 立方体
  // var material = new THREE.MeshBasicMaterial({color: "#090"});// 影が表示される
  // var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  // cube.position.x = -1000
  // scene.add(cube);
  // var geometry = new THREE.BoxGeometry(5, 5, 2000);// 立方体
  // var material = new THREE.MeshBasicMaterial({color: "#f00"});// 影が表示される
  // var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  // cube.position.z = 1000
  // scene.add(cube);
  // var material = new THREE.MeshBasicMaterial({color: "#900"});// 影が表示される
  // var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  // cube.position.z = -1000
  // scene.add(cube);
=======
  var geometry = new THREE.BoxGeometry(5, 2000, 5);// 立方体
  var material = new THREE.MeshBasicMaterial({color: "#ff0"});// 影が表示される
  var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  cube.position.y = 1000
  //scene.add(cube);
  var geometry = new THREE.BoxGeometry(5, 2000, 5);// 立方体
  var material = new THREE.MeshBasicMaterial({color: "#990"});// 影が表示される
  var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  cube.position.y = -1000
  //scene.add(cube);
  var geometry = new THREE.BoxGeometry(2000, 5, 5);// 立方体
  var material = new THREE.MeshBasicMaterial({color: "#0f0"});// 影が表示される
  var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  cube.position.x = 1000
  //scene.add(cube);
  var geometry = new THREE.BoxGeometry(2000, 5, 5);// 立方体
  var material = new THREE.MeshBasicMaterial({color: "#090"});// 影が表示される
  var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  cube.position.x = -1000
  //scene.add(cube);
  var geometry = new THREE.BoxGeometry(5, 5, 2000);// 立方体
  var material = new THREE.MeshBasicMaterial({color: "#f00"});// 影が表示される
  var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  cube.position.z = 1000
  //scene.add(cube);
  var material = new THREE.MeshBasicMaterial({color: "#900"});// 影が表示される
  var cube = new THREE.Mesh(geometry, material);// それらをまとめて3Dオブジェクトにします
  cube.position.z = -1000
  //scene.add(cube);
>>>>>>> 366581d560941a2b620ed89012790186047631af
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
  // const CONSTELLATIONS = await import("../constellations.json")
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
  constellations.flat().flat().forEach((id) => {
      let star = getStarFromId(id)
      lines.push(star.x, star.y, star.z)
  })
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
  var material = new THREE.MeshBasicMaterial( {color: "#B5A48A", side: THREE.DoubleSide} );
  var plane = new THREE.Mesh( geometry, material );
  plane.rotation.z = Math.PI / 2;
  // scene.add( plane );

  const dat = await import('dat.gui');
  const gui = new dat.GUI()
  // const lineFolder = gui.addFolder('Star Lines color')
  // lineFolder.add(starLines.material.color, 'r', 0, 1)
  // lineFolder.add(starLines.material.color, 'g', 0, 1)
  // lineFolder.add(starLines.material.color, 'b', 0, 1)
  // lineFolder.open()
  const sceneFolder = gui.addFolder('Orion Rotation')
  sceneFolder.add(orion.rotation, 'x', -Math.PI, Math.PI)
  sceneFolder.add(orion.rotation, 'y', -Math.PI, Math.PI)
  sceneFolder.add(orion.rotation, 'z', -Math.PI, Math.PI)
  // sceneFolder.add(camera.position, 'x', -1000, 1000)
  // sceneFolder.add(camera.position, 'y', -1000, 1000)
  // sceneFolder.add(camera.position, 'z', -1000, 1000)
  document.body.appendChild( renderer.domElement );
  renderer.render(scene, camera);
  function animate() {
    controls.update();
    renderer.render( scene, camera );
    requestAnimationFrame( animate );
  }
  animate()
  document.getElementById("drawtest").addEventListener("click", () => {
    var geometry = new THREE.PlaneGeometry( 300, 300 );
    var material = new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, transparent: true });
    const encoded_canvas = drawing;
    material.map = new THREE.TextureLoader().load(encoded_canvas)
    var plane = new THREE.Mesh(geometry, material);
    plane.rotation.set(0,0,0)
    plane.position.set(0,0,-1000)
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
    var file = im_file.files[0];
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
        // plane.rotation.set(-Math.PI/2, -Math.PI, Math.PI)
        // plane.position.set(0,1000,0)
        plane.rotation.set(0,0,0)
        plane.position.set(0,0,-1000)
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
  document.getElementById("toggle_mode").addEventListener("click", () => {
    if (mode == "drawing"){
      mode = "image"
    } else {
      mode="drawing";
    }
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
    var vector = new THREE.Vector3();
    var cameraVector = camera.getWorldDirection(vector);
    var lookat = [];
    Object.keys(cameraVector).forEach(key => lookat.push(cameraVector[key] * 1000));
    function checkOverlap() {
      return !zodiac_positions.some((p) => {
        return ((p["x"][0] < lookat[0] && lookat[0] < p["x"][1]) && (p["y"][0] < lookat[1] && lookat[1] < p["y"][1]) && (p["z"][0] < lookat[2] && lookat[2] < p["z"][1]))
      })
    }
    if (checkOverlap()) {
    isWaiting = true;
    var img_content
    var img_size;
    if (mode == "drawing") {
      img_content = drawing;
      if (img_content == "") { alert("ちゃんとお絵描きしてください。"); isWaiting = false; } else {
      img_size = {width: 300, height: 300};
      const res = await startQA({
        image:img_content,
        angle:lookat,
        max_mag:8,
        blur_radius:15,
        pixel_rate:20000
      });
      saveCstl(
        document.getElementById("name").value, //star_name
        res, //stars_connection
        img_content, //image
        lookat, //coord
        img_size, // `[${img_size.x}, ${img_size.y}]` //size
      )
      isWaiting = false;
      isGenerataed = true;
      }} else if (mode == "image") {
        var file = await im_file.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = async function (e) {
          img_content = e.target.result;
          var img = new Image()
          img.src = e.target.result
          img.onload = async function () {
            img_size = { width: this.width, height: this.height };
            const res = await startQA({
              image:img_content,
              angle:lookat,
              max_mag:document.getElementById("max_mag").value,
              blur_radius:document.getElementById("blur_rad").value,
              pixel_rate:document.getElementById("pixel_rate").value
            });
            console.log(res);
            saveCstl(
              document.getElementById("name").value, //star_name
              res, //stars_connection
              img_content, //image
              lookat, //coord
              img_size, // `[${img_size.x}, ${img_size.y}]` //size
            )
            isWaiting = false;
            isGenerataed = true;
          };
        }
      }
    } else { alert("使われていない領域を選択してください。") }
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
  <title>QZ4U ~Quantum Zodiac maker for you~</title>
  <meta property="og:url" content="https://qac.vercel.app/">
  <meta property="og:title" content="QZ4U ~Quantum Zodiac maker for you~">
  <meta property="og:description" content="量子アニーリングを使ってお絵描きや透過画像から星座を生成するアプリです">
  <meta property="og:image" content="">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta property="twitter:domain" content="qac.vercel.app">
  <meta property="twitter:url" content="https://qac.vercel.app/">
  <meta name="twitter:title" content="QZ4U ~Quantum Zodiac maker for you~">
  <meta name="twitter:description" content="量子アニーリングを使ってお絵描きや透過画像から星座を生成するアプリです">
  <meta name="twitter:image" content="">
</svelte:head>

<div id="container">
  <div id="canvas_container" bind:this={canvas_container}>
    <button id="toggle_mode">🫰</button>
    <div style="display: {mode == "drawing" ? "inline" : "none"};">
      <span>お絵描き</span>
      <CanvasEditor bind:png={drawing} bind:disable={isWaiting} />
      <button id="drawtest">お絵描き描画</button>
    </div>
    <div style="display: {mode == "drawing" ? "none" : "inline"};">
      <span>画像</span>
      <div>
        <input type="file" accept="image/png" bind:this={im_file}>
      </div>
      <button id="picturetest">写真描画</button>
    </div>
    <div>
      <div>
        <label for="name">星座名</label>
        <input id="name" type="text" />
      </div>
      <div>
        <label for="pixel_rate">何ピクセル毎に星1つか</label>
        <input id="pixel_rate" value="10000" type="number" class="mini"/>
      </div>
      <div>
        <label for="max_mag">使う最大の等級</label>
        <input id="max_mag" value="8" type="number" class="mini"/>
      </div>
      <div>
        <label for="blur_rad">ぼかし度合い</label>
        <input id="blur_rad" value="15" type="number" class="mini"/>
      </div>
      <button id="send">生成</button>
    </div>
    <button id="btn_toggle_closed">{closed? ">": "<"}</button>
  </div>
</div>
<div class="toast">
  {#if isWaiting && !isGenerataed}
  <p>生成中...お待ちください。(大体2分くらいかかります)</p>
  {:else if isGenerataed}
  <p>生成完了！リロードしてください。</p>
  {/if}
</div>
<style>
	:global(body) {
    overflow: hidden;
		margin: 0;
	}
  #canvas_container {
    border: 2px solid black;
    position: absolute;
    width: 300px;
    /* height: 400px; */
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
.toast {
  position: fixed;
  bottom: 0;
  left: 0;
  /* background: #444; */
  color: white;
  font-size: 1.3rem;
}
.mini {
  width: 100px
}
</style>
