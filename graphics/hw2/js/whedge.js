// the arguments of each function could be null or empty
function HEdge(v, f, pair, next) {
	// its paired edges
	this.pair = pair;
	this.next = next;
	// the vertex it points to
	this.v = v;
	// the face it is attached to
	this.f = f;
}

function Face(hedge) {
	this.h = hedge;
}

// returns the barycentric coordinates of the point at the intersection of ray r with this face
Face.prototype.with_ray(r) {
	
}

function Vertex(id, hedge) {
	// index of vertex in vertex array
	this.id = id;
	// "any h-edge pointing towards this vertex"
	this.h = hedge;
}

// takes a shape file and uses it to create the a mesh of winged half-edges
function WHEdgeMesh(shape) {
	// list of vertex positions
	this.V = shape.V;
	
	// arrays of each component
	this.hedge = [];
	this.face = [];
	this.vertex = [];
	
	for (i=0;i<shape.F.length;i++) {
		old_face = shape.F[i];
		// this inner loop goes through each vertex index in old_face (like one face row from an OBJ file)
		for (j=0;j<old_face.length;j++) {
			// the next vertex
			var v = new Vertex(old_face[j])
		}
	}
	
}