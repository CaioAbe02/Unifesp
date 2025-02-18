function main() {
  const canvas = document.querySelector("#canvas");
  const gl = canvas.getContext('webgl', { preserveDrawingBuffer: true });

  if (!gl) {
    throw new Error('WebGL not supported');
  }

  var vertexShaderSource = document.querySelector("#vertex-shader").text;
  var fragmentShaderSource = document.querySelector("#fragment-shader").text;

  var vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
  var fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

  var program = createProgram(gl, vertexShader, fragmentShader);

  gl.useProgram(program);

  gl.enable(gl.DEPTH_TEST);

  var ambientReflectionLocation = gl.getUniformLocation(program, `uAmbientReflection`);
  var diffuseReflectionLocation = gl.getUniformLocation(program, `uDiffuseReflection`);
  var specularReflectionLocation = gl.getUniformLocation(program, `uSpecularReflection`);
  gl.uniform3fv(ambientReflectionLocation, new Float32Array([1.0, 1.0, 1.0]));
  gl.uniform3fv(diffuseReflectionLocation, new Float32Array([1.0, 1.0, 1.0]));
  gl.uniform3fv(specularReflectionLocation, new Float32Array([0.0, 0.0, 0.0]));


  const modelMatrixUniformLocation = gl.getUniformLocation(program, `uModelMatrix`);
  const viewMatrixUniformLocation = gl.getUniformLocation(program, `uViewMatrix`);
  const projectionMatrixUniformLocation = gl.getUniformLocation(program, `uProjectionMatrix`);
  const inverseTransposeModelMatrixUniformLocation = gl.getUniformLocation(program, `uInverseTransposeModelMatrix`);
  var lightPositionsLocation = gl.getUniformLocation(program, `uLightPosition`);
  var viewPositionLocation = gl.getUniformLocation(program, `uViewPosition`);
  var shininessLocation = gl.getUniformLocation(program, `uShininess`);

  gl.uniform3fv(lightPositionsLocation, new Float32Array(
    [
      -2.0, 1.0, 1.0,
      1.0, -1.0, 1.0
    ]));
  gl.uniform1f(shininessLocation, 250.0);

  gl.clearColor(0.0, 0.0, 0.0, 1.0);

  // Points
  let game_over = false;
  let next_checkpoint_up = true;
  let points = 0.0;
  document.getElementById('points').textContent = Math.floor(points);
  let bonus_velocity = 0.0

  // Listener de teclado
  const bodyElement = document.querySelector("body");
  bodyElement.addEventListener("keydown", keyDown, false);
  bodyElement.addEventListener("keyup", keyUp, false);

  let keysPressed = {};

  function keyDown(event) {
    keysPressed[event.key] = true;
  }

  function keyUp(event) {
    keysPressed[event.key] = false;
  }

  function isKeyPressed(key) {
    return keysPressed[key] === true;
  }

  // Player data
  const playerPositionBuffer = gl.createBuffer();
  const playerNormalBuffer = gl.createBuffer();
  const playerColorBuffer = gl.createBuffer();

  const player_locations = setLocations(gl, program, playerPositionBuffer, playerNormalBuffer, playerColorBuffer);
  addToBuffer(gl, playerPositionBuffer, playerNormalBuffer, playerColorBuffer, setPlayerVertices(), setPlayerNormals(), setPlayerColors());

  let rotation = 0.0
  const tx_player_initial = -2.0;
  const tz_player_initial = 0.0;
  const t_step_player_initial = 0.01;
  let tx_player = tx_player_initial;
  let tz_player = tz_player_initial;
  let t_step_player = t_step_player_initial;
  const halfXPlayer = 0.1;
  const halfZPlayer = 0.1;

  // Car 1 data
  const carPositionBuffer = gl.createBuffer();
  const carNormalBuffer = gl.createBuffer();
  const carColorBuffer = gl.createBuffer();

  const car_locations = setLocations(gl, program, carPositionBuffer, carNormalBuffer, carColorBuffer);
  addToBuffer(gl, carPositionBuffer, carNormalBuffer, carColorBuffer, setCarVertices(), setCarNormals(), setCarColorsVertices());

  const tx_car1_initial = 0.5;
  const tz_car1_initial = 4.0;
  const t_step_car1_initial = 0.02;
  let tx_car1 = tx_car1_initial;
  let tz_car1 = tz_car1_initial;
  let t_step_car1 = t_step_car1_initial;
  const halfXCar = 0.15;
  const halfZCar = 0.3;

  // Car 2 data
  const yellowCarColorBuffer = gl.createBuffer();

  addToBuffer(gl, carPositionBuffer, carNormalBuffer, yellowCarColorBuffer, setCarVertices(), setCarNormals(), setYellowCarColorsVertices());

  const tx_car2_initial = 1.0;
  const tz_car2_initial = 5.0;
  const t_step_car2_initial = 0.015;
  let tx_car2 = tx_car2_initial;
  let tz_car2 = tz_car2_initial;
  let t_step_car2 = t_step_car2_initial;

  // Car 3 data
  const tx_car3_initial = -0.5;
  const tz_car3_initial = 4.0;
  const t_step_car3_initial = -0.018;
  let tx_car3 = tx_car3_initial;
  let tz_car3 = tz_car3_initial;
  let t_step_car3 = t_step_car3_initial;

  // Car 4 data
  const purpleCarColorBuffer = gl.createBuffer();

  addToBuffer(gl, carPositionBuffer, carNormalBuffer, purpleCarColorBuffer, setCarVertices(), setCarNormals(), setPurpleCarColorsVertices());

  const tx_car4_initial = -1.0;
  const tz_car4_initial = 6.0;
  const t_step_car4_initial = -0.035;
  let tx_car4 = tx_car4_initial;
  let tz_car4 = tz_car4_initial;
  let t_step_car4 = t_step_car4_initial;

  // Checkpoint Up Data
  const checkpointPositionBuffer = gl.createBuffer();
  const checkpointNormalBuffer = gl.createBuffer();
  const checkpointColorBuffer = gl.createBuffer();

  const checkpoint_locations = setLocations(gl, program, checkpointPositionBuffer, checkpointNormalBuffer, checkpointColorBuffer);
  addToBuffer(gl, checkpointPositionBuffer, checkpointNormalBuffer, checkpointColorBuffer, setCheckpointVertices(), setTerrainNormals(), setCheckpointColors());

  let tx_checkpointUp = 1.6;
  let tz_checkpointUp = 0.0;
  const halfXCheckpoint = 2.8;
  const halfZCheckpoint = 5.0;

  // Checkpoint Down Data
  let tx_checkpointDown = -4.2;
  let tz_checkpointDown = 0.0;

  // Road Data
  const roadPositionBuffer = gl.createBuffer();
  const roadNormalBuffer = gl.createBuffer();
  const roadColorBuffer = gl.createBuffer();

  const road_locations = setLocations(gl, program, roadPositionBuffer, roadNormalBuffer, carColorBuffer);
  addToBuffer(gl, roadPositionBuffer, roadNormalBuffer, roadColorBuffer, setRoadVertices(), setTerrainNormals(), setRoadColors());

  let tx_road = 0.0;
  let tz_road = 0.0;

  // Camera
  gl.viewport(0, 0, canvas.width, canvas.height);
  let theta = 1.0;
  const xw_min = -0.5, xw_max = 0.5;
  const yw_min = -0.5, yw_max = 0.5;
  const z_near = -1.0, z_far = 10.0;
  let P0 = [4.0 * Math.sin(-theta), 1.7, 4.0 * Math.cos(-theta)];
  P_ref = [0.0, 0.0, 0.0];
  V = [0.0, 1.0, 0.0];
  let viewingMatrix = set3dViewingMatrix(P0, P_ref, V);

  gl.uniform3fv(viewPositionLocation, new Float32Array(P0));
  gl.uniformMatrix4fv(viewMatrixUniformLocation, false, viewingMatrix);

  let projectionMatrix = m4.identity();
  projectionMatrix = perspectiveProjection(xw_min, xw_max, yw_min, yw_max, z_near, z_far);
  gl.uniformMatrix4fv(projectionMatrixUniformLocation, false, projectionMatrix);

  function updateScene() {
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Collision detection
    const collisionXCar1 = Math.abs(tx_player - tx_car1) <= (halfXPlayer + halfXCar);
    const collisionZCar1 = Math.abs(tz_player - tz_car1) <= (halfZPlayer + halfZCar);

    const collisionXCar2 = Math.abs(tx_player - tx_car2) <= (halfXPlayer + halfXCar);
    const collisionZCar2 = Math.abs(tz_player - tz_car2) <= (halfZPlayer + halfZCar);

    const collisionXCar3 = Math.abs(tx_player - tx_car3) <= (halfXPlayer + halfXCar);
    const collisionZCar3 = Math.abs(tz_player - tz_car3) <= (halfZPlayer + halfZCar);

    const collisionXCar4 = Math.abs(tx_player - tx_car4) <= (halfXPlayer + halfXCar);
    const collisionZCar4 = Math.abs(tz_player - tz_car4) <= (halfZPlayer + halfZCar);

    const collisionXCheckpointDown = Math.abs(tx_player - tx_checkpointDown) <= (halfXPlayer + halfXCheckpoint);
    const collisionZCheckpointDown = Math.abs(tz_player - tz_checkpointDown) <= (halfZPlayer + halfZCheckpoint);

    const collisionXCheckpointUp = Math.abs(tx_player - tx_checkpointUp) <= (halfXPlayer + halfXCheckpoint - 2.1);
    const collisionZCheckpointUp = Math.abs(tz_player - tz_checkpointUp) <= (halfZPlayer + halfZCheckpoint);

    if (collisionXCar1 && collisionZCar1 || collisionXCar2 && collisionZCar2 || collisionXCar3 && collisionZCar3 || collisionXCar4 && collisionZCar4) {
      console.log('🚨 COLISÃO DETECTADA! 🚗💥');
      game_over = true;
      t_step_player = 0;
      t_step_car1 = 0;
      t_step_car2 = 0;
      t_step_car3 = 0;
      t_step_car4 = 0;
      bonus_velocity = 0.0;
    }
    if (collisionXCheckpointDown && collisionZCheckpointDown) {
      if (!next_checkpoint_up) {
        console.log('COLISÃO CHECKPOINT DOWN!');
        points += 10;
        bonus_velocity += 0.005;
      }
      next_checkpoint_up = true;
    }
    if (collisionXCheckpointUp && collisionZCheckpointUp) {
      if (next_checkpoint_up) {
        console.log('COLISÃO CHECKPOINT UP!');
        points += 10;
        bonus_velocity += 0.005;
      }
      next_checkpoint_up = false;
    }
    document.getElementById('points').textContent = Math.floor(points);

    // Player moviment
    if (!game_over) {
      if (isKeyPressed('w') || isKeyPressed('ArrowUp')) {
        tx_player += t_step_player
        rotation = 0.0
      }
      if (isKeyPressed('s') || isKeyPressed('ArrowDown')) {
        tx_player -= t_step_player
        rotation = -180.0
      }
      if (isKeyPressed('d') || isKeyPressed('ArrowRight')) {
        if (tz_player < 4) {
          tz_player += t_step_player
          rotation = -90.0
        }
      }
      if (isKeyPressed('a') || isKeyPressed('ArrowLeft')) {
        if (tz_player > -4) {
          tz_player -= t_step_player
          rotation = 90.0
        }
      }
    }
    else {
      if (isKeyPressed('r')) {
        game_over = false;
        next_checkpoint_up = true;
        points = 0;
        tx_player = -2.0;
        tz_player = 0.0;
        t_step_player = t_step_player_initial;
        tx_car1 = tx_car1_initial;
        tz_car1 = tz_car1_initial;
        t_step_car1 = t_step_car1_initial;
        tx_car2 = tx_car2_initial;
        tz_car2 = tz_car2_initial;
        t_step_car2 = t_step_car2_initial;
        tx_car3 = tx_car3_initial;
        tz_car3 = tz_car3_initial;
        t_step_car3 = t_step_car3_initial;
        tx_car4 = tx_car4_initial;
        tz_car4 = tz_car4_initial;
        t_step_car4 = t_step_car4_initial;
      }
    }

    // Light Positions
    gl.uniform3fv(lightPositionsLocation, new Float32Array(
      [
        tx_car1 + 0.2, 0.7, tz_car1 - 0.7,
        tx_car2 + 0.2, 0.7, tz_car2 - 0.7,
        tx_car3 + 0.2, 0.7, tz_car3 + 0.7,
        tx_car4 + 0.2, 0.7, tz_car4 + 0.7,
      ]));

    // Draw Player
    let modelMatrix = m4.identity();
    modelMatrix = m4.translate(modelMatrix, tx_player, 0, tz_player);
    modelMatrix = m4.yRotate(modelMatrix, degToRad(rotation));

    drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, setPlayerVertices(),
              playerPositionBuffer, playerNormalBuffer, playerColorBuffer, player_locations);

    // Car 1 moviment
    if (tz_car1 < -4) {
      tz_car1 = 4
    }
    tz_car1 -= t_step_car1 + bonus_velocity;

    // Draw Car 1
    modelMatrix = m4.identity();
    modelMatrix = m4.translate(modelMatrix, tx_car1, 0.0, tz_car1);

    drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, setCarVertices(),
              carPositionBuffer, carNormalBuffer, carColorBuffer, car_locations);

    // Car 2 moviment
    if (tz_car2 < -4) {
      tz_car2 = 4
    }
    tz_car2 -= t_step_car2 + bonus_velocity;

    // Draw Car 2
    modelMatrix = m4.identity();
    modelMatrix = m4.translate(modelMatrix, tx_car2, 0.0, tz_car2);

    drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, setCarVertices(),
              carPositionBuffer, carNormalBuffer, yellowCarColorBuffer, car_locations);

    // Car 3 moviment
    if (tz_car3 > 4) {
      tz_car3 = -4
    }
    tz_car3 -= t_step_car3 - bonus_velocity;

    // Draw Car 3
    modelMatrix = m4.identity();
    modelMatrix = m4.translate(modelMatrix, tx_car3, 0.0, tz_car3);

    drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, setCarVertices(),
              carPositionBuffer, carNormalBuffer, carColorBuffer, car_locations);

    // Car 4 moviment
    if (tz_car4 > 5) {
      tz_car4 = -6
    }
    tz_car4 -= t_step_car4 - bonus_velocity;

    // Draw Car 4
    modelMatrix = m4.identity();
    modelMatrix = m4.translate(modelMatrix, tx_car4, 0.0, tz_car4);

    drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, setCarVertices(),
              carPositionBuffer, carNormalBuffer, purpleCarColorBuffer, car_locations);

    // Draw Checkpoint Up
    modelMatrix = m4.identity();
    modelMatrix = m4.translate(modelMatrix, tx_checkpointUp, 0.0, tz_checkpointUp);

    drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, setCheckpointVertices(),
              checkpointPositionBuffer, checkpointNormalBuffer, checkpointColorBuffer, checkpoint_locations);

    // Draw Checkpoint Down
    modelMatrix = m4.identity();
    modelMatrix = m4.translate(modelMatrix, tx_checkpointDown, 0.0, tz_checkpointDown);

    drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, setCheckpointVertices(),
              checkpointPositionBuffer, checkpointNormalBuffer, checkpointColorBuffer, checkpoint_locations);

    // Draw Road
    modelMatrix = m4.identity();
    modelMatrix = m4.translate(modelMatrix, tx_road, 0.0, tz_road);

    drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, setRoadVertices(),
              roadPositionBuffer, roadNormalBuffer, roadColorBuffer, road_locations);

    requestAnimationFrame(updateScene);
  }

  updateScene();
}

