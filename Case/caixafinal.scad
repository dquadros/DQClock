
raio = 46;

corte_topo = 5;
corte_frente = 35;
corte_traz = 24;
altura_base = 30;
largura_frente = 30;

placa = 5;

module usbc() {
    cube([11, 7, 4]);
    translate([0,0,2]) {
        rotate([0,90,0]) {
            cylinder(h=11, r=2);
        }
    }
    translate([0,7,2]) {
        rotate([0,90,0]) {
            cylinder(h=11, r=2);
        }
    }
}

module supermini() {
    cube([24, 19, 5.6]);
    translate([17, 6, 2]) {
        usbc();
    }
}

module display() {
    rotate([0, 90, 0]) {
        cylinder(h=4, r=20);
        translate([0, 0, 4]) {
            cylinder(h=1, r=17);
        }
        translate([11.5, -12, -14]) {
            cube([16, 24, 18]);
        }
    }
}

module ledrgb() {
    rotate([0, 90, 0]) {
        cylinder(h=4, r=1.5);
    }
}


module anel() {
    rotate([0, 90, 0]) {
      cylinder(h=14, r=26);
    }
    for (angle=[0:360/12:359]) {
        translate([14,21*cos(angle),21*sin(angle)]) {
            ledrgb();
        }
    }
}


module sensor() {
    translate([-8, -6, 0]) {
        cube([16, 12, 5]);
        translate([5.5, 6, 0]) {
            cylinder(h=corte_topo+5, r=5.5);
        }
    }
}

module falante() {
    rotate([0, 90, 0]) {
      cylinder(h=6, r1=16, r2=21);
      translate([0, 0, 5]) {
        cylinder(h=corte_traz-11, r=21);
      }
    }    
}

module mp3() {
    cube([15,22,20]);
}

module completo() {
    difference() {
        // partimos de uma esferea
        sphere(raio);
        
        // Corta a frente e coloca display e anel de LEDs
        translate([corte_frente, -raio, -raio]) {
            cube([raio, 2*raio, 2*raio]);
        }
        translate([corte_frente-5,0,0]) {
            display();
        }
        translate([corte_frente-19,0,0]) {
            anel();
        }
        
        // Corta o topo e coloca o sensor de toque
        translate([-raio, -raio, raio-corte_topo/2]) {
            cube([2*raio, 2*raio, corte_topo/2]);
        }
        translate([0, 0, raio-corte_topo-6]) {
            sensor();
        }
        
        // Base:
        // Encaixe da placa
        translate([-raio+26.6, -11, -raio+12-2]) {
            cube([28, 22, 6]);
        }
        // Placa
        translate([4.6, 9, -raio+1.5*placa-2]) {
            rotate([0, 0, 180]) {
                supermini();
            }
        }
        // Chanfro para conector
        translate([-52, -8.5, -raio+4]) {
            cube([30, 16, 8]);
        }
        // Corta a parte inferior
        translate([-raio, -raio, -raio-placa-2]) {
            cube([2*raio, 2*raio, 2*placa]);
        }
        
        // Traseira
        translate([-raio, -raio, -raio]) {
            cube([8, 2*raio, 2*raio]);
        }
        translate([-raio+7,0,6]) {
            falante();
        }
    }
}

module base() {
    difference() {
        completo();
        // deixa só a base
        translate([-50,-50,-altura_base]) {
            cube([100,100,100]);
        }
        // reduz um pouco o material
        translate([-18,14,-raio+11]) {
            cube([36,10,5]);
        }
        translate([-18,-24,-raio+11]) {
            cube([36,10,5]);
        }
        translate([12,-10,-raio+11]) {
            cube([11,20,5]);
        }
        // furos de fixação
        translate([-26,-14,-raio+9]) {
            cylinder(h=7, r=1);
            cylinder(h=4, r=2.5);
        }
        translate([26,-14,-raio+9]) {
            cylinder(h=7, r=1);
            cylinder(h=4, r=2.5);
        }
        translate([-26,14,-raio+9]) {
            cylinder(h=7, r=1);
            cylinder(h=4, r=2.5);
        }
        translate([26,14,-raio+9]) {
            cylinder(h=7, r=1);
            cylinder(h=4, r=2.5);
        }
        translate([0,30,-raio+9]) {
            cylinder(h=7, r=1);
            cylinder(h=4, r=2.5);
        }
        translate([0,-30,-raio+9]) {
            cylinder(h=7, r=1);
            cylinder(h=4, r=2.5);
        }
    }
}


module pr_base() {
    rotate([0, 180, 0]) {
        translate([0,0,raio-16]) {
            base();
        }
    }
}

module frente() {
    difference() {
        completo();
        // retira a base
        translate([-raio,-raio,-raio]) {
            cube([2*raio,2*raio,raio-altura_base]);
        }
        // deixa só a frente
        translate([-raio,-raio,-raio+1]) {
            cube([2*raio-largura_frente,2*raio,2*raio]);
        }
        // furos para parafuso
        translate([26,-14,-raio+16]) {
            cylinder(h=7, r=1);
        }
        translate([26,14,-raio+16]) {
            cylinder(h=7, r=1);
        }
    }
}

module pr_frente() {
    translate([0,0,+35]) {
        rotate([0,90,]) {
            frente();
        }
    }
}

module traseira() {
    difference() {
        completo();
        // retira a base
        translate([-raio,-raio,-raio]) {
            cube([2*raio,2*raio,raio-altura_base]);
        }
        // deixa só a traseira
        translate([-raio+corte_traz, -raio, -raio]) {
            cube([2*raio-corte_traz, 2*raio, 2*raio]);
        }
        translate([-26,-14,-raio+16]) {
            cylinder(h=7, r=1);
        }
        translate([-26,14,-raio+16]) {
            cylinder(h=7, r=1);
        }
    }
}

module pr_traseira() {
    translate([0,0,-22]) {
        rotate([0,90,]) {
            traseira();
        }
    }
}


module corpo() {
    difference() {
        completo();
        // deixar oco
        translate([-23,0,0]) {
            rotate([0,90,0]) {
                cylinder(r=raio-10, h=40);
            }
        }
        // retira a base
        translate([-raio,-raio,-raio]) {
            cube([2*raio,2*raio,raio-altura_base]);
        }
        // retira a frente
        translate([raio-largura_frente,-raio,-raio]) {
            cube([largura_frente,2*raio,2*raio]);
        }
        // retira a traseira
        translate([-raio-6,-raio,-raio]) {
            cube([largura_frente,2*raio,2*raio]);
        }
        // furos para parafusos
        translate([0,30,-raio+15]) {
            cylinder(h=7, r=1);
        }
        translate([0,-30,-raio+15]) {
            cylinder(h=7, r=1);
        }
    }
}

module pr_corpo() {
    translate([0,0,16]) {
        rotate([0,90,]) {
            corpo();
        }
    }
}

module explodido() {
    traseira();
    translate([20,0,0]) {
        corpo();
    }
    translate([40,0,0]) {
        frente();
    }
    translate([20, 0, -10]) {
        base();
    }
}


$fa = 1;
$fs = 0.4;

// explodido();

pr_corpo();
