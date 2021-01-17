var names = [ "UFU", "URU", "UBU", "ULU", "DFD", "DRD", "DBD", "DLD", "FRF", "FLF", "BRB", "BLB",
              "UFRUF", "URBUR", "UBLUB", "ULFUL", "DRFDR", "DFLDF", "DLBDL", "DBRDB" ];

var co_trans  = make_array( 2187 * 6);
var eo_trans  = make_array( 2048 * 6);
var ud1_trans = make_array(  495 * 6);
var cp_trans  = make_array(40320 * 6);
var ep_trans  = make_array(40320 * 6);
var ud2_trans = make_array(   24 * 6);

var co_prune  = make_array( 2187);
var eo_prune  = make_array( 2048);
var ud1_prune = make_array(  495);
var cp_prune  = make_array(40320);
var ep_prune  = make_array(40320);
var ud2_prune = make_array(   24);

var co = make_array( 8);
var eo = make_array(12);
var cp = make_array( 8);
var ep = make_array(12);

var co_coord, eo_coord, ud1_coord;
var cp_coord, co_coord, ud2_coord;

var phase_1_moves = make_array(12);
var phase_2_moves = make_array(18);

var c_cycles = [
	[ 0, 1, 2, 3 ], // U
	[ 4, 5, 6, 7 ], // D
	[ 0, 3, 5, 4 ], // F
	[ 1, 7, 6, 2 ], // B
	[ 0, 4, 7, 1 ], // R
	[ 2, 6, 5, 3 ], // L
];
var e_cycles = [
	[ 0,  1, 2,  3 ], // U
	[ 4,  7, 6,  5 ], // D
	[ 0,  9, 4,  8 ], // F
	[ 2, 10, 6, 11 ], // B
	[ 1,  8, 5, 10 ], // R
	[ 3, 11, 7,  9 ], // L
];
var c_twists = [
	[ 0, 0, 0, 0 ], // U
	[ 0, 0, 0, 0 ], // D
	[ 2, 1, 2, 1 ], // F
	[ 1, 2, 1, 2 ], // B
	[ 1, 2, 1, 2 ], // R
	[ 1, 2, 1, 2 ], // L
];
var e_twists = [
	[ 0, 0, 0, 0 ], // U
	[ 0, 0, 0, 0 ], // D
	[ 1, 1, 1, 1 ], // F
	[ 1, 1, 1, 1 ], // B
	[ 0, 0, 0, 0 ], // R
	[ 0, 0, 0, 0 ], // L
];

function make_array(len)
{
	var array;

	array = new Array();
	array.length = len;
	return array;
}

function move_pieces(perm, orie, cycle, twist, mod)
{
	var otmp, ptmp, i;

	ptmp = perm[cycle[0]];
	otmp = orie[cycle[0]];

	for (i = 0; i < 3; i++) {
		orie[cycle[i]] = (orie[cycle[i + 1]] + twist[i + 1]) % mod;
		perm[cycle[i]] = perm[cycle[i + 1]];
	}
	orie[cycle[3]] = (otmp + twist[0]) % mod;
	perm[cycle[3]] = ptmp;
}

function do_move(mv)
{
	var i, face;

	face = Math.floor(mv / 3);

	for (i = 0; i < (mv % 3) + 1; i++) {
		move_pieces(cp, co, c_cycles[face], c_twists[face], 3);
		move_pieces(ep, eo, e_cycles[face], e_twists[face], 2);
	}
}

function fact(n)
{
	var i;

	for (i = 1; n > 1; n--)
		i *= n;

	return i;
}

function choose(n, k)
{
	return fact(n) / (fact(k) * fact(n - k));
}

function set_eo_coord(coord)
{
	var i;

	eo[11] = 0;
	for (i = 10; i >= 0; i--, coord >>= 1) {
		eo[i] = coord & 1;
		eo[11] ^= eo[i];
	}
}

function get_eo_coord()
{
	var i, coord;

	for (i = coord = 0; i < 11; i++, coord <<= 1)
		coord |= eo[i];

	return coord >> 1;
}

function set_co_coord(coord)
{
	var i, p = 729;

	co[7] = 0;
	for (i = 6; i >= 0; i--, p = Math.floor(p / 3)) {
		co[i] = Math.floor(coord / p);
		coord -= co[i] * p;
		co[7] = (co[7] + 3 - co[i]) % 3;
	}
}

function get_co_coord()
{
	var i, p, coord;

	for (i = coord = 0, p = 1; i < 7; i++, p *= 3)
		coord += co[i] * p;

	return coord;
}