function drawObject(gl, modelMatrixUniformLocation, inverseTransposeModelMatrixUniformLocation, modelMatrix, vertices, positionBuffer, normalBuffer, colorBuffer, locations) {
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.vertexAttribPointer(locations[0], 3, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
  gl.vertexAttribPointer(locations[1], 3, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  gl.vertexAttribPointer(locations[2], 3, gl.FLOAT, false, 0, 0);

  gl.uniformMatrix4fv(modelMatrixUniformLocation, false, modelMatrix);
  var inverseTransposeModelMatrix = m4.transpose(m4.inverse(modelMatrix));
  gl.uniformMatrix4fv(inverseTransposeModelMatrixUniformLocation, false, inverseTransposeModelMatrix);
  gl.drawArrays(gl.TRIANGLES, 0, vertices.length / 3);
}

function addToBuffer(gl, positionBuffer, normalBuffer, colorBuffer, vertices, normals, colors) {
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);

  gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(normals), gl.STATIC_DRAW);

  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);
}

function setLocations(gl, program, positionBuffer, normalBuffer, colorBuffer) {
  const positionLocation = gl.getAttribLocation(program, `aPosition`);
  gl.enableVertexAttribArray(positionLocation);
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.vertexAttribPointer(positionLocation, 3, gl.FLOAT, false, 0, 0);

  const normalLocation = gl.getAttribLocation(program, `aNormal`);
  gl.enableVertexAttribArray(normalLocation);
  gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
  gl.vertexAttribPointer(normalLocation, 3, gl.FLOAT, false, 0, 0);

  const colorLocation = gl.getAttribLocation(program, `aColor`);
  gl.enableVertexAttribArray(colorLocation);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  gl.vertexAttribPointer(colorLocation, 3, gl.FLOAT, false, 0, 0);

  return [positionLocation, normalLocation, colorLocation]
}

