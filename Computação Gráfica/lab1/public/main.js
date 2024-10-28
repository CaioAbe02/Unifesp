function main(){
  const canvas = document.querySelector("#c");
  const gl = canvas.getContext('webgl');

  if (!gl) {
      throw new Error('WebGL not supported');
  }

  canvas.addEventListener("mousedown",mouseDown,false);

  function mouseDown(event){
    console.log(event.screenX);
    console.log(event.screenY);
  }

  let vertexShaderSource = document.querySelector("#vertex-shader-2d").text;
  let fragmentShaderSource = document.querySelector("#fragment-shader-2d").text;

  let vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
  let fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

  let program = createProgram(gl, vertexShader, fragmentShader);

  gl.useProgram(program);

  const positionBuffer = gl.createBuffer();
  const colorBuffer = gl.createBuffer();

  const positionLocation = gl.getAttribLocation(program, `position`);
  gl.enableVertexAttribArray(positionLocation);
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

  const colorLocation = gl.getAttribLocation(program, `color`);
  gl.enableVertexAttribArray(colorLocation);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  gl.vertexAttribPointer(colorLocation, 3, gl.FLOAT, false, 0, 0);

  gl.clearColor(1.0, 1.0, 1.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);

  drawCar(gl, positionBuffer, colorBuffer);
  drawFlower(gl, positionBuffer, colorBuffer);
  drawClown(gl, positionBuffer, colorBuffer);
}

function drawCar(gl, positionBuffer, colorBuffer) {
  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setRectangleVertices(gl, -0.75, 0.5, 0.2, 0.2);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setRectangleColor(gl,[1, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 6);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setRectangleVertices(gl, -0.55, 0.5, 0.5, 0.4);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setRectangleColor(gl,[1, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 6);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setRectangleVertices(gl, -0.1, 0.5, 0.3, 0.2);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setRectangleColor(gl,[1, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 6);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setRectangleVertices(gl, -0.45, 0.7, 0.3, 0.15);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setRectangleColor(gl,[0, 0.8, 1]);
  gl.drawArrays(gl.TRIANGLES, 0, 6);

  n=30;
  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.1, -0.6, 0.5);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.1, 0.0, 0.5);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);
}

function drawFlower(gl, positionBuffer, colorBuffer) {
  n=30;
  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.12, 0.0, 0.12);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0.7, 0.2, 1]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.12, 0.12, 0.0);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0.7, 0.2, 1]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.12, 0.0, -0.12);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0.7, 0.2, 1]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.12, -0.12, -0.0);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0.7, 0.2, 1]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.1, 0.0, 0.0);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0.8, 0.8, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);
}

function drawClown(gl, positionBuffer, colorBuffer) {
  n=30;
  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.1, -0.5, -0.4);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.1, -0.1, -0.4);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[0, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setCircleVertices(gl, n, 0.15, -0.3, -0.6);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setCircleColor(gl,n,[1, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 3*n);

  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  setRectangleVertices(gl, -0.5, -0.85, 0.4, 0.02);
  gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
  setRectangleColor(gl,[0, 0, 0]);
  gl.drawArrays(gl.TRIANGLES, 0, 6);
}

function createShader(gl, type, source) {
  let shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  let success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
  if (success) {
    return shader;
  }

  console.log(gl.getShaderInfoLog(shader));
  gl.deleteShader(shader);
}

function createProgram(gl, vertexShader, fragmentShader) {
  let program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  let success = gl.getProgramParameter(program, gl.LINK_STATUS);
  if (success) {
    return program;
  }

  console.log(gl.getProgramInfoLog(program));
  gl.deleteProgram(program);
}

function setRectangleVertices(gl, x, y, width, height) {
  let x1 = x;
  let x2 = x + width;
  let y1 = y;
  let y2 = y + height;
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
     x1, y1,
     x2, y1,
     x1, y2,
     x1, y2,
     x2, y1,
     x2, y2,
  ]), gl.STATIC_DRAW);
}

function setRectangleColor(gl, color) {
  colorData = [];
  for (let triangle = 0; triangle < 2; triangle++) {
    for(let vertex=0; vertex<3; vertex++)
      colorData.push(...color);
  }
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colorData), gl.STATIC_DRAW);
}

function setCircleVertices(gl, n, radius, x, y){
  let center = [x, y];
  let vertexData = [];
  for(let i=0;i<n;i++){
    vertexData.push(...center);
    vertexData.push(...[x + radius*Math.cos(i*(2*Math.PI)/n), y + radius*Math.sin(i*(2*Math.PI)/n)]);
    vertexData.push(...[x + radius*Math.cos((i+1)*(2*Math.PI)/n), y + radius*Math.sin((i+1)*(2*Math.PI)/n)]);
  }
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertexData), gl.STATIC_DRAW);
}

function setCircleColor(gl,n,color){
  colorData = [];
  for (let triangle = 0; triangle < n; triangle++) {
    for(let vertex=0; vertex<3; vertex++)
      colorData.push(...color);
  }
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colorData), gl.STATIC_DRAW);
}

main();