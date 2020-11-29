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
def raster_frame_creator(np_list ,cellsize):
    """returns raster as a 1d array (list of all coordinates of pixels referring to lower left)
    the no of cells as a tuple and the bounding box         

    Args:
        np_list ([numpy array]): [numpy array of list of lists sent to function]
        cellsize ([float]): [cellsize as processed and passed on to main function]
    """
    #compute bbox 
    x_list = np_list[:,0].copy()
    y_list = np_list[:,1].copy()
    z_list = np_list[:,2].copy()
    
    xmin, xmax, ymin, ymax = x_list.min(), x_list.max(), y_list.min(), y_list.max()

    #determine no of cells and create bbox
    no_x, no_y = 0, 0

    if (xmax-xmin)%cellsize == 0:
        no_x = int((xmax-xmin)//cellsize)
    else:
        no_x = int((xmax-xmin)//cellsize) +1

    if (ymax-ymin)%cellsize == 0:
        no_y = int((ymax-ymin)//cellsize)
    else:
        no_y = int((ymax-ymin)//cellsize) +1
    
    bbox = ((xmin,ymin) , (xmin + no_x*cellsize , ymin + no_y*cellsize))


    #create convex hull
    conv_points = np_list[:,[0,1]]
    hull = scipy.spatial.ConvexHull(conv_points).simplices

    #raster creation
    rast_x = np.arange(bbox[0][0],bbox[1][0], cellsize)
    rast_y = np.arange(bbox[0][1],bbox[1][1], cellsize)
    rast_x = np.flip(rast_x)

    rast_coord = np.array([[i,j] for i in rast_x for j in rast_y])

    return(rast_coord , z_list , (no_x, no_y) , bbox)

def asc_file(no_y, no_x, xmin, ymin, cellsize, filename, rast_z):
    ##writing asc file
    fh = open(filename, "w")
    fh.write(f"NCOLS {no_y}\nNROWS {no_x}\nXLLCORNER {xmin}\nYLLCORNER {ymin}\nCELLSIZE {cellsize}\nNODATA_VALUE {-9999}\n") 
    for i in rast_z:
        fh.write(" ".join([str(_) for _ in i]) + '\n')
    fh.close()
    print("File written to", filename)    

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
    #compute bbox     #convert list3d to numpy array find min and max coordinates
    np_list = np.array(list_pts_3d)
    #make raster frame as 1d
    rast_coord , z_list,(no_x,no_y) ,bbox= raster_frame_creator(np_list , cellsize)
    xmin , ymin = bbox[0]

    list_pts = np_list[:,[0,1]]
    kd = scipy.spatial.KDTree(list_pts)
    
    rast_z = []
    
    for coord in rast_coord:
        _ , indx = kd.query(coord, k=1)
        rast_z.append(z_list[indx])
    
    #to put in the interpolation for z values
    rast_z=np.array(rast_z)
    rast_z=rast_z.reshape(int(no_x), int(no_y))

    #convex hull set anything outside it as     
    #create convex hull
    hull = scipy.spatial.ConvexHull(list_pts)
    filename = j_nn['output-file']
    asc_file(no_y, no_x, xmin, ymin, cellsize, filename, rast_z)


#%%
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

    cellsize =  float(j_idw['cellsize'])
    radius =  float(j_idw['radius'])
    power =  float(j_idw['power'])
    np_list = np.array(list_pts_3d)
    
    rast_coord , z_list , (no_x, no_y), bbox = raster_frame_creator(np_list ,cellsize)
    x_list = np_list[:,0].copy()
    y_list = np_list[:,1].copy()
    z_list = np_list[:,2].copy()
    xmin , ymin = bbox[0]
    
    list_pts = np_list[:,[0,1]]
    
    kd = scipy.spatial.KDTree(list_pts)
    idw_rast_z = []
    
    for coord in rast_coord:
        i = kd.query_ball_point(coord, radius)
        if not i: 
            idw_rast_z.append(-9999)
        else:         
            weights = []
            known_z = []

            for indx in i:
                i_x, i_y = coord[0], coord[1] 
                p_x, p_y = list_pts[indx][0], list_pts[indx][1]
                
                if np.all(list_pts[indx] == coord):
                    weight = 1
                    z = z_list[indx]

                    weights.append(weight)
                    known_z.append(z) 
                else: 
                    dist = ((p_x - i_x)**2 + (p_y - i_y)**2)
                    weight = (1/(dist)**power)
                    z = z_list[indx]
                    
                    weights.append(weight)
                    known_z.append(z) 

            w_array = np.array(weights)
            z_array = np.array(known_z)

            z_value = (sum(w_array * z_array)/sum(w_array))
            idw_rast_z.append(z_value)

    rast_z = np.array(idw_rast_z)
    rast_z = rast_z.reshape(int(no_x), int(no_y))

    #convex hull set anything outside it as     
    #create convex hull
    hull = scipy.spatial.ConvexHull(list_pts)
    filename = j_idw['output-file']

    asc_file(no_y, no_x, xmin, ymin, cellsize, filename, rast_z)
    

#%%
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
    #take params and create a raster outline as in nn
    cellsize =  float(j_tin['cellsize'])
    np_list = np.array(list_pts_3d)
    # load the rast coord and the other things using predefined function
    rast_coord , z_list,(no_x,no_y) ,bbox= raster_frame_creator(np_list , cellsize)
    xmin , ymin = bbox[0]
    # rast_coord = rast_coord.reshape(int(no_x),int(no_y))
    rast_z = []
    # delauney triangulation of the x and y values obtained from file
    dt = scipy.spatial.Delaunay(np_list[:,[0,1]])

    counter=0
    # find triangles
    for coord in rast_coord:
        tri_indx =  dt.find_simplex(coord)
        if (not tri_indx) :
            # NODATA
            rast_z.append(-9999)
            continue
        elif (tri_indx == -1):
            # NODATA
            rast_z.append(-9999)            
            continue
        # else:
        # vi1,vi2,vi3 = dt.simplices[tri_indx] # indices of vertcies of the triangle
        # v1,v2,v3 =  np_list[[vi1,vi2,vi3],:] # coordinates of the vertices of the triangle
        vert =  np_list[ dt.simplices[tri_indx] ,:] # coordinates of the vertices of the triangle
        #calculate barycentric weights
        # if (((vert[1][1] - vert[2][1])*(vert[0][0]-vert[2][0])) + ((vert[2][0]-vert[1][0])*(vert[0][1]-vert[2][1])) != 0):
        #     print(f"haha {counter}")
        #     counter+=1 # set up a counter to see


        w1 = (((vert[1][1] - vert[2][1])*(coord[0] - vert[2][0])) + ((vert[2][0]-vert[1][0])*(coord[1]-vert[2][1])) /
                ((vert[1][1] - vert[2][1])*(vert[0][0]-vert[2][0])) + ((vert[2][0]-vert[1][0])*(vert[0][1]-vert[2][1]))
                )

        w2 = (((vert[2][1] - vert[0][1])*(coord[0] - vert[2][0])) + ((vert[0][0]-vert[2][0])*(coord[1] - vert[2][1])) /
              ((vert[1][1] - vert[2][1])*(vert[0][0]-vert[2][0])) + ((vert[2][0]-vert[1][0])*(vert[0][1]-vert[2][1]))
                )            
        w3 = 1 - w1 - w2
        # once weight found multiply weight with the z values at vertex of each triangle
        z_val = vert[0][2]*w1 + vert[1][2]*w2 + vert[2][2]*w3
        rast_z.append(z_val)

    rast_z = np.array(rast_z).reshape(no_x, no_y)    
    filename = j_tin['output-file']
    asc_file(no_y, no_x, xmin, ymin, cellsize, filename, rast_z)
    
#%%
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
