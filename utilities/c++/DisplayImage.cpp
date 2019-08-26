#include <iostream>
#include <ctime>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;

int main()
{
    cv::VideoCapture cam;

    if (!cam.open(0))
        std::cout << "Problem connecting to cam " << std::endl;
    else
        std::cout << "Successfuly connected to camera " << std::endl;

    long frameCounter = 0;

    std::time_t timeBegin = std::time(0);
    int tick = 0;

    cv::Mat frame;
    int fps = 0;
    cam.read(frame);
    int key;
    bool read_frame = true;

    while (1)
    {
        if (read_frame)
        {
            cam.read(frame);
        }

        cv::resize(frame, frame, cv::Size(900, 900));
        cv::rectangle(frame, cv::Rect(0, 0, 900, 40), cv::Scalar(0, 0, 0), -1);
        cv::putText(frame, cv::format("Frames per second: %d - %d", fps, frameCounter), cv::Point(30, 30), cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(255, 0, 0));

        cv::imshow("FPS test", frame);
        key = cv::waitKey(1);

        if (key == 32) // press Space key to toggle reading new frame
        {
            read_frame = !read_frame;
        }

        frameCounter++;

        std::time_t timeNow = std::time(0) - timeBegin;

        if (timeNow - tick >= 1)
        {
            tick++;
            fps = frameCounter;
            frameCounter = 0;
        }
    }

    return 0;
}