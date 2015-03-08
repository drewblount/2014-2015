// from here to about line 100 is close to copied from the tutorial on learningwebgl.com
var gl;

function initGL(canvas) {
    try {
        gl = canvas.getContext("experimental-webgl");
        gl.viewportWidth = canvas.width;
        gl.viewportHeight = canvas.height;
    } catch (e) {
    }
    if (!gl) {
        alert("Could not initialise WebGL, sorry :-(");
    }
}

// gets the shader scripts from index.html
function getShader(gl, id) {
    var shaderScript = document.getElementById(id);
    if (!shaderScript) {
        return null;
    }

    var str = "";
    var k = shaderScript.firstChild;
    while (k) {
        if (k.nodeType == 3) {
            str += k.textContent;
        }
        k = k.nextSibling;
    }

    var shader;
    if (shaderScript.type == "x-shader/x-fragment") {
        shader = gl.createShader(gl.FRAGMENT_SHADER);
    } else if (shaderScript.type == "x-shader/x-vertex") {
        shader = gl.createShader(gl.VERTEX_SHADER);
    } else {
        return null;
    }

    gl.shaderSource(shader, str);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert(gl.getShaderInfoLog(shader));
        return null;
    }

    return shader;
}

// Global var for passing to webGL
var shaderProgram;
// self-explanatory, boring and essentially copied from lessons1-4 of learningwebgl.com
function initShaders() {
    var fragmentShader = getShader(gl, "shader-fs");
    var vertexShader = getShader(gl, "shader-vs");

    shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
        alert("Could not initialise shaders");
    }

    gl.useProgram(shaderProgram);

    shaderProgram.vertexPositionAttribute = gl.getAttribLocation(shaderProgram, "aVertexPosition");
    gl.enableVertexAttribArray(shaderProgram.vertexPositionAttribute);

    shaderProgram.vertexColorAttribute = gl.getAttribLocation(shaderProgram, "aVertexColor");
    gl.enableVertexAttribArray(shaderProgram.vertexColorAttribute);

    shaderProgram.pMatrixUniform = gl.getUniformLocation(shaderProgram, "uPMatrix");
    shaderProgram.mvMatrixUniform = gl.getUniformLocation(shaderProgram, "uMVMatrix");
}


// the model-view matrix. Most of the matrix stuff is taken from the example code at learningwebgl.com, lessons 1-4
var mvMatrix = mat4.create();
var mvMatrixStack = [];
var pMatrix = mat4.create();

function mvPushMatrix() {
    var copy = mat4.create();
    mat4.set(mvMatrix, copy);
    mvMatrixStack.push(copy);
}

function mvPopMatrix() {
    if (mvMatrixStack.length == 0) {
        throw "Invalid popMatrix!";
    }
    mvMatrix = mvMatrixStack.pop();
}


function setMatrixUniforms() {
    gl.uniformMatrix4fv(shaderProgram.pMatrixUniform, false, pMatrix);
    gl.uniformMatrix4fv(shaderProgram.mvMatrixUniform, false, mvMatrix);
}


function degToRad(degrees) {
    return degrees * Math.PI / 180;
}

// everything from here on was written or heavily modified by me

function drawScene() {
	resizeCanvas();
    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

	// gives a nice perspective
    // 2/18/15:: I don't quite understand what's up here
    mat4.perspective(45, gl.viewportWidth / gl.viewportHeight, 0.1, 100.0, pMatrix);
    mat4.identity(mvMatrix);

    floor_shape.drawShape(gl);
    
	// honestly this translation is a relic from old code, and all of my later positions are relative to it so I haven't fixed it
    mat4.translate(mvMatrix, [0.0, 0.3, -3]);

    if (draw_shape) {
        shape.drawShape(gl);
        shad_shape.drawShape(gl);
    };	

}

