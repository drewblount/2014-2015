// to help with my OBJ-like representation of shapes
// this is a tad cludgey, because there's no type checking anywhere---JS makes on-the-fly ObjOrientation too easy
// but that is very nice here because of polymorphism: for now this is all used on vertices.

function add_vec(v1,v2) {
    if(v1.length!=v2.length){console.log('WARNING:vectors ('+v1+', '+v2+') are incompatible shapes)');return};
    var out = [];
    for(i=0;i<v1.length;i++){
        out.push(v1[i]+v2[i]);
    };
    return out
}

function scale_vec(v,s) {
    var out = []
    for(i=0;i<v.length;i++){
        out.push(s*v[i])
    }
    return out;
}

function midpoint(v1,v2) {
    return scale_vec(add_vec(v1,v2),0.5);   
}

// rounding is an optional param determining if the answer is rounded to four decimal places
function euc_len(v, rounding) {
    var out = 0;
    for(i=0;i<v.length;i++){
        out+=v[i]*v[i]
    };
    out = Math.sqrt(out);
    if(typeof(rounding) === undefined || rounding) {
        return Math.round(out*1000)/1000
    } else {
        return out
    }
}

function dist_between(v1,v2) {
    return euc_len(from_to_vec(v1,v2));   
}

function norm_vec(v) {
    return(scale_vec(v,1/euc_len(v)));
}

function set_mag(v,mag) {
    return(scale_vec(v,mag/euc_len(v)));
}

// returns the vector from v1 to v2 (v2-v1)
function from_to_vec(v1,v2) {
    var out = []
    for(i=0;i<v1.length;i++){
        out.push(v2[i]-v1[i])
    }
    return out;
}

// scales the ray from v2 to v1 to be length mag, and returns the v at the end of that ray
function set_v1_rel_v2(v1,v2,mag) {
    var v2v1 = from_to_vec(v2,v1);
    return set_mag(v2v1,mag) 
}