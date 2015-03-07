// The goal here is to make a tiny little library for storing/manipulating
// 3d shapes in JS, in a class called 'Shape'. The Shape class will be used
// for the initial loading of shapes (from OBJ files or hard-coded data) into
// webgl

//var icos;
// assumes 'vertices' and 'faces' are each either arrays of arrays (one array for each v/f), or flat 1-d arrays representing 3-vectors. In either case, the Shape's V and F are stored as arrays of 3-arrays.
function Shape (vertices, faces) {
	// typeof(array)='object' in JS
	if (typeof(vertices[0])=='object'){
		this.V = vertices;
	} else {
		this.V = [];
		for (i=0; i<vertices.length; i+=3){
			this.V.push(vertices.slice(i,i+3));
		}
	} if (typeof(faces[0])=='object'){
		this.F = faces;
	} else {
		this.F = [];
		for (i=0;i<faces.length;i+=3){
			this.F.push(faces.slice(i,i+3));
		}
	}
}

// LOAD SHAPE FROM OBJ: allows plain names, name.obj (assumed to be in the same directory as index.html), or full web link starting with http


var OBJ_name_parse = function(fname) {
    fullname = fname;
    if (fname.substring(fname.length-4,fname.length) != '.obj') {
        fullname = fullname.concat('.obj');
    }
    // remember, a user of the webpage doesn't want JS to open a local file, but one hosted somewhere online (assumed to be in the current directory on my page if not specified). Assumed: any url would start with http
    if (fname.substring(0,4) != 'http') {
        var loc = window.location.pathname; 
        var dir = loc.substring(0, loc.lastIndexOf('/'));
        fullname = dir.concat('/'.concat(fullname));
    }
    return fullname
}


// how do I make the output of this function the output of the callback function
// below??

var get_OBJ_string = function(fname, saveStr) {
    fullname = OBJ_name_parse(fname);
    var ret = $.get(fullname, function(data) {
        saveStr = data.toString();
        icos_string = saveStr;
        console.log('in ret saveStr = ' + saveStr);
        return 6
        
    })
    console.log('ret = ' + ret);
}

// region

// in efforts to isolate the asynchronous ajax section of the code:
// fstring is expected to be the OBJ file contents in string form
// fix_index is an optional arg. If true, it subtracts 1 from every
// vertex index (when describing a face), because some .obj files use
// 1-first indexing rather than 0-first
var fromOBJ_string = function(fstring, fix_index) {
    if (typeof(fix_index) === 'undefined') {var fix_index = true};
    var lines = fstring.split('\n');
    var vertices = [];
    var faces = [];
    // adds vertices and faces, and ignores all else for now
    for( i=0; i<lines.length; i++ ){
        var words = lines[i].split(/[ ,]+/); //regexp for any num of commas/spaces
        var firstLetter = words[0][0];
        if (firstLetter == 'v' || firstLetter == 'V') {
            var vect = [];
            for( j=1;j<words.length;j++ ){
                vect[j-1] = parseFloat(words[j]);    
            }
            vertices.push(vect);
        } else if (firstLetter == 'f' || firstLetter == 'F') {
            var fac = [];
            for( j=1;j<words.length;j++ ){
                if (fix_index) {fac[j-1] = parseInt(words[j]) - 1}
                else {          fac[j-1] = parseInt(words[j])};
            }
            faces.push(fac);
        }
    };
    var out = new Shape(vertices, faces);
    return out;
};


// makes it such that each vertex is only on one face. Right now, I want to do this to make
// each face its own color.
Shape.prototype.split_verts = function() {
    var new_V = [];
    var new_F = [];
    for(i=0;i<this.F.length;i++){
        var face = this.F[i];
        var new_face = []
        for(j=0;j<face.length;j++){
            new_face = new_face.concat(new_V.length);
            new_V = new_V.concat([this.V[face[j]]]);
        }
        new_F = new_F.concat([new_face]);
    }
    this.V = new_V;
    this.F = new_F;
}

Shape.prototype.find_centroid = function() {
    var avgV = [];
    for(j=0;j<this.V[0].length;j++){avgV = avgV.concat([0])};
    for(i=0;i<this.V.length;i++){
        for(j=0;j<this.V[0].length;j++){
            avgV[j]+=this.V[i][j];
        }
    }
    for(j=0;j<this.V[0].length;j++){
        avgV[j]=Math.round(avgV[j]/this.V.length*1000)/1000;
    }
    // only four decimal accuracy (gets rid of float weirdness)
    return avgV
}