function set_ud1_coord(coord)
{
	var i, j;

	for (i = 0; i < 12; i++)
		ep[i] = 0;
	for (i = 11, j = 4; i >= 0 && j; i--) {
		if (coord >= choose(i, j - 1)) {
			coord -= choose(i, j - 1);
		} else {
			ep[i] = 8;
			j--;
		}
	}
}

function get_ud1_coord()
{
	var i, j = 0, coord = 0;

	for (i = 0; i < 12; i++) {
		if (ep[i] > 7)
			j++;
		if (j && ep[i] < 8)
			coord += choose(i, j - 1);
	}
	return coord;
}

// set a permutation coordinate: cp, ep, ud2
function set_p_coord(perm, start, len, coord)
{
	var val = 076543210;
	var p = fact(len);
	var i;
	for (i = 0; i < len; i++) {
		p /= (len - i);
		var v = 3 * Math.floor(coord / p);
		coord %= p;
		perm[start + ((val >> v) & 07)] = i ;
		var m = (1 << v) - 1;
		val = (val & m) + ((val >> 3) & ~m);
	}
}
function get_p_coord(iperm, start, len)
{
        var perm = new Array(8) ;
	var r = 0;
	var val = 076543210;
	var i;
	var m = len - 1;
        for (i=0; i<len; i++)
           perm[iperm[start+i] & m] = i ;
	for (i = 0; i + 1 < len; i++) {
		var v = 3 * perm[i];
		r = (len - i) * r + ((val >> v) & 07);
		val -= 011111110 << v;
	}
	return r;
}

function set_cp_coord (coord) { set_p_coord(cp, 0, 8, coord); }
function set_ep_coord (coord) { set_p_coord(ep, 0, 8, coord); }
function set_ud2_coord(coord) { set_p_coord(ep, 8, 4, coord); }

function get_cp_coord () { return get_p_coord(cp, 0, 8); }
function get_ep_coord () { return get_p_coord(ep, 0, 8); }
function get_ud2_coord() { return get_p_coord(ep, 8, 4); }

function get_bits(perm) {
   var r = 0 ;
   var i ;
   for (i=0; i<7; i++)
      r |= (perm[i] & 4) << i ;
   return r >> 2 ;
}

function init_trans2(group, tran_table, len, set_coord, get_coord, perm)
{
	var i, j, k, b, t, klim ;
        var base = new Array(128) ;
	for (i=0; i<len; i+=24) {
		set_coord(i) ;
		b = get_bits(perm) ;
		if (base[b] == undefined) {
			base[b] = i ;
			klim = 24 ;
		} else {
			klim = 1 ;
		}
		b = base[b] * 6 ;
		for (k=0; k<klim; k++) {
			for (j=0; j<6; j++) {
				set_coord(i + k) ;
				if (group && j >= 2) {
					do_move(j*3+1) ;
				} else {
					do_move(j*3) ;
				}
				tran_table[(i+k)*6+j] = get_coord() ;
			}
		}
		for (j=0; j<6; j++) {
			t = tran_table[i*6+j] - tran_table[b+j] ;
			for (k=klim; k<24; k++)
				tran_table[(i+k)*6+j] = t + tran_table[b+k*6+j] ;
		}
	}
}

function init_trans(group, tran_table, len, set_coord, get_coord)
{
	var i, j;
	for (i = 0; i < len; i++) {
		for (j = 0; j < 6; j++) {
			if (tran_table[i * 6 + j] == undefined) {
				var start = i;
				var face = j;
				set_coord(start);
				while (tran_table[start * 6 + face] == undefined) {
					if (group && face >= 2) // double turns on F, B, R, L, in G1
						do_move(3 * face + 1);
					else
						do_move(3 * face);
					var newpos = get_coord();
					tran_table[start * 6 + face] = newpos;
					if (len == 40320) {
						tran_table[(len - 1 - start) * 6 + face] = len - 1 - newpos;
					}
					start = newpos;
					face = 0;
					while (face < 5 && tran_table[start * 6 + face] != undefined) {
						face++;
					}
				}
			}
		}
	}
}

function init_trans_tables()
{
	init_trans(0, eo_trans, 2048, set_eo_coord,  get_eo_coord );
	init_trans(0, co_trans, 2187, set_co_coord,  get_co_coord );
	init_trans(0, ud1_trans, 495, set_ud1_coord, get_ud1_coord);

	init_trans2(1, ep_trans, 40320, set_ep_coord,  get_ep_coord, ep);
	init_trans2(1, cp_trans, 40320, set_cp_coord,  get_cp_coord, cp);
	init_trans(1, ud2_trans,   24, set_ud2_coord, get_ud2_coord);
}

