#-- my_code_hw01.py
#-- hw01 GEO1015.2020
#-- Pratyush Kumar
#-- 5359252
#-- Simon Pena Pereira
#-- 5391210


#-- import outside the standard Python library are not allowed, just those:
#%%
import math
import numpy as np
import scipy.spatial
import startin 
#-----


#%%
def nn_interpolation(list_pts_3d, j_nn):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with nearest neighbour interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_nn:        the parameters of the input for "nn"
    Output:
        returns the value of the area
 
    """  
    print("cellsize:", j_nn['cellsize'])
    cellsize =  float(j_nn['cellsize'])
    #compute bbox
    #convert list3d to numpy array find min and max coordinates
    np_list = np.array(list_pts_3d)
    x_list = np_list[:,0].copy()
    y_list = np_list[:,1].copy()
    x_list.sort()
    y_list.sort()
    xmin=x_list[0]
    xmax=x_list[-1]
    ymin=y_list[0]
    ymax=y_list[-1]

    #determine no of cells and create bbox
    no_x=0
    no_y=0

    if (xmax-xmin)%cellsize == 0:
        no_x = int((xmax-xmin)/cellsize)
    else:
        no_x = int((xmax-xmin)/cellsize) +1

    if (ymax-ymin)%cellsize == 0:
        no_y = int((ymax-ymin)/cellsize)
    else:
        no_y = int((ymax-ymin)/cellsize) +1
    
    bbox = ((xmin,ymin) , (xmin + no_x*cellsize , ymin + no_y*cellsize))

<<<<<<< HEAD
#%%

    #create convex hull
    conv_points = np_list[:,[0,1]]
    hull = scipy.spatial.ConvexHull(conv_points).simplices

=======
    #create convex hull
    conv_points = np_list[:,[0,1]]
    hull = scipy.spatial.ConvexHull(conv_points).simplices
>>>>>>> main

    #raster creation
    rast_x = np.arange(bbox[0][0],bbox[1][0], cellsize)
    rast_y = np.arange(bbox[0][1],bbox[1][1], cellsize)
    rast_y = np.flip(rast_y)

    rast_coord = np.array([[i,j] for i in rast_x for j in rast_y])
    #-- to sjkpeed up the nearest neighbour us a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    
    # list_pts = list(zip( np_list[:,0],np_list[:,1]))
    list_pts = np_list[:,[0,1]]
    kd = scipy.spatial.KDTree(list_pts)
    # for x in rast_coord:
    _ , indx = kd.query(rast_coord, k=1)
    
    #to put in the values of z:
    z_vals = np_list[:,2]
    # z_rast=[]
    # for i in indx:
    #     z_rast.append(z_vals[i]) 
    z_rast = [z_vals[i] for i in indx]
    z_rast = np.array(z_rast)
    z_rast=z_rast.reshape(no_x, no_y)
        
    ##writing asc file
    fh = open(j_nn['output-file'], "w")
    fh.write(f"NCOLS {no_y}\nNROWS {no_x}\nXLLCORNER {xmin}\nYLLCORNER {ymin}\nCELLSIZE {cellsize}\nNODATA_VALUE{-9999}\n") 
    for i in z_rast:
        fh.write(" ".join([str(_) for _ in i]) + '\n')
    fh.close()
    print("File written to", j_nn['output-file'])



def idw_interpolation(list_pts_3d, j_idw):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with IDW
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_idw:       the parameters of the input for "idw"
    Output:
        returns the value of the area
 
    """  
    print("cellsize:", j_idw['cellsize'])
    print("radius:", j_idw['radius'])

    #-- to speed up the nearest neighbour us a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    # kd = scipy.spatial.KDTree(list_pts)
    # i = kd.query_ball_point(p, radius)
    
    print("File written to", j_idw['output-file'])


def tin_interpolation(list_pts_3d, j_tin):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with linear in TIN interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_tin:       the parameters of the input for "tin"
    Output:
        returns the value of the area
 
    """  
    #-- example to construct the DT with scipy
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html#scipy.spatial.Delaunay
    # dt = scipy.spatial.Delaunay([])

    #-- example to construct the DT with startin
    # minimal docs: https://github.com/hugoledoux/startin_python/blob/master/docs/doc.md
    # how to use it: https://github.com/hugoledoux/startin_python#a-full-simple-example
    # you are *not* allowed to use the function for the tin linear interpolation that I wrote for startin
    # you need to write your own code for this step
    # but you can of course read the code [dt.interpolate_tin_linear(x, y)]
    
    print("File written to", j_tin['output-file'])


def kriging_interpolation(list_pts_3d, j_kriging):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with ordinary kriging interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_kriging:       the parameters of the input for "kriging"
    Output:
        returns the value of the area
 
    """  
    
    
    print("File written to", j_kriging['output-file'])

# %%
