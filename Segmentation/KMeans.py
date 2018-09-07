from random import *
import numpy as np
import math

class KmeansSegmentation:
    def choose_best_centroid(self, centroids, pixel):

        best_centre_value = abs(int(centroids[0]) - int(pixel))

        best_centre_idx = 0
        for i in range(1, len(centroids)):
            temp = abs(int(centroids[i]) - int(pixel))
            if (temp < best_centre_value):
                best_centre_value = temp
                best_centre_idx = i
            else:
                continue
        return best_centre_idx

    def choose_initial_centroids(self, no_clusters, image, max_col, max_row):
        temp_col = randint(0, max_col - 1)
        temp_row = randint(0, max_row - 1)
        centroids = []
        centroids.append(image[temp_row, temp_col])
        for k in range(0, no_clusters - 1):
            while True:
                temp_col = randint(0, max_col - 1)
                temp_row = randint(0, max_row - 1)

                if image[temp_row, temp_col] not in centroids:
                    break
                else:
                    continue

            centroids.append(image[temp_row, temp_col])
        return centroids

    def recompute_centroids(self, centroid_map, image, k, centroids, max_col, max_row):

        sum = 0
        n = 0
        for i in range(0, k):
            for row in range(0, max_row):
                for col in range(0, max_col):
                    if (centroid_map[row][col] == centroids[i]):
                        sum += image[row][col]
                        n = n + 1
                    else:
                        continue

            centroids[i] = round(sum / n)
            sum = 0
            n = 0

        return centroids

    def choose_initial_centroids_rgb(self, no_clusters, image, max_col, max_row,color):
        temp_col = randint(0, max_col - 1)
        temp_row = randint(0, max_row - 1)
        centroids = []
        centroids.append(image[temp_row, temp_col][color])
        for k in range(0, no_clusters - 1):
            while True:
                temp_col = randint(0, max_col - 1)
                temp_row = randint(0, max_row - 1)

                if image[temp_row, temp_col][color] not in centroids:
                    break
                else:
                    continue

            centroids.append(image[temp_row, temp_col,color])
        return centroids

    def choose_best_centroid_rgb(self, centroids, pixel):

        #Euclidean distance
        best_centre_value = math.sqrt((math.pow(int(centroids[0][0])-int(pixel[0]),2))+(math.pow(int(centroids[0][1])-int(pixel[1]),2))+(math.pow(int(centroids[0][2])-int(pixel[2]),2)))
        best_centre_idx = 0
        for i in range(1, len(centroids)):
            temp = math.sqrt((math.pow(int(centroids[i][0])-int(pixel[0]),2))+(math.pow(int(centroids[i][1])-int(pixel[1]),2))+(math.pow(int(centroids[i][2])-int(pixel[2]),2)))

            if (temp < best_centre_value):
                best_centre_value = temp
                best_centre_idx = i
            else:
                continue
        return best_centre_idx

    def recompute_centroids_rgb(self, centroid_map, image, k, centroids, max_col, max_row,color):

        sum = 0
        n = 0
        recompute_centroids = [-1] * k
        for i in range(0, k):
            for row in range(0, max_row):
                for col in range(0, max_col):

                    if (centroid_map[row][col][color] == centroids[i][color]):
                        sum += image[row,col][color]
                        n = n + 1
                    else:
                        continue
            recompute_centroids[i] = round(sum / n)
            sum = 0
            n = 0
        return recompute_centroids

    def ThreeD(self,a, b, c):
        lst = [[['#' for col in range(a)] for col in range(b)] for row in range(c)]
        return lst

    def segmentation_grey(self, image, k=2):

        new_image = image
        max_row = len(image)
        max_col = len(image[0])

        # Choosing centroids
        centroids = self.choose_initial_centroids(k, image, max_col, max_row)
        centroid_map = [[-1] * max_col for _ in range(max_row)]

        #Kmeans Algorithm
        for i in range(0, 10):

            for row in range(0, max_row):
                for col in range(0, max_col):

                    # Choosing closest cluster centre for the current pixel
                    best_centroid = self.choose_best_centroid(centroids, image[row, col])

                    # Creating a centroid map - labeling every pixel to corresponding cluster
                    centroid_map[row][col] = centroids[best_centroid]

            # Recomputing new cluster centers
            new_centroids = self.recompute_centroids(centroid_map, image, k, centroids, max_col, max_row)
            centroids = new_centroids

        # Segementation
        for centre in centroids:
            for row in range(0, max_row):
                for col in range(0, max_col):
                    if (centre == centroid_map[row][col]):
                        new_image[row][col] = centre

        return new_image

    def segmentation_rgb(self, image, k=2):

        new_image = image[:]
        max_row = len(image)
        max_col = len(image[0])

        # Choosing centroids
        centroids_r = self.choose_initial_centroids_rgb(k, image, max_col, max_row,0)

        centroids_g = self.choose_initial_centroids_rgb(k, image, max_col, max_row,1)

        centroids_b = self.choose_initial_centroids_rgb(k, image, max_col, max_row,2)

        centroids = [[-1] * 3 for _ in range(k)]
        new_centroids = [[-1] * 3 for _ in range(k)]
        # Combing r,g,b
        for i in range(0,k):

            new_centroids[i][0] = centroids_r[i]
            new_centroids[i][1] = centroids_g[i]
            new_centroids[i][2] = centroids_b[i]

        #Initialising a 3D centroid map - labels of pixels
        centroid_map = self.ThreeD(k, max_col, max_row)
        centroids = new_centroids[:]

        #Kmeans Algorithm
        for i in range(0, 10):
            for row in range(0, max_row):
                for col in range(0, max_col):
                    px = image[row,col]
                    # Choosing closest cluster centre for the current pixel
                    best_centroid = self.choose_best_centroid_rgb(centroids,px)
                    # Creating a centroid map - labeling every pixel to corresponding cluster
                    centroid_map[row][col] = centroids[best_centroid]
            # Recomputing new cluster centers
            new_centroids_r = self.recompute_centroids_rgb(centroid_map, image, k, centroids, max_col, max_row,0)
            new_centroids_g = self.recompute_centroids_rgb(centroid_map, image, k, centroids, max_col, max_row,1)
            new_centroids_b = self.recompute_centroids_rgb(centroid_map, image, k, centroids, max_col, max_row,2)
            for i in range(0, k):
                centroids[i][0] = new_centroids_r[i]
                centroids[i][1] = new_centroids_g[i]
                centroids[i][2] = new_centroids_b[i]



        # Segementation

        for row in range(0, max_row):
            for col in range(0, max_col):
                for centre in centroids:
                    if (centre[0] == centroid_map[row][col][0]):
                        if( centre[1] == centroid_map[row][col][1]):
                            if(centre[2] == centroid_map[row][col][2]):
                                    new_image[row,col] = centre

        return new_image
