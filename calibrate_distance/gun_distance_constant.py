dist_lists = {'m762': [8.7, 32.1, 30.4, 37.5, 34.6, 51.9, 49.5, 58.4, 55.6, 56.7, 76.1, 61.9, 62.0, 78.8, 57.7, 75.5, 68.5, 75.9, 61.4, 79.6, 64.3, 62.8, 64.1, 69.8, 59.2, 69.6, 63.7, 71.4, 64.4, 75.4, 76.6, 5.5],
'akm': [13.833333333333334, 32.833333333333336, 20.5, 33.5, 42.5, 40.5, 31.833333333333332, 30.0, 54.333333333333336, 36.5, 52.666666666666664, 44.666666666666664, 62.166666666666664, 49.666666666666664, 53.0, 47.833333333333336, 59.833333333333336, 47.0, 33.666666666666664, 53.666666666666664, 50.833333333333336, 47.833333333333336, 60.0, 56.166666666666664, 52.333333333333336, 32.0, 76.0, 47.833333333333336, 38.333333333333336, 52.166666666666664, 83.83333333333333, 3.0],
'aug': [6.2, 13.4, 18.0, 24.2, 26.2, 24.4, 24.4, 26.2, 25.2, 34.2, 25.8, 29.0, 30.6, 34.2, 30.4, 31.0, 31.6, 34.6, 26.6, 28.0, 34.4, 30.8, 28.4, 39.6, 24.0, 38.0, 28.2, 34.8, 23.4, 38.2, 29.8, 34.8, 29.8, 33.4, 32.6, 27.4, 34.4, 47.2, 32.4, 20.6, 46.0, 4.2, 0.2],
'dp28': [21.5, 17.75, 24.75, 18.0, 49.5, 28.0, 51.75, 51.5, 44.75, 34.0, 61.25, 55.25, 51.5, 74.25, 60.75, 52.75, 68.75, 54.5, 61.25, 52.25, 57.25, 56.0, 56.25, 66.75, 54.75, 69.5, 50.25, 63.0, 52.75, 43.0, 38.25, 52.0, 16.75, 19.0, 2.75, 16.75, 11.5, 16.75, 19.0, 12.0],
'groza': [7.428571428571429, 20.0, 22.857142857142858, 26.857142857142858, 24.714285714285715, 25.428571428571427, 30.0, 21.857142857142858, 30.142857142857142, 34.0, 23.285714285714285, 29.142857142857142, 27.857142857142858, 21.285714285714285, 34.57142857142857, 36.0, 29.714285714285715, 49.57142857142857, 34.42857142857143, 37.0, 54.857142857142854, 38.57142857142857, 44.0, 34.0, 53.0, 28.714285714285715, 38.57142857142857, 51.714285714285715, 35.42857142857143, 34.57142857142857, 58.42857142857143, 4.0],
'm249': [19.714285714285715, 13.571428571428571, 16.428571428571427, 16.285714285714285, 22.714285714285715, 16.285714285714285, 30.285714285714285, 32.142857142857146, 43.42857142857143, 33.142857142857146, 32.857142857142854, 22.285714285714285, 18.571428571428573, 29.285714285714285, 24.857142857142858, 22.571428571428573, 26.857142857142858, 17.142857142857142, 15.142857142857142, 21.857142857142858, 14.571428571428571, 22.285714285714285, 15.285714285714286, 15.0, 17.285714285714285, 10.714285714285714, 22.571428571428573, 12.428571428571429, 10.285714285714286, 3.0, 3.142857142857143],
'm416': [2.2, 18.8, 22.0, 26.2, 23.8, 35.2, 28.2, 39.4, 36.6, 38.2, 36.2, 44.4, 31.6, 50.8, 35.2, 48.6, 40.6, 45.2, 42.8, 46.2, 45.8, 48.2, 41.8, 46.0, 45.4, 45.2, 47.4, 48.2, 50.8, 26.0, 0.2, 0.2],
'qbz': [10.285714285714286, 18.571428571428573, 21.142857142857142, 28.0, 27.142857142857142, 30.142857142857142, 29.285714285714285, 32.285714285714285, 33.142857142857146, 32.142857142857146, 43.42857142857143, 38.142857142857146, 52.714285714285715, 38.0, 51.857142857142854, 43.0, 49.857142857142854, 47.57142857142857, 45.285714285714285, 47.42857142857143, 43.57142857142857, 47.0, 49.142857142857146, 45.57142857142857, 49.42857142857143, 45.714285714285715, 47.57142857142857, 48.142857142857146, 50.0, 45.285714285714285, 34.857142857142854, 2.142857142857143],
'scar': [7.0, 17.166666666666668, 21.5, 26.666666666666668, 24.833333333333332, 29.5, 34.833333333333336, 28.833333333333332, 37.666666666666664, 29.833333333333332, 37.666666666666664, 42.0, 39.166666666666664, 39.0, 46.333333333333336, 39.0, 40.833333333333336, 44.666666666666664, 41.333333333333336, 42.5, 45.5, 41.833333333333336, 42.833333333333336, 43.333333333333336, 42.0, 44.0, 37.5, 39.333333333333336, 41.666666666666664, 43.833333333333336, 35.833333333333336, 42.5, 36.5, 43.0, 47.666666666666664, 39.333333333333336, 45.5, 42.0, 35.5, 59.5, 46.166666666666664, 7.0, 12.666666666666666],
'g36c': [6.6, 25.6, 26.0, 28.0, 30.0, 35.0, 29.8, 36.0, 36.0, 36.8, 39.2, 41.0, 41.4, 45.8, 43.4, 53.8, 38.6, 50.6, 48.8, 45.4, 46.6, 43.8, 41.2, 44.8, 48.6, 44.8, 45.4, 45.8, 39.6, 48.4, 41.4, 49.2, 53.2, 63.2, 57.0, 31.4, 35.4, 14.0, 25.2, 27.0, 18.8, 0.2],
'pp19': [7.2, 14.8, 22.0, 20.4, 24.0, 24.2, 26.2, 24.2, 23.4, 26.6, 21.6, 24.6, 19.6, 23.2, 19.4, 23.8, 21.0, 21.0, 21.6, 22.0, 22.0, 20.6, 21.4, 18.2, 19.6, 21.2, 17.6, 23.4, 15.6, 24.4, 19.2, 16.6, 12.4, 11.4, 13.6, 12.0, 7.6, 4.4, 5.2, 3.8, 4.8],
'tommy': [14.333333333333334, 7.888888888888889, 14.333333333333334, 23.22222222222222, 20.88888888888889, 23.22222222222222, 21.77777777777778, 28.11111111111111, 23.666666666666668, 27.444444444444443, 31.11111111111111, 40.77777777777778, 33.333333333333336, 39.44444444444444, 38.77777777777778, 42.0, 37.333333333333336, 39.0, 36.55555555555556, 42.888888888888886, 33.333333333333336, 38.666666666666664, 35.111111111111114, 38.0, 40.0, 39.888888888888886, 36.666666666666664, 41.111111111111114, 35.333333333333336, 39.888888888888886, 39.55555555555556, 37.111111111111114, 41.55555555555556, 36.55555555555556, 37.666666666666664, 34.111111111111114, 40.55555555555556, 36.22222222222222, 36.111111111111114, 38.0, 38.333333333333336, 34.888888888888886, 45.111111111111114, 34.55555555555556, 37.44444444444444, 34.44444444444444, 30.11111111111111, 54.77777777777778, 0.3333333333333333],
'uzi': [7.8, 10.6, 12.6, 9.8, 13.0, 16.6, 20.8, 19.6, 20.2, 18.8, 23.6, 26.8, 30.0, 23.2, 28.0, 32.8, 33.2, 28.8, 32.0, 28.2, 31.0, 34.4, 28.4, 32.6, 29.8, 28.8, 30.6, 41.0, 30.4, 33.0, 44.4, 25.2, 18.4, 21.4, 33.8, 47.0, 4.2, 0.6],
'vss': [13, 10, 12, 12, 14, 16, 14, 16, 17, 18, 17, 19, 20, 17, 18, 20, 21, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
'ump45': [4.666666666666667, 24.166666666666668, 24.166666666666668, 25.833333333333332, 23.666666666666668, 27.5, 28.666666666666668, 27.333333333333332, 26.833333333333332, 24.833333333333332, 32.5, 28.666666666666668, 32.5, 29.0, 28.166666666666668, 30.666666666666668, 28.333333333333332, 31.666666666666668, 28.0, 27.333333333333332, 31.5, 31.0, 32.166666666666664, 28.333333333333332, 31.333333333333332, 27.833333333333332, 29.666666666666668, 30.5, 30.0, 25.333333333333332, 22.5, 37.666666666666664, 45.333333333333336, 16.666666666666668],
'vector': [10.0, 21.142857142857142, 18.714285714285715, 19.857142857142858, 18.428571428571427, 25.571428571428573, 20.571428571428573, 24.428571428571427, 26.0, 31.142857142857142, 26.142857142857142, 33.42857142857143, 32.42857142857143, 34.142857142857146, 31.0, 34.42857142857143, 35.857142857142854, 35.714285714285715, 29.142857142857142, 33.57142857142857, 35.714285714285715, 35.0, 33.42857142857143, 36.57142857142857, 33.0, 38.42857142857143, 39.857142857142854, 38.57142857142857, 36.285714285714285, 16.285714285714285, 14.714285714285714, 28.285714285714285, 20.428571428571427, 27.714285714285715, 0.5714285714285714],
'mp5k': [15.0, 31.8, 21.4, 27.0, 36.4, 23.6, 25.2, 31.6, 35.2, 30.0, 28.2, 32.2, 29.4, 27.8, 24.0, 32.4, 26.4, 28.6, 25.2, 25.8, 30.0, 28.4, 25.4, 34.0, 31.2, 28.2, 24.0, 30.6, 26.2, 31.0, 28.2, 23.4, 27.0, 29.4, 58.0, 16.8, 16.4, 48.0, 6.2, 5.2, 0.6, 1.0, 0.6],
'mini14': [9],
'qbu': [10],
'sks': [12],
'slr': [8.5],
'mk14': [16],
's686': [100],
's12k': [80],
}