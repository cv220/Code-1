# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 09:17:40 2025

@author: carson.vetsch
"""

#_______________________________________________
import math  # pulls a predefined extensive directory of python code
import numpy as np  # numerical python: library of scientific computing functions
#_______________________________________________
#_______________________________________________
def main():

    my_data_mgmt = Input_Mgmt(float)
    my_system = Lin_Solve()
    my_output = Output_Mgmt()

    size = my_data_mgmt.ask_dimension()

    my_system.a = my_data_mgmt.read_matrix(size, "coefficient")
    my_system.b = my_data_mgmt.read_vector(size, "right-hand side")

    my_system.solve_lin_system()

    print()

    print("Here is the system solution: ")
    print()

    my_output.display_matrix(my_system.a)
    my_output.display_array(my_system.b)
    my_output.display_array(my_system.x)

    my_output.store_to_file(my_system.x)


    return


#______________________________________________
#______________________________________________
class Input_Mgmt( object ):

    def __init__( self, funct ):

        self.funct  = funct


#______________________________________________
    #______________________________________________
    def ask_dimension( self ):

        while True:

            try:

                dimension = int( input( "Enter the size of the square matrix (n): " ) )

            except ValueError:

                print( "Please enter an integer value for n." )
                continue

            if dimension <= 0:

                print( "Please enter a positive integer." )

            else:

                return dimension


    #_______________________________________________
    def read_matrix( self, size, description ):

        matrix = []

        for i in range( size ):

            while True:

                row_input = input( f"Enter row { i + 1 } of the { description } matrix (space-separated { size } values): " )
                values = row_input.split()

                if len( values ) != size:

                    print( f"Row must contain exactly { size } values." )
                    continue

                try:

                    row = [ self.funct( value ) for value in values ]

                except ValueError:

                    print( "Please enter numeric values only." )
                    continue

                matrix.append( row )
                break

        return matrix


    #_______________________________________________
    def read_vector( self, size, description ):

        while True:

            vector_input = input( f"Enter the { description } vector (space-separated { size } values): " )
            values = vector_input.split()

            if len( values ) != size:

                print( f"The vector must contain exactly { size } values." )
                continue

            try:

                vector = [ self.funct( value ) for value in values ]

            except ValueError:

                print( "Please enter numeric values only." )
                continue

            return vector
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