// animate uses Date().getTime() to ensure that animated movement happens at a regular speed independent of framerate.
var r1,r2,r3;
var lastTime = 0;
function animate() {
    var timeNow = new Date().getTime();
    if (lastTime != 0) {
        var elapsed = timeNow - lastTime;

        r1 += (180 * elapsed) / 1000.0;
        r2 -= (75 * elapsed) / 1000.0;
		r3 += (30 * elapsed) / 1000.0;
    }
    lastTime = timeNow;
}

// called once per frame
function tick() {
	// arranges for tick to be called again
    requestAnimFrame(tick);
	// draws everything
    drawScene();
	// changes vars for next frame
    animate();
}

var canvas = document.getElementById("webGL-canvas");
function webGLStart() {
	resizeCanvas();
    initGL(canvas);
    initShaders();
    // gets ready to draw the floor plane
	floor_shape.initBuffs(gl);
    
    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.enable(gl.DEPTH_TEST);

    tick();
	
}

function resizeCanvas() {
   // only change the size of the canvas if the size it's being displayed has changed.
	var width = $(window).width();
	var height = $(window).height()-($('div').outerHeight());
	
   if (canvas.width != width || canvas.height != height) {
	   canvas.width = width;
       canvas.height = height;	 
   }
}


var cubit = new Shape(cubeV, cubeF);
cubit.setRandomGreyscale();
//console.log('cubit is a ' + cubit.verbose());

    
// the shape can only be handled as a callback from loading the .obj file, because file loads are by default asynchronous (no function outside of the .done callback can assume that the original .obj file was ever loaded)
var max_depth=4;
var draw_shape;
var shape_arr = [];
var current_shape = 0;
var shape;
var shad_shape;

var floor_y = -0.6
var floor_shape = floor_shape(8,floor_y,16);

var light_source = [-0.5,50,-50]

function smoothHandleShape(fname) {
    $.get(fname, function(data) {
    shape_string = data.toString();
}).done(function(){
        // load the shape object from the string and initialize it
    shape = fromOBJ_string(shape_string);
    // before complexifying the shape at all, generate its shadow
    shad_shape = shape.plane_shadow(light_source,floor_y);
    console.log('shad_shape = '+shad_shape.verbose());
    shad_shape.initBuffs(gl);
    
    shape.split_verts();
    shape.setRandomGreyFaces();
    shape.scale(0.6);
    shape.initBuffs(gl);
    shape_arr.push(shape.clone());
    draw_shape=true;
    
    var rand_colors = false;
    // for moving the light around: can use four buttons or the arrow keys
    // [dx,dy,dz] for light movement
    var d_xyz = [5,5,10]
    function move_light(dx,dy,dz) {
        light_source=add_vec(light_source,[dx,dy,dz]);
        shad_shape = shape.plane_shadow(light_source,floor_y);
        shad_shape.initBuffs(gl);
    }

    function x_plus() {
        move_light(d_xyz[0],0,0);
    }
    function x_minus() {
        move_light(-d_xyz[0],0,0);
    }
    function y_plus() {
        move_light(0,d_xyz[1],0);
    }
    function y_minus() {
        move_light(0,-d_xyz[1],0);
    }

    function z_plus() {
        move_light(0,0,d_xyz[2]);
    }
    function z_minus() {
        move_light(0,0,-d_xyz[2]);
    }
    $('#minus_x').click(function(event){
        x_minus();
    });
    $('#plus_x').click(function(event){
        x_plus();
    });
    $('#minus_y').click(function(event){
        y_minus();
    });
    $('#plus_y').click(function(event){
        y_plus();
    });
    $('#minus_z').click(function(event){
        z_minus();
    });
    $('#plus_z').click(function(event){
        z_plus();
    });
    // also have arrow-key control
    $(window).keydown(function(event){
        if(event.keyCode == 37) {
            x_minus();
        }
        if(event.keyCode == 39) {
            x_plus();
        }
        if(event.keyCode == 40) {
            z_minus();
        }
        if(event.keyCode == 38) {
            z_plus()
        }
    })
    }
    )
};
    

var shape_fname = OBJ_name_parse('icosahedron');
console.log('shape_fname = ' + shape_fname);
smoothHandleShape(shape_fname);