function setPlayerVertices(){
  const playerData = [
    // Body Right
    0.07, 0.15, 0.07,
    0.07, -.1, 0.07,
    -.07, 0.15, 0.07,
    -.07, 0.15, 0.07,
    0.07, -.1, 0.07,
    -.07, -.1, 0.07,

    // Body Back
    -.07, 0.15, 0.07,
    -.07, -.1, 0.07,
    -.07, 0.15, -.07,
    -.07, 0.15, -.07,
    -.07, -.1, 0.07,
    -.07, -.1, -.07,

    // Body Left
    -.07, 0.15, -.07,
    -.07, -.1, -.07,
    0.07, 0.15, -.07,
    0.07, 0.15, -.07,
    -.07, -.1, -.07,
    0.07, -.1, -.07,

    // Body Front
    0.07, 0.15, -.07,
    0.07, -.1, -.07,
    0.07, 0.15, 0.07,
    0.07, 0.15, 0.07,
    0.07, -.1, 0.07,
    0.07, -.1, -.07,

    // Body Top
    0.07, 0.15, 0.07,
    0.07, 0.15, -.07,
    -.07, 0.15, 0.07,
    -.07, 0.15, 0.07,
    0.07, 0.15, -.07,
    -.07, 0.15, -.07,

    // Body Bottom
    0.07, -.1, 0.07,
    0.07, -.1, -.07,
    -.07, -.1, 0.07,
    -.07, -.1, 0.07,
    0.07, -.1, -.07,
    -.07, -.1, -.07,

    // Back Body Right
    -.07, 0.02, 0.07,
    -.07, -.1, 0.07,
    -.14, 0.02, 0.07,
    -.14, 0.02, 0.07,
    -.07, -.1, 0.07,
    -.14, -.1, 0.07,

    // Back Body Left
    -.07, 0.02, -.07,
    -.07, -0.1, -.07,
    -.14, 0.02, -.07,
    -.14, 0.02, -.07,
    -.07, -0.1, -.07,
    -.14, -0.1, -.07,

    // Back Body Top
    0.07, 0.02, 0.07,
    0.07, 0.02, -.07,
    -.14, 0.02, 0.07,
    -.14, 0.02, 0.07,
    0.07, 0.02, -.07,
    -.14, 0.02, -.07,

    // Back Body Back
    -.14, 0.02, 0.07,
    -.14, -.1, 0.07,
    -.14, 0.02, -.07,
    -.14, 0.02, -.07,
    -.14, -.1, 0.07,
    -.14, -.1, -.07,

    // Right Wing Right
    0.05, 0.01, 0.1,
    0.05, -.08, 0.1,
    -.10, 0.01, 0.1,
    -.10, 0.01, 0.1,
    0.05, -.08, 0.1,
    -.10, -.08, 0.1,

    // Right Wing Top
    0.05, 0.01, 0.1,
    0.05, 0.01, 0.0,
    -.10, 0.01, 0.1,
    -.10, 0.01, 0.1,
    0.05, 0.01, 0.0,
    -.10, 0.01, 0.0,

    // Right Wing Back
    -.10, 0.01, 0.1,
    -.10, -.08, 0.1,
    -.10, 0.01, 0.0,
    -.10, 0.01, 0.0,
    -.10, -.08, 0.1,
    -.10, -.08, 0.0,

    // Right Wing Front
    0.05, 0.01, 0.0,
    0.05, -.08, 0.0,
    0.05, 0.01, 0.1,
    0.05, 0.01, 0.1,
    0.05, -.08, 0.1,
    0.05, -.08, 0.0,

    // Left Wing Left
    0.05, 0.01, -.1,
    0.05, -.08, -.1,
    -.10, 0.01, -.1,
    -.10, 0.01, -.1,
    0.05, -.08, -.1,
    -.10, -.08, -.1,

    // Left Wing Top
    0.05, 0.01, -.1,
    0.05, 0.01, 0.0,
    -.10, 0.01, -.1,
    -.10, 0.01, -.1,
    0.05, 0.01, 0.0,
    -.10, 0.01, 0.0,

    // Left Wing Back
    -.10, 0.01, -.1,
    -.10, -.08, -.1,
    -.10, 0.01, 0.0,
    -.10, 0.01, 0.0,
    -.10, -.08, -.1,
    -.10, -.08, 0.0,

    // Left Wing Front
    0.05, 0.01, 0.0,
    0.05, -.08, 0.0,
    0.05, 0.01, -.1,
    0.05, 0.01, -.1,
    0.05, -.08, -.1,
    0.05, -.08, 0.0,

    // Top Right
    0.04, 0.20, 0.02,
    0.04, 0.15, 0.02,
    -.04, 0.20, 0.02,
    -.04, 0.20, 0.02,
    0.04, 0.15, 0.02,
    -.04, 0.15, 0.02,

    // Top Left
    -.04, 0.20, -.02,
    -.04, 0.15, -.02,
    0.04, 0.20, -.02,
    0.04, 0.20, -.02,
    -.04, 0.15, -.02,
    0.04, 0.15, -.02,

    // Top Top
    0.04, 0.2, 0.02,
    0.04, 0.2, -.02,
    -.04, 0.2, 0.02,
    -.04, 0.2, 0.02,
    0.04, 0.2, -.02,
    -.04, 0.2, -.02,

    // Top Back
    -.04, 0.20, -.02,
    -.04, 0.15, -.02,
    -.04, 0.20, 0.02,
    -.04, 0.20, 0.02,
    -.04, 0.15, -.02,
    -.04, 0.15, 0.02,

    // Top Front
    0.04, 0.20, 0.02,
    0.04, 0.15, 0.02,
    0.04, 0.20, -.02,
    0.04, 0.20, -.02,
    0.04, 0.15, -.02,
    0.04, 0.15, 0.02,

    // Beak Top
    0.12, 0.07, 0.02,
    0.12, 0.07, -.02,
    0.07, 0.07, 0.02,
    0.07, 0.07, 0.02,
    0.12, 0.07, -.02,
    0.07, 0.07, -.02,

    // Beak Bottom
    0.12, 0.05, 0.02,
    0.12, 0.05, -.02,
    0.07, 0.05, 0.02,
    0.07, 0.05, 0.02,
    0.12, 0.05, -.02,
    0.07, 0.05, -.02,

    // Beak Right
    0.12, 0.07, 0.02,
    0.12, 0.05, 0.02,
    0.07, 0.07, 0.02,
    0.07, 0.07, 0.02,
    0.12, 0.05, 0.02,
    0.07, 0.05, 0.02,

    // Beak Left
    0.12, 0.07, -.02,
    0.12, 0.05, -.02,
    0.07, 0.07, -.02,
    0.07, 0.07, -.02,
    0.12, 0.05, -.02,
    0.07, 0.05, -.02,

    // Beak Front
    0.12, 0.07, 0.02,
    0.12, 0.05, 0.02,
    0.12, 0.07, -.02,
    0.12, 0.07, -.02,
    0.12, 0.05, -.02,
    0.12, 0.05, 0.02,

    // Beak Right
    0.02, 0.10, 0.071,
    0.02, 0.08, 0.071,
    0.00, 0.10, 0.071,
    0.00, 0.10, 0.071,
    0.02, 0.08, 0.071,
    0.00, 0.08, 0.071,

    // Beak Right
    0.02, 0.10, -.071,
    0.02, 0.08, -.071,
    0.00, 0.10, -.071,
    0.00, 0.10, -.071,
    0.02, 0.08, -.071,
    0.00, 0.08, -.071,
  ];
  return playerData;
}

