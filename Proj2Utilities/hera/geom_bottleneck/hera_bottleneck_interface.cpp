#include <iostream>
#include <string>
#include "./include/bottleneck.h"
#include <vector>

int main(int argc, char ** argv){
    std::string persistance_diagram1_string = argv[1];
    std::string persistance_diagram2_string = argv[2];
    std::vector<std::pair<double, double>> diagram1, diagram2;
    if (!hera::readDiagramPointSet(persistance_diagram1_string, diagram1)){
        std::cout << "An error occurred reading: " + persistance_diagram1_string << std::endl;
        return -1;
    }
    if (!hera::readDiagramPointSet(persistance_diagram2_string, diagram2)){
        std::cout << "An error occurred reading: " + persistance_diagram2_string << std::endl;
        return -1;
    }
    double btDist = hera::bottleneckDistApprox(diagram1, diagram2, 0.01);
    std::cout << btDist << std::endl;
}