function init_prune(group, coord, prune_table, tran_table, mdepth, depth, last)
{
	var i, mv;

	if (depth == mdepth)
		return;
	prune_table[coord] = depth;

	for (mv = 0; mv < 18; mv += 3) {
		var thisface = mv / 3;
		if (thisface == last || ((last & 1) == 0 && thisface == last + 1)) // don't do two moves in a row on the same face
			continue;
		var coord2 = coord;
		for (i = 0; i < 3; i++) {
			if (group && mv >= 6 && i) // double turns in G1
				break;
			coord2 = tran_table[coord2 * 6 + thisface];
			if (!(prune_table[coord2] <= depth + 1))
				init_prune(group, coord2, prune_table, tran_table, mdepth, depth + 1, thisface);
		}
	}
}

function init_prune2(group, prune_table, tran_table, mdepth)
{
	var i;
	for (i = prune_table.length - 1; i >= 0; i--) {
		prune_table[i] = mdepth;
	}
	init_prune(group, 0, prune_table, tran_table, mdepth - 1, 0, 18);
}

function init_prune_tables()
{
	init_prune2(0, eo_prune,  eo_trans,  8);
	init_prune2(0, co_prune,  co_trans,  7);
	init_prune2(0, ud1_prune, ud1_trans, 6);

	init_prune2(1, ep_prune,  ep_trans,  9);
	init_prune2(1, cp_prune,  cp_trans, 14);
	init_prune2(1, ud2_prune, ud2_trans, 5);
}

function phase_1(eo_coord, co_coord, ud1_coord, depth, last)
{
	var face, i;

	if (depth == 0)
		return (eo_coord == 0 && co_coord == 0 && ud1_coord == 0) ;
	depth-- ;
	for (face=0; face<6; face++) {
		// no two moves in a row on same face, no move on same axis after U, F, R
		if (face == last || (face == last + 1 && (last & 1) == 0))
			continue;
		var eo_coord2  = eo_coord;
		var co_coord2  = co_coord;
		var ud1_coord2 = ud1_coord;
		for (i = 0; i < 3; i++) {
			eo_coord2  = eo_trans [eo_coord2  * 6 + face];
			co_coord2  = co_trans [co_coord2  * 6 + face];
			ud1_coord2 = ud1_trans[ud1_coord2 * 6 + face];
			if (co_prune[co_coord2] <= depth &&
                            eo_prune[eo_coord2] <= depth &&
                            ud1_prune[ud1_coord2] <= depth &&
	                    phase_1(eo_coord2, co_coord2, ud1_coord2, depth, face)) {
				phase_1_moves[depth] = 3*face + i;
				return 1;
			}
		}
	}
	return 0;
}

function phase_2(ep_coord, cp_coord, ud2_coord, depth, last)
{
	var mv, face, i;

	if (depth == 0)
		return (ep_coord == 0 && cp_coord == 0 && ud2_coord == 0) ;
	depth-- ;
	for (face=0; face<6; face++) {
		// no two moves in a row on same face, no move on same axis after U, F, R
		if (face == last || (face == last + 1 && (last & 1) == 0))
			continue;
		var ep_coord2  = ep_coord;
		var cp_coord2  = cp_coord;
		var ud2_coord2 = ud2_coord;
		for (i=0; i<3; i++) {
			ep_coord2  = ep_trans [ep_coord2  * 6 + face];
			cp_coord2  = cp_trans [cp_coord2  * 6 + face];
			ud2_coord2 = ud2_trans[ud2_coord2 * 6 + face];
			if (ep_prune[ep_coord2] <= depth &&
                            cp_prune[cp_coord2] <= depth &&
                            ud2_prune[ud2_coord2] <= depth &&
	                    phase_2(ep_coord2, cp_coord2, ud2_coord2, depth, face)) {
				phase_2_moves[depth] = 3*face + (face >= 2 ? 1 : i) ;
				return 1;
			}
			if (face >= 2)
				break;
		}
	}
	return 0;
}

function set_cube(cube)
{
	var i, j, p, t;

	for (i = 0; i < 12; i++) {
		p = cube.substring(i * 3, i * 3 + 2);
		for (j = 0; j < 12; j++) {
			if ((t = names[j].indexOf(p)) != -1) {
				ep[i] = j;
				eo[i] = t;
			}
		}
	}

	for (i = 0; i < 8; i++) {
		p = cube.substring((12 * 3) + (i * 4), (12 * 3) + (i * 4) + 3);
		for (j = 0; j < 8; j++) {
			if ((t = names[j + 12].indexOf(p)) != -1) {
				cp[i] = j;
				co[i] = t;
			}
		}
	}

	co_coord  = get_co_coord();
	eo_coord  = get_eo_coord();
	ud1_coord = get_ud1_coord();
}

