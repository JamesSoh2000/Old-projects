#include "helpers.h"
#include "math.h"
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float blue = image[i][j].rgbtBlue;

            int average = round((red+green+blue)/3);

            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = average;

        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            temp[i][j] = image[i][j];
        }
    }

    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2 ,-1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            int redX = 0;
            int redY = 0;
            int GreenX = 0;
            int GreenY = 0;
            int BlueX = 0;
            int BlueY = 0;
            int Redfinal = 0;
            int Greenfinal = 0;
            int Bluefinal = 0;

            for (int x = -1; x < 2; x++) {
                for (int y = -1; y < 2; y++) {
                    int currentX = i + x;
                    int currentY = j + y;

                    if (currentX < 0 || currentY < 0 || currentX > (height - 1) || currentY > (width - 1)) {

                        continue;
                    }

                    redX += Gx[x + 1][y + 1] * image[currentX][currentY].rgbtRed;
                    redY += Gy[x + 1][y + 1] * image[currentX][currentY].rgbtRed;
                    GreenX += Gx[x + 1][y + 1] * image[currentX][currentY].rgbtGreen;
                    GreenY += Gy[x + 1][y + 1] * image[currentX][currentY].rgbtGreen;
                    BlueX += Gx[x + 1][y + 1] * image[currentX][currentY].rgbtBlue;
                    BlueY += Gy[x + 1][y + 1] * image[currentX][currentY].rgbtBlue;
                }
            }
            Redfinal = round(sqrt(pow(redX, 2) + pow(redY, 2)));
            Greenfinal = round(sqrt(pow(GreenX, 2) + pow(GreenY, 2)));
            Bluefinal = round(sqrt(pow(BlueX, 2) + pow(BlueY, 2)));

            if (Redfinal > 255) {
                Redfinal = 255;
            }else if (Greenfinal > 255) {
                Greenfinal = 255;
            }else if (Bluefinal > 255) {
                Bluefinal = 255;
            }

            temp[i][j].rgbtRed = Redfinal;
            temp[i][j].rgbtGreen = Greenfinal;
            temp[i][j].rgbtBlue = Bluefinal;
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