function  setPlayerNormals() {
  const normalData = [
    // Body Right
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,

    // Body Back
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,

    // Body Left
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,

    // Body Front
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,

    // Body Top
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,

    // Body Bottom
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,

    // Back Body Right
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,

    // Back Body Left
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,

    // Back Body Top
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,

    // Back Body Back
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,

    // Right Wing Right
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,

    // Right Wing Top
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,

    // Right Wing Back
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,

    // Right Wing Front
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,

    // Left Wing Left
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,

    // Left Wing Top
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,

    // Left Wing Back
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,

    // Left Wing Front
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,

    // Top Right
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,

    // Top Left
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,

    // Top Top
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,

    // Top Back
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,

    // Top Front
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,

    // Beak Top
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,

    // Beak Bottom
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,

    // Beak Right
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,

    // Beak Left
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,

    // Beak Front
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
];
  return normalData;
}

function setPlayerColors() {
  let colorData = [];
  for (let face = 0; face < 18; face++) {
    let faceColor = [0.8, 0.8, 0.8];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }
  for (let face = 0; face < 10; face++) {
    let faceColor = [0.8, 0.2, 0.0];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }

  for (let face = 0; face < 10; face++) {
    let faceColor = [0.2, 0.2, 0.2];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }
  return colorData;
}

