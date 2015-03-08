
// goal: draw a plane on y=0.8 (so 1/5 from the bottom of the mv cube)
// solution: just create a 2d shape object that's a big square
function floor_shape(xmag,ymag,zmag) {
    var vs = [[-xmag,ymag,zmag],[-xmag,ymag,-zmag],[xmag,ymag,-zmag],[xmag,ymag,zmag]];
    var fs = [[0,1,2],[2,3,0]];
    var floor = new Shape(vs, fs);
    var greyness = 0.9;
    floor.setUniformColor(greyness,greyness,greyness,1);
    return floor;
}

// takes a point source p, a location in three-space v, and returns the coordinates of the intersection of line pv and the plane Y=y
function point_plane_proj(p,v,y) {
    // normalized direction from p to v
    var r = norm_vec(from_to_vec(p,v));
    // assumed: the plane is for any x,z value and fixed Y=y
    var normal = [0,1,0];
    // for linear algebra
    var on_plane = [0,y,0];
    // solution from the written homework, saying v' = len*r + p
    var len = dot_vec(normal, from_to_vec(p,on_plane))/dot_vec(normal, r)
    var v_out = add_vec(scale_vec(r,len),p);
    // can do a sanity check: v_out's y-component should be essentially y
    if(Math.abs(v_out[1]-y)>0.001){
        console.log('WARNING: point_plane_proj made a bad projection on inputs (p,v,y) = ('+p+', '+v+', '+y+')');
    }
    // now to avoid colliding with the plane, add 0.001 to the y coord
    return [v_out[0],y+0.001,v_out[2]];
}

// given a shape (this), a 3d light location L, and a y-plane elevation y, returns a shape that describes this's shadow on the plane
Shape.prototype.plane_shadow = function(L,y) {
    // the face array is copied exactly
    var shad_shape=this.clone();
    // each vertex is projected (simultaneously build color array)
    var black_arr=[];
    var black=[0.1,0.1,0.1,1];
    for(vert_num=0;vert_num<this.V.length;vert_num++){
        shad_shape.V[vert_num]=point_plane_proj(L,this.V[vert_num],y);
        black_arr=black_arr.concat(black);
    }
    shad_shape.color=black_arr;
    return shad_shape
}