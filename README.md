# COMP-6651-Project
Comparative study of NNS algorithms &amp; data structures

## To setup virtualenv before running as .py file
    
    virtualenv -p python3.8 env
    source env/bin/activate
    pip install -r requirements.txt


## To run project
    
    python algo.py


## Output 1

	Please enter total number of points: 150
	Total number of points:  150
	The query point co-ordinate : (84, 35)
	The nearest neighbour point co-ordinate KDTree : (88, 35)
	Total Search Time for KDTree : 0.086 ms
	The nearest neighbour point co-ordinate RTree : (88, 35)
	Total Search Time for RTree : 0.333 ms
	
![Output Image](https://github.com/ypandya614929/COMP-6651-Project/blob/main/Figure_1.png?raw=true)


## Output 2

	Please enter total number of points: 1000000
	Total number of points:  1000000
	The query point co-ordinate : (499016, 920180)
	The nearest neighbour point co-ordinate KDTree : (498890, 920166)
	Total Search Time for KDTree : 0.3830 ms
	The nearest neighbour point co-ordinate RTree : (498890, 920166)
	Total Search Time for RTree : 0.2400 ms
