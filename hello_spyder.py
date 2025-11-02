# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 09:17:40 2025

@author: carson.vetsch
"""

#_______________________________________________
import math #pulls a predefined extensive directory of python code
import numpy as np # numerical python: library of scientific computing functions
#_______________________________________________
#_______________________________________________
def main():
    
    my_data_mgmt = Input_Mgmt( float )
    my_system    = Lin_Solve()
    my_output    = Output_Mgmt()
    
    my_data_mgmt.read_from_file() #dot notation referred to example organization.department()
    my_data_mgmt.file_conversion()
    
    print( my_data_mgmt.matrix )
    
    my_system.a = my_data_mgmt.matrix #the matrix a from my_system pulls the data from my_data_mgmt
    
    my_data_mgmt.read_from_file()
    my_data_mgmt.file_conversion()
    
    print( my_data_mgmt.matrix )
    
    my_system.b = my_data_mgmt.matrix
    
    #my_system.test_data()
    
    my_system.solve_lin_system()
    #print( my_system.x )
    
    print()
    
    print("Here is the system solution: ")
    print()
    
    my_output.display_matrix( my_system.a )
    my_output.display_array( my_system.b )
    my_output.display_array( my_system.x )
        
    my_output.store_to_file( my_system.x )
    
    
    return


#______________________________________________
#______________________________________________
class Input_Mgmt( object ):
    
    def __init__( self, funct ):
        
        self.funct  = funct
        self.matrix = [] #need matrix, do not need size right away, it will be initialized
        
        
#______________________________________________
    #______________________________________________
    def read_from_file( self ):
     
        file_name = input("Enter the file name: " )
        
        file_name = file_name + ".txt"
        
        try:
            external_file = open( file_name, "r" ) # r is keyword for read
            
        except:
            print( "sorry, I could not find that file")
            return( -1 ) #returns to file_data_entry
        
        mtrx = [] #matrix that is empty so we can pull info into it
        
        go_on = True
        
        while go_on == True:
            
            row = external_file.readline() # .readline and the parentheses confirm it is a function
            
            if row == "":
                
                go_on = False
                
            else:
                
                row = row.rstrip( "\n")
                row = row.split() # splits rows from a single string into columns
                
                
                mtrx.append( row )
                
            
        external_file.close()
        
        self.matrix = mtrx
        
        
        return
    #_______________________________________________
    
    #_______________________________________________
    def file_conversion( self ): #converts string file to integers ^^changes read_from_file
        
        funct = self.funct
        mtrx = self.matrix
    
        rows     = len( mtrx )    # number of rows
        columns = len( mtrx[0] ) # number of columns
        
        for i in range( rows ):
            
            for j in range( columns ):
                
                mtrx[ i ][ j ] = funct(mtrx[ i ][ j ]) #now integers so no more ' ' single quotes
        
        self.matrix = mtrx
        
        
        return
    #______________________________________________
#______________________________________________
class Lin_Solve( object ):
    
    def __init__( self ):
        
        self.a = [] #matrix
        self.b = [] #rhs
        self.x = [] #solve system
        
    #______________________________________________
    def test_data( self ):
        
        print( self.a )
        print( self.b )
        
    #______________________________________________
    #_______________________________________________
    def solve_lin_system( self ):
        
        a = self.a
        b = self.b
        
        x = np.linalg.solve( a, b )
        
        self.x = x
        
        return
    #_______________________________________________        
    
#______________________________________________
#______________________________________________
class Output_Mgmt( object ):
    
    
    def __init__( self ):
        
        
        pass
        
  
    #______________________________________________
    def display_array( self, array ):
        
        for row in array:    
            print( row ) # implicit loop (no counter) (fewer characers)
            
            
        print()
        
        return
    #______________________________________________
    #_______________________________________________
    def display_matrix( self, matrix ):
        
        
        for row in matrix:
            
            for entry in row:
            
                print( entry, end = " " ) 
            
            print()
            
        print()

        
        return
    #_______________________________________________
    #_______________________________________________
    def store_to_file( self, array ):
     
        file_name = input("Save solution array as: " )
        file_name = file_name + ".txt"
        
        external_file = open( file_name, "wt" ) # wt is keyword for write
        
        for row in array:
            
            string = str( row ) + "\n"
            
            external_file.write( string )
            
        external_file.close() # make sure to add bc otherwise it could get lost(stored in buffer temperarily before saving to file)
        
        
        return
    #_______________________________________________

    #_______________________________________________
    def store_mtrx_to_file( self, matrix ):
     
        file_name = file_name = input("Enter the matrix-file name: " )
        
        external_file = open( file_name, "wt" ) # wt is keyword for write
        
        for row in matrix:
            
            string = ""
            for entry in row:
                string = string + str( entry ) + " "
                
            string = string + "\n"
     
        
            external_file.write( string )
            
        external_file.close()
        
        
        return
    #_______________________________________________

#______________________________________________
#______________________________________________
main()
#______________________________________________