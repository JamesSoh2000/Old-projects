#include "helpers.h"
#include <math.h>


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // loop through each row(첫번쨰 가로줄, 두번째 가로줄 ... etc)
    for (int i = 0; i < height; i++) {
        // loop through each column(첫번쨰 세로줄, 두번쨰 세로줄 ... etc)
        for (int j = 0; j < width; j++) {
            // First, we need to have float value of red, blue, green (왜냐하면 이 세개를 합치고 3으로 나눠 average값을 구할 때
            // 소수점 결과가 나올수 있기때문에 먼저 float으로 다 합치고 round를 시킨후 int로 변환)
            float a = image[i][j].rgbtBlue;
            float b = image[i][j].rgbtRed;
            float c = image[i][j].rgbtGreen;

            int average = round((a+b+c)/3);

            image[i][j].rgbtBlue = image[i][j].rgbtRed = image[i][j].rgbtGreen = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; height > i; i++) {
        for (int j = 0; width > j; j++) {

            float oriRed = image[i][j].rgbtRed;
            float oriGreen = image[i][j].rgbtGreen;
            float oriBlue = image[i][j].rgbtBlue;

            int sepiaRed = round(0.393 * oriRed + 0.769 * oriGreen + 0.189 * oriBlue);
            int sepiaGreen = round(0.349 * oriRed + 0.686 * oriGreen + 0.168 * oriBlue);
            int sepiaBlue = round(0.272 * oriRed + 0.534 * oriGreen + 0.131 * oriBlue);

            if (sepiaRed > 255) {
                sepiaRed = 255;

            }else if (sepiaGreen > 255) {
                sepiaGreen = 255;
            }else if (sepiaBlue > 255) {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; height > i; i++) {
        for (int j = 0; width > j; j++) {
            if (round(width/2) >= j) {
                RGBTRIPLE temp = image[i][j];
                image[i][j] = image[i][width-j-1];
                image[i][width-j-1] = temp;
            }

        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++) {   // current x
        for (int j = 0; j < width; j++) { // current y
            int totalRed, totalGreen, totalBlue;
            totalRed = totalGreen = totalBlue = 0;
            float count = 0.00;

            for (int k = -1; k < 2; k++) {
                for (int t = -1; t < 2; t++) {
                    int currentX = i+k;
                    int currentY = j+t;
                    if (currentX < 0 || currentY < 0 || currentX > (height-1) || currentY > (width-1)) {
                        continue;
                    }
                    totalRed += image[currentX][currentY].rgbtRed;
                    totalGreen += image[currentX][currentY].rgbtGreen;
                    totalBlue += image[currentX][currentY].rgbtBlue;
                    count++;
                }
            }
            temp[i][j].rgbtRed = round(totalRed/count);
            temp[i][j].rgbtGreen = round(totalGreen/count);
            temp[i][j].rgbtBlue = round(totalBlue/count);

        }
    }

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}