function print_move(mv)
{
	var faces = [ "U", "D", "F", "B", "R", "L" ];
	var num   = [ "", "2", "'" ];
	if (mv == undefined) return "";
	return faces[Math.floor(mv / 3)] + num[mv % 3] + " ";
}

function init_cube()
{
	var i;

	ep_coord = cp_coord = ud2_coord = 0;

	init_trans_tables();

	init_prune_tables();
}

function benchmark()
{
	var very_beg, very_end, beg, end, res = "";
	var cubes = [
		"BD FU FR DF LB LF RU LU BR DL RD BU RDB RFD BLU LFU LDF LBD BUR RUF",
		"RB DL LF FR UL BL UB UF FD DR BD UR BRD FRU FLD RFD RBU ULF DLB BLU",
		"DL BD LU DR UR FD BR FL RF LB UB FU LDF BRD DLB DRF LFU UBL RUF URB",
		"FU LB LD FR DR LU RU UB FD FL RB BD LUB RUF RBU DRF DBR BDL ULF LDF",
	];

	co_trans  = make_array( 2187 * 6);
	eo_trans  = make_array( 2048 * 6);
	ud1_trans = make_array(  495 * 6);
	cp_trans  = make_array(40320 * 6);
	ep_trans  = make_array(40320 * 6);
	ud2_trans = make_array(   24 * 6);
	
	co_prune  = make_array( 2187);
	eo_prune  = make_array( 2048);
	ud1_prune = make_array(  495);
	cp_prune  = make_array(40320);
	ep_prune  = make_array(40320);
	ud2_prune = make_array(   24);

	very_beg = beg = new Date();
	init_trans_tables();
	end = new Date();
	res += "initializing transition tables took " + (end - beg) + " ms<br>";

	beg = new Date();
	init_prune_tables();
	end = new Date();
	res += "initializing pruning tables took " + (end - beg) + " ms<br>";
	res += "<br>";

	for (i = 0; i < cubes.length; i++) {
		res += "solving cube " + i + " (" + cubes[i] + ")<br>";
		res += solvecube_benchmark(cubes[i]);
		res += "<br>";
	}

	very_end = new Date();

	res += "Total time: " + (very_end - very_beg) + " ms";

	return res;
}

function solvecube_benchmark(pos) {
	phase_1_moves = make_array(12);
	phase_2_moves = make_array(18);
	set_cube(pos);
	var i, beg, end;
	var sol = "";

	beg = new Date();
	for (i = 0; phase_1(eo_coord, co_coord, ud1_coord, i, 6) == 0; i++) {}
	end = new Date();
	sol += "phase 1 searched to depth " + i + " and took " + (end - beg) + " ms<br>";
	for (i = 11; i > -1; i--)
		if (phase_1_moves[i] != undefined)
			do_move(phase_1_moves[i]);

	ep_coord  = get_ep_coord();
	cp_coord  = get_cp_coord();
	ud2_coord = get_ud2_coord();

	beg = new Date();
	for (i = 0; phase_2(ep_coord, cp_coord, ud2_coord, i, 18) == 0; i++) {}
	end = new Date();
	sol += "phase 2 searched to depth " + i + " and took " + (end - beg) + " ms<br>";
	return sol;
}

function solvecube(pos, invert) {
	phase_1_moves = make_array(12);
	phase_2_moves = make_array(18);
	set_cube(pos);
	var i, sol = "";

	for (i = 0; phase_1(eo_coord, co_coord, ud1_coord, i, 6) == 0; i++) {}
	for (i = 11; i > -1; i--)
		if (phase_1_moves[i] != undefined)
			do_move(phase_1_moves[i]);

	ep_coord  = get_ep_coord();
	cp_coord  = get_cp_coord();
	ud2_coord = get_ud2_coord();

	for (i = 0; phase_2(ep_coord, cp_coord, ud2_coord, i, 18) == 0; i++) {}

	if (invert) {
		for (i = 0; i < 18; i++)
			if (phase_2_moves[i] != undefined)
				sol += print_move(phase_2_moves[i] + 2 - 2 * (phase_2_moves[i] % 3));
		for (i = 0; i < 12; i++)
			if (phase_1_moves[i] != undefined)
				sol += print_move(phase_1_moves[i] + 2 - 2 * (phase_1_moves[i] % 3));
	} else {
		for (i = 11; i > -1; i--)
			sol += print_move(phase_1_moves[i]);
		for (i = 17; i > -1; i--)
			sol += print_move(phase_2_moves[i]);
	}
	return sol;
}

/* vim: set ts=4 sw=4 noexpandtab : */
