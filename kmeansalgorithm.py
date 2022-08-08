from PIL import Image
import numpy
from os import path

def initCentroids(image_data, K):
    random_perm = numpy.random.permutation(image_data)
    initial_centroids = random_perm[:K, :]
    return initial_centroids

def getClosestCentroids(image_data, centroids):
    idx_centroid = numpy.zeros(numpy.shape(image_data)[0])
    K = numpy.shape(centroids)[0]

    for i in range(numpy.shape(image_data)[0]):
        '''temp = numpy.zeros((K, 1))
        for j in range(K):
            temp[j] = numpy.sqrt(numpy.sum(numpy.square(image_data[i, :] - centroids[j, :])))'''
        temp = numpy.sqrt(numpy.sum(numpy.square(numpy.subtract(centroids, image_data[i, :])), axis = 1))
        idx_centroid[i] = numpy.argmin(temp)

    return idx_centroid

def computeCentroids(image_data, idx_centroid, K):
    centroids = numpy.zeros((K, numpy.shape(image_data)[1]))

    for i in range(K):
        temp = numpy.where(idx_centroid == i)
        centroids[i] = numpy.mean(image_data[temp], axis = 0)
    
    return centroids

def kMeansClustering(image_data, initial_centroids, max_iters):
    K = numpy.shape(initial_centroids)[0]
    centroids = initial_centroids

    for i in range(max_iters):
        idx_centroid = getClosestCentroids(image_data, centroids)
        centroids = computeCentroids(image_data, idx_centroid, K)

    return (centroids, idx_centroid)

def runAlgorithm(image_path, K): 
    image = Image.open(image_path)
    original_image_data = numpy.array(image)

    image_data = numpy.array(image)
    image_data = numpy.reshape(image_data, (numpy.shape(image_data)[0] * numpy.shape(image_data)[1], 3))

    initial_centroids = initCentroids(image_data, K)
    max_iters = 10

    (final_centroids, idx_centroids) = kMeansClustering(image_data, initial_centroids, max_iters)
    compressed_image_data = numpy.zeros(numpy.shape(image_data))

    for i in range(len(idx_centroids)):
        compressed_image_data[i] = final_centroids[int(idx_centroids[i])]

    compressed_image_data = numpy.reshape(compressed_image_data, numpy.shape(original_image_data))

    compressed_image = Image.fromarray(compressed_image_data.astype(numpy.uint8))
    
    compressed_image.save("compressed_{}".format(path.basename(image_path)))
