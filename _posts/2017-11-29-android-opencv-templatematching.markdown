---
layout: post
title:  "template matching"
date:   2017-11-29 15:46:00
author: 김지운
cover:  "/assets/instacode.png"
---
android를 이용한 영상처리에 관심이 있어서 공부용으로 feature matching 과 template matching 을 해보았는데 feature matching 짜놓은 코드는
저장소가 날라가면서 사라져 버려서 템플릿 매칭코드만이 남았다. ㅜ.ㅜ 백업 잘해야지...
{% highlight javascript %}
#include <jni.h>
#include <string>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;

extern "C" {

int process(Mat img_input, Mat &img_result) {
    cvtColor(img_input, img_result, CV_RGBA2GRAY);

    return (0);
}
JNIEXPORT jint JNICALL
Java_com_example_kjw_opencvtest_MainActivity_convertNativeLib(
        JNIEnv*, jobject, jlong addrInput, jlong addrResult) {
    Mat &img_input = *(Mat *) addrInput;
    Mat &img_result = *(Mat *) addrResult;

    int conv = process(img_input, img_result);
    int ret = (jint) conv;

    return ret;
}
/// Global Variables
Mat img; //src image
Mat templ; //matching image
Mat result; //result
char* image_window = "Source Image";
char* result_window = "Result window";

int match_method;
int max_Trackbar = 5;

/// Function Headers
void MatchingMethod( int, void* );
/**
 * @function MatchingMethod
 * @brief Trackbar callback
 */
JNIEXPORT jint JNICALL
Java_com_example_kjw_opencvtest_MainActivity_MatchingMethod( JNIEnv*, jobject, jlong addrInput,jlong templinput ,jlong addrResult)
{
    /// Source image to display
    Mat &img_display = *(Mat *) addrInput;
    Mat &img_result = *(Mat *) addrResult;
    templ = *(Mat *) templinput;
    img.copyTo( img_display );

    /// Create the result matrix
    int result_cols =  img.cols - templ.cols + 1;
    int result_rows = img.rows - templ.rows + 1;

    result.create( result_rows, result_cols, CV_32FC1 );

    /// Do the Matching and Normalize
    matchTemplate( img, templ, result, match_method );
    normalize( result, result, 0, 1, NORM_MINMAX, -1, Mat() );

    /// Localizing the best match with minMaxLoc
    double minVal; double maxVal; Point minLoc; Point maxLoc;
    Point matchLoc;

    minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );

    /// For SQDIFF and SQDIFF_NORMED, the best matches are lower values. For all the other methods, the higher the better
    if( match_method  == CV_TM_SQDIFF || match_method == CV_TM_SQDIFF_NORMED )
    { matchLoc = minLoc; }
    else
    { matchLoc = maxLoc; }

    /// Show me what you got
    rectangle( img_display, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );
    rectangle( result, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );

//    imshow( image_window, img_display );
//    imshow( result_window, result );

    return 1;
}
}
{% endhighlight %}
