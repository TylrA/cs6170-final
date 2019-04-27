#include <iostream>
#include <string>
#include "./wasserstein/include/wasserstein.h"
#include <vector>

int main(int argc, char ** argv){
    std::string persistance_diagram1_string = argv[1];
    std::string persistance_diagram2_string = argv[2];
    std::vector<std::pair<double, double>> diagram1, diagram2;
    if (!hera::read_diagram_point_set(persistance_diagram1_string, diagram1)){
        std::cout << "An error occurred reading: " + persistance_diagram1_string << std::endl;
        return -1;
    }
    if (!hera::read_diagram_point_set(persistance_diagram2_string, diagram2)){
        std::cout << "An error occurred reading: " + persistance_diagram2_string << std::endl;
        return -1;
    }
    hera::AuctionParams<double> params;
    params.wasserstein_power = 1.0;
    params.delta = 0.01;
    params.internal_p = hera::get_infinity<double>();
    double wsDist = hera::wasserstein_dist(diagram1, diagram2, params, "");
//    double wsDist = hera::wasserstein_dist(diagram1, diagram2, 1.0, 2.0, "");

    std::cout << wsDist << std::endl;
}