// for decomposing the icos to a sphere:
// takes a face in a shape, and sierpinski-style makes it into four faces (adding vertices as necessary). Each new vertex is scaled radially so that its distance from p is either fix_dist (optional param) or the average of the distances the two vertices it interpolates.
// for non-triangular faces, this algorithm inscribes a copy of that face's shape by drawing lines between each midpoint on its edge.
Shape.prototype.decompose_face_point = function(face_id, p, fix_dist) {
    var new_vs = [];
    var v1, v2, next_i, new_vec;
    var face = this.F[face_id];
    console.log('face = ' + face);
    // for each line on the face, find the vertex on that midpoint, scale that vertex relative p, and add it to new_vs
    for(j=0;j<face.length;j++){
        var next_v = face[(j+1)%face.length];
        var mid_v = midpoint(this.V[face[j]],this.V[next_v]);
        if(fix_dist){
            new_vec = set_v1_rel_v2(mid_v,p,fix_dist);
        } else {
            var dist = 0.5*(dist_between(this.V[face[j]],p)+dist_between(this.V[next_v],p));
            new_vec = set_v1_rel_v2(mid_v,p,dist);
        }
        console.log('new_vec =  ' + new_vec);
        new_vs.push(new_vec);
    }

    // new_vs now contains all the midpoints: time to add the new faces
    // First add all the newfound vertices to V, and remember their indices for easy use
    var new_V_ids = []
    for(i=0;i<new_vs.length;i++){
        new_V_ids.push(this.V.length+i)   
    }
    this.V = this.V.concat(new_vs);
    console.log('new_vs =  ' + new_vs);
    // remember 
    
    // for each vertex on the old face, make a new face with that vertex and its two new neighbors (maintains handedness)
    var new_face = [face[0],new_V_ids[0],new_V_ids[new_V_ids.length-1]];
    this.F.push(new_face);
    for(i=1;i<face.length;i++){
        console.log('added a face here');
        var new_face = [face[i],new_V_ids[i],new_V_ids[i-1]];
        this.F.push(new_face);
    }    
    // i love this trick: the array of new_V_ids is identical to a face describing the inner triangle in the sierpinsky step
    this.F.push(new_V_ids);
    
    // final step: removes the old face (this step might make things real slow if there are tons of faces?)

}

// performs the above function on every face, using the centroid as an origin. If is_regular, assumes a fixed
// distance from the centroid
Shape.prototype.smoothen = function(is_regular) {
    var centroid = this.find_centroid();
    if(is_regular){
        var fixed_dist = dist_between(centroid,this.V[0])
    } else {
        var fixed_dist = false
    };
    var old_length = this.F.length;
    for(f_id=0;f_id<old_length;f_id++) {
        this.decompose_face_point(f_id, centroid, fixed_dist);
    }
}

Shape.prototype.test_decompose = function() {
    var p = this.find_centroid();
    var dist = dist_between(this.V[0],p);
    this.decompose_face_point(0,p,dist);
}


// Shape.color should be a flat array of rgba values (4 array entries) for each vertex
Shape.prototype.setUniformColor = function(r,g,b,a) {
	this.color = [];
	var col = [r,g,b,a];
	for(i=0;i<this.V.length;i++){
		this.color=this.color.concat(col);
	}
};

Shape.prototype.setRandomGreyscale = function() {
	this.color = [];
	var l; //for lightness
	for(i=0;i<this.V.length;i++){
		l = Math.random(); 
		this.color = this.color.concat([l,l,l,1])
	}
};

// like above, but makes each face a uniform random grey shade (if different faces share a vertex, whichever face is last in the F array will be a solid color at the expense of those before it)
Shape.prototype.setRandomGreyFaces = function() {
	var l; //for lightness
    var colorObj = {};
    this.color = [];
	for(i=0;i<this.F.length;i++){
		l = Math.random()*0.3+0.35 ; 
		var f = this.F[i];
        for(j=0;j<f.length;j++){
            if(colorObj[f[j]] === undefined){colorObj[f[j]] = [l,l,l,1]}; 
        }
	}
    // now copy the dictionary to an array
    for(i=0;i<this.V.length;i++){
        //this.color = this.color.concat(colorObj[i]);
        if(colorObj[i] !== undefined){
            this.color = this.color.concat(colorObj[i]);
        } else { // in case a vertex isn't in any face
            this.color = this.color.concat([l,l,l,1]);
        }
    }
};