function setCarVertices(){
  const carDownData = [
    // Front
    0.15, 0.15, 0.3,
    0.15, -.05, 0.3,
    -.15, 0.15, 0.3,
    -.15, 0.15, 0.3,
    0.15, -.05, 0.3,
    -.15, -.05, 0.3,

    // Left
    -.15, 0.15, 0.3,
    -.15, -.05, 0.3,
    -.15, 0.15, -.3,
    -.15, 0.15, -.3,
    -.15, -.05, 0.3,
    -.15, -.05, -.3,

    // Back
    -.15, 0.15, -.3,
    -.15, -.05, -.3,
    0.15, 0.15, -.3,
    0.15, 0.15, -.3,
    -.15, -.05, -.3,
    0.15, -.05, -.3,

    // Right
    0.15, 0.15, -.3,
    0.15, -.05, -.3,
    0.15, 0.15, 0.3,
    0.15, 0.15, 0.3,
    0.15, -.05, 0.3,
    0.15, -.05, -.3,

    // Top
    0.15, 0.15, 0.3,
    0.15, 0.15, -.3,
    -.15, 0.15, 0.3,
    -.15, 0.15, 0.3,
    0.15, 0.15, -.3,
    -.15, 0.15, -.3,

    // Bottom
    0.15, -.05, 0.3,
    0.15, -.05, -.3,
    -.15, -.05, 0.3,
    -.15, -.05, 0.3,
    0.15, -.05, -.3,
    -.15, -.05, -.3,

    // Front
    0.15, 0.35, 0.15,
    0.15, 0.15, 0.15,
    -.15, 0.35, 0.15,
    -.15, 0.35, 0.15,
    0.15, 0.15, 0.15,
    -.15, 0.15, 0.15,

    // Left
    -.15, 0.35, 0.15,
    -.15, 0.15, 0.15,
    -.15, 0.35, -.15,
    -.15, 0.35, -.15,
    -.15, 0.15, 0.15,
    -.15, 0.15, -.15,

    // Back
    -.15, 0.35, -.15,
    -.15, 0.15, -.15,
    0.15, 0.35, -.15,
    0.15, 0.35, -.15,
    -.15, 0.15, -.15,
    0.15, 0.15, -.15,

    // Right
    0.15, 0.35, -.15,
    0.15, 0.15, -.15,
    0.15, 0.35, 0.15,
    0.15, 0.35, 0.15,
    0.15, 0.15, 0.15,
    0.15, 0.15, -.15,

    // Top
    0.15, 0.35, 0.15,
    0.15, 0.35, -.15,
    -.15, 0.35, 0.15,
    -.15, 0.35, 0.15,
    0.15, 0.35, -.15,
    -.15, 0.35, -.15,

    // Back Wheel Left
    -.151, 0.05, .10,
    -.151, -.10, .10,
    -.151, 0.05, 0.25,
    -.151, 0.05, 0.25,
    -.151, -.10, 0.25,
    -.151, -.10, .10,

    // Back Wheel Back
    -.151, 0.05, .25,
    -.151, -.10, .25,
    -.100, 0.05, .25,
    -.100, 0.05, .25,
    -.151, -.10, .25,
    -.100, -.10, .25,

    // Back Wheel Front
    -.151, 0.05, .10,
    -.151, -.10, .10,
    -.100, 0.05, .10,
    -.100, 0.05, .10,
    -.151, -.10, .10,
    -.100, -.10, .10,

    // Front Wheel Left
    -.151, 0.05, -.25,
    -.151, -.10, -.25,
    -.151, 0.05, -.10,
    -.151, 0.05, -.10,
    -.151, -.10, -.10,
    -.151, -.10, -.25,

    // Front Wheel Back
    -.151, 0.05, -.1,
    -.151, -.10, -.1,
    -.100, 0.05, -.1,
    -.100, 0.05, -.1,
    -.151, -.10, -.1,
    -.100, -.10, -.1,

    // Front Wheel Front
    -.151, 0.05, -.25,
    -.151, -.10, -.25,
    -.100, 0.05, -.25,
    -.100, 0.05, -.25,
    -.151, -.10, -.25,
    -.100, -.10, -.25,

    // Back Wheel Right
    .101, 0.05, .10,
    .101, -.10, .10,
    .101, 0.05, 0.25,
    .101, 0.05, 0.25,
    .101, -.10, 0.25,
    .101, -.10, .10,

    // Back Wheel Back
    .151, 0.05, .25,
    .151, -.10, .25,
    .100, 0.05, .25,
    .100, 0.05, .25,
    .151, -.10, .25,
    .100, -.10, .25,
  ];
  return carDownData;
}

