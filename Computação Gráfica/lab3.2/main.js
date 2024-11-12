function main(){
  const canvas = document.querySelector("#canvas");
  const gl = canvas.getContext('webgl', { preserveDrawingBuffer: true });

  if (!gl) {
      throw new Error('WebGL not supported');
  }

  var vertexShaderSource = document.querySelector("#vertex-shader-2d").text;
  var fragmentShaderSource = document.querySelector("#fragment-shader-2d").text;

  var vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
  var fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

  var program = createProgram(gl, vertexShader, fragmentShader);

  gl.useProgram(program);

  const positionBuffer = gl.createBuffer();

  const positionLocation = gl.getAttribLocation(program, `position`);
  gl.enableVertexAttribArray(positionLocation);
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

  const matrixUniformLocation = gl.getUniformLocation(program, `matrix`);
  const colorUniformLocation = gl.getUniformLocation(program, `color`);

  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.clearColor(1.0, 1.0, 1.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);

  let colorVector = [0, 0, 0];

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

  let theta = 0.0;
  let tx = 0.0;
  let ty = 0.0;
  let tx_step = 0.01;
  let ty_step = 0.02;

  let matrix_l = m4.identity();
  let ty_l = 0.0;
  let ty_l_step = 0.01;

  let matrix_r = m4.identity();
  let ty_r = 0.0;
  let ty_r_step = 0.01;

  let matrix_b = m4.identity();
  let tx_b = 0.0;
  let tx_b_step = 0.003;
  let ty_b = 0.0;
  let ty_b_step = 0.003;

  function pong(){
    gl.clear(gl.COLOR_BUFFER_BIT);

    playerLeft();
    playerRight();
    ball();

    requestAnimationFrame(pong);
  }

  function playerLeft() {
    let positionVectorLeft = [
      -0.95, 0.1,
      -0.9, 0.1,
      -0.95, -0.1,
      -0.95, -0.1,
      -0.9, 0.1,
      -0.9, -0.1,
    ];
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positionVectorLeft), gl.STATIC_DRAW);

    if (isKeyPressed('w')) {
      if (ty_l < 0.9) {
        ty_l += ty_l_step;
      }
    }

    if (isKeyPressed('s')) {
      if (ty_l > -0.9) {
        ty_l -= ty_l_step;
      }
    }

    matrix_l = m4.identity();
    matrix_l = m4.translate(matrix_l, 0, ty_l, 0.0);
    gl.uniform3fv(colorUniformLocation,colorVector);
    gl.uniformMatrix4fv(matrixUniformLocation, false, matrix_l);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  }

  function playerRight() {
    let positionVectorRight = [
      0.95, 0.1,
      0.9, 0.1,
      0.95, -0.1,
      0.95, -0.1,
      0.9, 0.1,
      0.9, -0.1,
    ];
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positionVectorRight), gl.STATIC_DRAW);

    if (isKeyPressed('ArrowUp')) {
      if (ty_r < 0.9) {
        ty_r += ty_r_step;
      }
    }

    if (isKeyPressed('ArrowDown')) {
      if (ty_r > -0.9) {
        ty_r -= ty_r_step;
      }
    }

    matrix_r = m4.identity();
    matrix_r = m4.translate(matrix_r, 0, ty_r, 0.0);
    gl.uniform3fv(colorUniformLocation,colorVector);
    gl.uniformMatrix4fv(matrixUniformLocation, false, matrix_r);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  }

  function ball() {
    let positionVectorBall = [
      -0.02,-0.02,
      -0.02, 0.02,
       0.02,-0.02,
      -0.02, 0.02,
       0.02,-0.02,
       0.02, 0.02,
    ];
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positionVectorBall), gl.STATIC_DRAW);

    if (tx_b > 0.9) {
      if (ty_b > (ty_r - 0.1) && ty_b < (ty_r + 0.1)) {
        tx_b_step = -tx_b_step;
        if (tx_b_step > -0.5 && tx_b_step < 0.5) {
          tx_b_step *= 1.1;
          ty_b_step *= 1.1;
        }
      }
    }

    if (tx_b < -0.9) {
      if (ty_b > (ty_l - 0.1) && ty_b < (ty_l + 0.1)) {
        tx_b_step = -tx_b_step;
        if (tx_b_step > -0.5 && tx_b_step < 0.5) {
          tx_b_step *= 1.1;
          ty_b_step *= 1.1;
        }
      }
    }

    if (ty_b > 1.0 || ty_b < -1.0) {
      ty_b_step = -ty_b_step;
    }

    tx_b += tx_b_step;
    ty_b += ty_b_step;

    matrix_b = m4.identity();
    matrix_b = m4.translate(matrix_b, tx_b, ty_b, 0.0);
    gl.uniform3fv(colorUniformLocation,colorVector);
    gl.uniformMatrix4fv(matrixUniformLocation, false, matrix_b);
    gl.drawArrays(gl.TRIANGLES, 0, 6);

  }

  pong();
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
  identity: function() {
    return [
      1, 0, 0, 0,
      0, 1, 0, 0,
      0, 0, 1, 0,
      0, 0, 0, 1
    ];
  },

  multiply: function(a, b) {
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

  translation: function(tx, ty, tz) {
    return [
        1,  0,  0,  0,
        0,  1,  0,  0,
        0,  0,  1,  0,
        tx, ty, tz, 1,
    ];
  },

  xRotation: function(angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);

    return [
      1, 0, 0, 0,
      0, c, s, 0,
      0, -s, c, 0,
      0, 0, 0, 1,
    ];
  },

  yRotation: function(angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);

    return [
      c, 0, -s, 0,
      0, 1, 0, 0,
      s, 0, c, 0,
      0, 0, 0, 1,
    ];
  },

  zRotation: function(angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);

    return [
        c, s, 0, 0,
      -s, c, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1,
    ];
  },

  scaling: function(sx, sy, sz) {
    return [
      sx, 0,  0,  0,
      0, sy,  0,  0,
      0,  0, sz,  0,
      0,  0,  0,  1,
    ];
  },

  translate: function(m, tx, ty, tz) {
    return m4.multiply(m, m4.translation(tx, ty, tz));
  },

  xRotate: function(m, angleInRadians) {
    return m4.multiply(m, m4.xRotation(angleInRadians));
  },

  yRotate: function(m, angleInRadians) {
    return m4.multiply(m, m4.yRotation(angleInRadians));
  },

  zRotate: function(m, angleInRadians) {
    return m4.multiply(m, m4.zRotation(angleInRadians));
  },

  scale: function(m, sx, sy, sz) {
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