// clones the shape. taken from John Resig's great answer to http://stackoverflow.com/questions/122102/what-is-the-most-efficient-way-to-clone-an-object
Shape.prototype.clone = function() {
    return jQuery.extend(true, {}, this);   
}


Shape.prototype.getInfo = function() {
	return "Shape with " + this.V.length + " vertices and " + this.F.length + " faces.";
};

Shape.prototype.toString = function() {
	return this.getInfo();
};

Shape.prototype.valueOf = function() {
	return this.getInfo();
};

Shape.prototype.verbose = function() {
	var outS = this.toString() + '\nVERTICES:\n';
	for (i=0;i<this.V.length;i++){
		outS = outS.concat(String(this.V[i])+',\n');
	}
	outS = outS.concat('FACES:\n')
	for (i=0;i<this.F.length;i++){
		outS = outS.concat(String(this.F[i])+',\n');
	}
    outS = outS.concat('COLORS:\n')
    if (typeof(this.color) !== 'undefined') {
        for (i=0;i<this.color.length;i++){
		  outS = outS.concat(String(this.color[i])+',\n');
        }
    }else {
        outS = outS.concat('<none>');
    }
	return outS;
};

// helpful
function flatten(twoDarray){
	return twoDarray.reduce(function(a, b) {
	  return a.concat(b);
	});
};


// Aimed to recreate the functionality of the initBuffers() function. takes a gl instance argument
Shape.prototype.initBuffs = function(gl) {
	
    this.positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
	
	// hands vertex position data to webGL
	gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(flatten(this.V)), gl.STATIC_DRAW);
	// these parameters are used elsewhere in script.js
    this.positionBuffer.itemSize = 3;
    this.positionBuffer.numItems = this.V.length;
	
	this.colorBuffer = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
	
	// checks to see if color has been set; else makes the shape gray
	if(typeof this.color === 'undefined') {this.setUniformColor(0.5,0.5,0.5,0)}
	
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.color), gl.STATIC_DRAW);
    this.colorBuffer.itemSize = 4;
    this.colorBuffer.numItems = this.color.length/4;
    
	
	this.indexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.indexBuffer);
	
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(this.F)), gl.STATIC_DRAW);
	// not sure why the following two are "unflattened," but they were in the example
    this.indexBuffer.itemSize = 1;
    this.indexBuffer.numItems = this.F.length * 3;
	
};

// replicates the shape-specific action of the drawScene() function in script.js. It's assumed that gl has already translated/rotated and whatever, and all that's left is to draw the shape
Shape.prototype.drawShape = function(gl) {
	
	gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
	// shaderProgram is inherited from script.js. Assumes positions are 3-vectors
	gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, this.positionBuffer.itemSize, gl.FLOAT, false, 0, 0);
	
    gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
    gl.vertexAttribPointer(shaderProgram.vertexColorAttribute, this.colorBuffer.itemSize, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.indexBuffer);
    setMatrixUniforms();
    gl.drawElements(gl.TRIANGLES, this.indexBuffer.numItems, gl.UNSIGNED_SHORT, 0);
	
};

var cubeV = [
        // Front face
        -1.0, -1.0,  1.0,
         1.0, -1.0,  1.0,
         1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,

        // Back face
        -1.0, -1.0, -1.0,
        -1.0,  1.0, -1.0,
         1.0,  1.0, -1.0,
         1.0, -1.0, -1.0,

        // Top face
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0, -1.0,

        // Bottom face
        -1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0,  1.0,
        -1.0, -1.0,  1.0,

        // Right face
         1.0, -1.0, -1.0,
         1.0,  1.0, -1.0,
         1.0,  1.0,  1.0,
         1.0, -1.0,  1.0,

        // Left face
        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0,  1.0, -1.0
    ];	
var cubeF = [
	0, 1, 2,      0, 2, 3,    // Front face
	4, 5, 6,      4, 6, 7,    // Back face
	8, 9, 10,     8, 10, 11,  // Top face
	12, 13, 14,   12, 14, 15, // Bottom face
	16, 17, 18,   16, 18, 19, // Right face
	20, 21, 22,   20, 22, 23  // Left face
];

// endregion


//var icos_data = $.get(




//


//icos_data