function setCarNormals(){
  const carDownData = [
    // Front
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,

    // Left
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,

    // Back
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,

    // Right
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,

    // Top
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,

    // Bottom
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,
    0.0, -1.0, 0.0,

    // Front
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,

    // Left
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,

    // Back
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,
    0.0, 0.0, -1.0,

    // Right
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    1.0, 0.0, 0.0,

    // Top
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
  ];
  return carDownData;
}

function setCarColorsVertices() {
  let colorData = [];
  for (let face = 0; face < 6; face++) {
    let faceColor = [1.0, 0.0, 0.0];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }
  for (let face = 0; face < 5; face++) {
    let faceColor = [0.9, 0.9, 0.9];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }
  return colorData;
}

function setYellowCarColorsVertices() {
  let colorData = [];
  for (let face = 0; face < 6; face++) {
    let faceColor = [0.8, 0.8, 0.0];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }
  for (let face = 0; face < 5; face++) {
    let faceColor = [0.2, 0.2, 0.2];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }
  return colorData;
}

function setPurpleCarColorsVertices() {
  let colorData = [];
  for (let face = 0; face < 6; face++) {
    let faceColor = [0.8, 0.0, 0.8];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }
  for (let face = 0; face < 5; face++) {
    let faceColor = [0.8, 0.8, 0.8];
    for (let vertex = 0; vertex < 6; vertex++) {
      colorData.push(...faceColor);
    }
  }
  return colorData;
}

function setCheckpointVertices(){
  const data = [
    // Bottom
    3.0, -.3, 25.0,
    3.0, -.3, -25.,
    -.0, -.3, 25.0,
    -.0, -.3, 25.0,
    3.0, -.3, -25.,
    -.0, -.3, -25.,
  ];
  return data;
}

function setCheckpointColors(){
  const data = [
    // Bottom
    0.0, 0.7, 0.0,
    0.0, 0.7, 0.0,
    0.0, 0.7, 0.0,
    0.0, 0.7, 0.0,
    0.0, 0.7, 0.0,
    0.0, 0.7, 0.0,
  ];
  return data;
}

function setRoadVertices(){
  const data = [
    // Bottom
    2., -.31, 25.0,
    2., -.31, -25.,
    -2, -.31, 25.0,
    -2, -.31, 25.0,
    2., -.31, -25.,
    -2, -.31, -25.,
  ];
  return data;
}

function setRoadColors(){
  const data = [
    // Bottom
    0.4, 0.4, 0.4,
    0.4, 0.4, 0.4,
    0.4, 0.4, 0.4,
    0.4, 0.4, 0.4,
    0.4, 0.4, 0.4,
    0.4, 0.4, 0.4,
  ];
  return data;
}

function setTerrainNormals() {
      const data = [
      // Bottom
      0.0, 1.0, 0.0,
      0.0, 1.0, 0.0,
      0.0, 1.0, 0.0,
      0.0, 1.0, 0.0,
      0.0, 1.0, 0.0,
      0.0, 1.0, 0.0,
    ];
    return data
}

function set3dViewingMatrix(P0, P_ref, V) {
  let matrix = [];
  let N = [
    P0[0] - P_ref[0],
    P0[1] - P_ref[1],
    P0[2] - P_ref[2],
  ];
  let n = unitVector(N);
  let u = unitVector(crossProduct(V, n));
  let v = crossProduct(n, u);

  let T = [
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    -P0[0], -P0[1], -P0[2], 1,
  ];
  let R = [
    u[0], v[0], n[0], 0,
    u[1], v[1], n[1], 0,
    u[2], v[2], n[2], 0,
    0, 0, 0, 1,
  ];

  matrix = m4.multiply(R, T);
  return matrix;
}

function ortographicProjection(xw_min, xw_max, yw_min, yw_max, z_near, z_far) {
  let matrix = [
    2 / (xw_max - xw_min), 0, 0, 0,
    0, 2 / (yw_max - yw_min), 0, 0,
    0, 0, -2 / (z_near - z_far), 0,
    -(xw_max + xw_min) / (xw_max - xw_min), -(yw_max + yw_min) / (yw_max - yw_min), (z_near + z_far) / (z_near - z_far), 1,
  ];
  return matrix;
}

function perspectiveProjection(xw_min, xw_max, yw_min, yw_max, z_near, z_far) {
  let matrix = [
    -(2 * z_near) / (xw_max - xw_min), 0, 0, 0,
    0, -(2 * z_near) / (yw_max - yw_min), 0, 0,
    (xw_max + xw_min) / (xw_max - xw_min), (yw_max + yw_min) / (yw_max - yw_min), (z_near + z_far) / (z_near - z_far), -1,
    0, 0, -1, 0,
  ];
  return matrix;
}

