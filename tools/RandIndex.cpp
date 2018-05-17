#include <iostream>
#include <pcl/io/ply_io.h>
#include <pcl/kdtree/kdtree_flann.h>

double computeRandIndex(pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud1, pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud2)
{
    if (cloud1->size() != cloud2->size())
    {
        std::cerr << "Cloud size don't match!" << std::endl;
        return 0;
    }
    double randIndex = 0.0;
    for (size_t i = 0; i < cloud1->size(); ++i)
    {
        for (size_t j = i + 1; j < cloud2->size(); ++j)
        {
            int cij = 0, pij = 0;
            if (cloud1->points[i].r == cloud1->points[j].r)
                cij = 1;
            if (cloud2->points[i].r == cloud2->points[j].r)
                pij = 1;
            randIndex += cij * pij + (1 - cij) * (1 - pij);
        }

        if (i % 10000 == 0)
            std::cout << i << std::endl;
    }
    randIndex /= (cloud1->size() * (cloud1->size() - 1) / 2.0);
    return randIndex;
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        std::cerr << "Lack of arguments" << std::endl;
        exit(0);
    }

    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud1(new pcl::PointCloud<pcl::PointXYZRGB>);
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud2(new pcl::PointCloud<pcl::PointXYZRGB>);

    pcl::io::loadPLYFile(argv[1], *cloud1);
    pcl::io::loadPLYFile(argv[2], *cloud2);

    std::cout << computeRandIndex(cloud1, cloud2) << std::endl;
    
    return 0;
}