function crossProduct(v1, v2) {
  let result = [
    v1[1] * v2[2] - v1[2] * v2[1],
    v1[2] * v2[0] - v1[0] * v2[2],
    v1[0] * v2[1] - v1[1] * v2[0]
  ];
  return result;
}

function unitVector(v) {
  let result = [];
  let vModulus = vectorModulus(v);
  return v.map(function (x) { return x / vModulus; });
}

function vectorModulus(v) {
  return Math.sqrt(Math.pow(v[0], 2) + Math.pow(v[1], 2) + Math.pow(v[2], 2));
}


function createShader(gl, type, source) {
  var shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  var success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
  if (success) {
    return shader;
  }

  console.log(gl.getShaderInfoLog(shader));
  gl.deleteShader(shader);
}

function createProgram(gl, vertexShader, fragmentShader) {
  var program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  var success = gl.getProgramParameter(program, gl.LINK_STATUS);
  if (success) {
    return program;
  }

  console.log(gl.getProgramInfoLog(program));
  gl.deleteProgram(program);
}

var m4 = {
  identity: function () {
    return [
      1, 0, 0, 0,
      0, 1, 0, 0,
      0, 0, 1, 0,
      0, 0, 0, 1
    ];
  },

  normalize: function (v, dst) {
    dst = dst || new MatType(3);
    var length = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    // make sure we don't divide by 0.
    if (length > 0.00001) {
      dst[0] = v[0] / length;
      dst[1] = v[1] / length;
      dst[2] = v[2] / length;
    }
    return dst;
  },

  multiply: function (a, b) {
    var a00 = a[0 * 4 + 0];
    var a01 = a[0 * 4 + 1];
    var a02 = a[0 * 4 + 2];
    var a03 = a[0 * 4 + 3];
    var a10 = a[1 * 4 + 0];
    var a11 = a[1 * 4 + 1];
    var a12 = a[1 * 4 + 2];
    var a13 = a[1 * 4 + 3];
    var a20 = a[2 * 4 + 0];
    var a21 = a[2 * 4 + 1];
    var a22 = a[2 * 4 + 2];
    var a23 = a[2 * 4 + 3];
    var a30 = a[3 * 4 + 0];
    var a31 = a[3 * 4 + 1];
    var a32 = a[3 * 4 + 2];
    var a33 = a[3 * 4 + 3];
    var b00 = b[0 * 4 + 0];
    var b01 = b[0 * 4 + 1];
    var b02 = b[0 * 4 + 2];
    var b03 = b[0 * 4 + 3];
    var b10 = b[1 * 4 + 0];
    var b11 = b[1 * 4 + 1];
    var b12 = b[1 * 4 + 2];
    var b13 = b[1 * 4 + 3];
    var b20 = b[2 * 4 + 0];
    var b21 = b[2 * 4 + 1];
    var b22 = b[2 * 4 + 2];
    var b23 = b[2 * 4 + 3];
    var b30 = b[3 * 4 + 0];
    var b31 = b[3 * 4 + 1];
    var b32 = b[3 * 4 + 2];
    var b33 = b[3 * 4 + 3];
    return [
      b00 * a00 + b01 * a10 + b02 * a20 + b03 * a30,
      b00 * a01 + b01 * a11 + b02 * a21 + b03 * a31,
      b00 * a02 + b01 * a12 + b02 * a22 + b03 * a32,
      b00 * a03 + b01 * a13 + b02 * a23 + b03 * a33,
      b10 * a00 + b11 * a10 + b12 * a20 + b13 * a30,
      b10 * a01 + b11 * a11 + b12 * a21 + b13 * a31,
      b10 * a02 + b11 * a12 + b12 * a22 + b13 * a32,
      b10 * a03 + b11 * a13 + b12 * a23 + b13 * a33,
      b20 * a00 + b21 * a10 + b22 * a20 + b23 * a30,
      b20 * a01 + b21 * a11 + b22 * a21 + b23 * a31,
      b20 * a02 + b21 * a12 + b22 * a22 + b23 * a32,
      b20 * a03 + b21 * a13 + b22 * a23 + b23 * a33,
      b30 * a00 + b31 * a10 + b32 * a20 + b33 * a30,
      b30 * a01 + b31 * a11 + b32 * a21 + b33 * a31,
      b30 * a02 + b31 * a12 + b32 * a22 + b33 * a32,
      b30 * a03 + b31 * a13 + b32 * a23 + b33 * a33,
    ];
  },

  transpose: function (m, dst) {
    dst = dst || new Float32Array(16);

    dst[0] = m[0];
    dst[1] = m[4];
    dst[2] = m[8];
    dst[3] = m[12];
    dst[4] = m[1];
    dst[5] = m[5];
    dst[6] = m[9];
    dst[7] = m[13];
    dst[8] = m[2];
    dst[9] = m[6];
    dst[10] = m[10];
    dst[11] = m[14];
    dst[12] = m[3];
    dst[13] = m[7];
    dst[14] = m[11];
    dst[15] = m[15];

    return dst;
  },

  inverse: function (m, dst) {
    dst = dst || new Float32Array(16);
    var m00 = m[0 * 4 + 0];
    var m01 = m[0 * 4 + 1];
    var m02 = m[0 * 4 + 2];
    var m03 = m[0 * 4 + 3];
    var m10 = m[1 * 4 + 0];
    var m11 = m[1 * 4 + 1];
    var m12 = m[1 * 4 + 2];
    var m13 = m[1 * 4 + 3];
    var m20 = m[2 * 4 + 0];
    var m21 = m[2 * 4 + 1];
    var m22 = m[2 * 4 + 2];
    var m23 = m[2 * 4 + 3];
    var m30 = m[3 * 4 + 0];
    var m31 = m[3 * 4 + 1];
    var m32 = m[3 * 4 + 2];
    var m33 = m[3 * 4 + 3];
    var tmp_0 = m22 * m33;
    var tmp_1 = m32 * m23;
    var tmp_2 = m12 * m33;
    var tmp_3 = m32 * m13;
    var tmp_4 = m12 * m23;
    var tmp_5 = m22 * m13;
    var tmp_6 = m02 * m33;
    var tmp_7 = m32 * m03;
    var tmp_8 = m02 * m23;
    var tmp_9 = m22 * m03;
    var tmp_10 = m02 * m13;
    var tmp_11 = m12 * m03;
    var tmp_12 = m20 * m31;
    var tmp_13 = m30 * m21;
    var tmp_14 = m10 * m31;
    var tmp_15 = m30 * m11;
    var tmp_16 = m10 * m21;
    var tmp_17 = m20 * m11;
    var tmp_18 = m00 * m31;
    var tmp_19 = m30 * m01;
    var tmp_20 = m00 * m21;
    var tmp_21 = m20 * m01;
    var tmp_22 = m00 * m11;
    var tmp_23 = m10 * m01;

    var t0 = (tmp_0 * m11 + tmp_3 * m21 + tmp_4 * m31) -
        (tmp_1 * m11 + tmp_2 * m21 + tmp_5 * m31);
    var t1 = (tmp_1 * m01 + tmp_6 * m21 + tmp_9 * m31) -
        (tmp_0 * m01 + tmp_7 * m21 + tmp_8 * m31);
    var t2 = (tmp_2 * m01 + tmp_7 * m11 + tmp_10 * m31) -
        (tmp_3 * m01 + tmp_6 * m11 + tmp_11 * m31);
    var t3 = (tmp_5 * m01 + tmp_8 * m11 + tmp_11 * m21) -
        (tmp_4 * m01 + tmp_9 * m11 + tmp_10 * m21);

    var d = 1.0 / (m00 * t0 + m10 * t1 + m20 * t2 + m30 * t3);

    dst[0] = d * t0;
    dst[1] = d * t1;
    dst[2] = d * t2;
    dst[3] = d * t3;
    dst[4] = d * ((tmp_1 * m10 + tmp_2 * m20 + tmp_5 * m30) -
        (tmp_0 * m10 + tmp_3 * m20 + tmp_4 * m30));
    dst[5] = d * ((tmp_0 * m00 + tmp_7 * m20 + tmp_8 * m30) -
        (tmp_1 * m00 + tmp_6 * m20 + tmp_9 * m30));
    dst[6] = d * ((tmp_3 * m00 + tmp_6 * m10 + tmp_11 * m30) -
        (tmp_2 * m00 + tmp_7 * m10 + tmp_10 * m30));
    dst[7] = d * ((tmp_4 * m00 + tmp_9 * m10 + tmp_10 * m20) -
        (tmp_5 * m00 + tmp_8 * m10 + tmp_11 * m20));
    dst[8] = d * ((tmp_12 * m13 + tmp_15 * m23 + tmp_16 * m33) -
        (tmp_13 * m13 + tmp_14 * m23 + tmp_17 * m33));
    dst[9] = d * ((tmp_13 * m03 + tmp_18 * m23 + tmp_21 * m33) -
        (tmp_12 * m03 + tmp_19 * m23 + tmp_20 * m33));
    dst[10] = d * ((tmp_14 * m03 + tmp_19 * m13 + tmp_22 * m33) -
        (tmp_15 * m03 + tmp_18 * m13 + tmp_23 * m33));
    dst[11] = d * ((tmp_17 * m03 + tmp_20 * m13 + tmp_23 * m23) -
        (tmp_16 * m03 + tmp_21 * m13 + tmp_22 * m23));
    dst[12] = d * ((tmp_14 * m22 + tmp_17 * m32 + tmp_13 * m12) -
        (tmp_16 * m32 + tmp_12 * m12 + tmp_15 * m22));
    dst[13] = d * ((tmp_20 * m32 + tmp_12 * m02 + tmp_19 * m22) -
        (tmp_18 * m22 + tmp_21 * m32 + tmp_13 * m02));
    dst[14] = d * ((tmp_18 * m12 + tmp_23 * m32 + tmp_15 * m02) -
        (tmp_22 * m32 + tmp_14 * m02 + tmp_19 * m12));
    dst[15] = d * ((tmp_22 * m22 + tmp_16 * m02 + tmp_21 * m12) -
        (tmp_20 * m12 + tmp_23 * m22 + tmp_17 * m02));

    return dst;
  },

  translation: function (tx, ty, tz) {
    return [
      1, 0, 0, 0,
      0, 1, 0, 0,
      0, 0, 1, 0,
      tx, ty, tz, 1,
    ];
  },

  xRotation: function (angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);

    return [
      1, 0, 0, 0,
      0, c, s, 0,
      0, -s, c, 0,
      0, 0, 0, 1,
    ];
  },

  yRotation: function (angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);

    return [
      c, 0, -s, 0,
      0, 1, 0, 0,
      s, 0, c, 0,
      0, 0, 0, 1,
    ];
  },

  zRotation: function (angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);

    return [
      c, s, 0, 0,
      -s, c, 0, 0,
      0, 0, 1, 0,
      0, 0, 0, 1,
    ];
  },

  scaling: function (sx, sy, sz) {
    return [
      sx, 0, 0, 0,
      0, sy, 0, 0,
      0, 0, sz, 0,
      0, 0, 0, 1,
    ];
  },

  translate: function (m, tx, ty, tz) {
    return m4.multiply(m, m4.translation(tx, ty, tz));
  },

  xRotate: function (m, angleInRadians) {
    return m4.multiply(m, m4.xRotation(angleInRadians));
  },

  yRotate: function (m, angleInRadians) {
    return m4.multiply(m, m4.yRotation(angleInRadians));
  },

  zRotate: function (m, angleInRadians) {
    return m4.multiply(m, m4.zRotation(angleInRadians));
  },

  scale: function (m, sx, sy, sz) {
    return m4.multiply(m, m4.scaling(sx, sy, sz));
  },

};

function radToDeg(r) {
  return r * 180 / Math.PI;
}

function degToRad(d) {
  return d * Math.PI / 180;
}

main();